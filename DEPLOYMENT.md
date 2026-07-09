# Live Hosting Guide (Shareable Link)

This project is ready to run as a live Streamlit app with a public URL.

## Option 1: Streamlit Community Cloud (Fastest)

1. Push this repository to GitHub.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **New app** and select:
   - Repository: your repo
   - Branch: `main` (or your deployment branch)
   - Main file path: `app/main.py`
4. Open **Advanced settings** and add secrets:
   - `OPENAI_API_KEY = "your_key"`
   - Optional model settings from `.env.example`
5. Deploy. You will get a shareable URL like:
   - `https://your-app-name.streamlit.app`

## Option 2: Render (Docker Deploy)

1. Push this repo to GitHub (includes `Dockerfile` and `render.yaml`).
2. In Render, create a new **Blueprint** and select the repo.
3. Set `OPENAI_API_KEY` in environment variables.
4. Deploy and share the generated public URL.

## Option 3: Railway (Docker)

1. Create a new Railway project from your GitHub repo.
2. Railway detects `Dockerfile`.
3. Add `OPENAI_API_KEY` in Variables.
4. Deploy and share the generated domain.

## Local Docker Validation

```bash
docker build -t ieoh-agent .
docker run -p 8503:8501 -e OPENAI_API_KEY=your_key ieoh-agent
```

Then open `http://localhost:8503`.

## Production Notes

- The app stores data in `data/*.json` and `data/enterprise.db`.
- On most cloud free tiers, local container filesystem is ephemeral.
- For durable storage, move persistence to managed DB/object storage.
- Keep `OPENAI_API_KEY` only in platform secrets, never in git.
