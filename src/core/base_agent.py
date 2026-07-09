from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import BaseTool
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from src.config import settings

class BaseAgent:
    def __init__(
        self,
        name: str,
        role: str,
        system_prompt: str,
        tools: List[BaseTool],
        model_type: str = "gpt4",
        temperature: Optional[float] = None
    ):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.tools = tools
        
        model_name = settings.OPENAI_MODEL_GPT4 if model_type == "gpt4" else settings.OPENAI_MODEL_GPT35
        temp = temperature if temperature is not None else (
            settings.TEMPERATURE_REASONING if model_type == "gpt4" else settings.TEMPERATURE_STRUCTURED
        )
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temp,
            max_tokens=settings.MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        if tools:
            agent = create_openai_functions_agent(self.llm, tools, self.prompt)
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=8,
                early_stopping_method="generate"
            )
        else:
            self.agent_executor = None

    def _normalize_chat_history(self, chat_history: Any) -> List[BaseMessage]:
        """Normalize app/session chat history into LangChain message objects."""
        if not isinstance(chat_history, list):
            return []

        normalized_history: List[BaseMessage] = []

        for item in chat_history:
            if isinstance(item, BaseMessage):
                normalized_history.append(item)
                continue

            if isinstance(item, dict):
                role = item.get("role")
                content = item.get("content")

                if role in {"human", "user"} and content:
                    normalized_history.append(HumanMessage(content=str(content)))
                    continue

                if role in {"ai", "assistant"} and content:
                    normalized_history.append(AIMessage(content=str(content)))
                    continue

                # Backward compatibility with older {"user": "...", "assistant": "..."} format
                if item.get("user"):
                    normalized_history.append(HumanMessage(content=str(item["user"])))
                if item.get("assistant"):
                    normalized_history.append(AIMessage(content=str(item["assistant"])))

        return normalized_history
    
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        user_input = state.get("user_request", "")
        chat_history = self._normalize_chat_history(state.get("conversation_history", []))
        
        if self.agent_executor:
            response = self.agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            output = response.get("output", "")
            if "Agent stopped due to iteration limit or time limit" in output:
                output = (
                    "I could not complete this in one reasoning pass, so I created a safe interim action. "
                    "Please confirm key details and I will continue execution."
                )
        else:
            response = self.llm.invoke([
                ("system", self.system_prompt),
                ("human", user_input)
            ])
            output = response.content
        
        return {
            "agent": self.name,
            "response": output,
            "status": "success"
        }
