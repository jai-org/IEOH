import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL_GPT4: str = os.getenv("OPENAI_MODEL_GPT4", "gpt-4o-mini")
    OPENAI_MODEL_GPT35: str = os.getenv("OPENAI_MODEL_GPT35", "gpt-3.5-turbo")
    TEMPERATURE_REASONING: float = float(os.getenv("TEMPERATURE_REASONING", "0.7"))
    TEMPERATURE_STRUCTURED: float = float(os.getenv("TEMPERATURE_STRUCTURED", "0.3"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4000"))
    
    DATABASE_PATH: str = "data/enterprise.db"
    
    @classmethod
    def validate(cls) -> bool:
        if not cls.OPENAI_API_KEY:
            return False
        return True

settings = Settings()
