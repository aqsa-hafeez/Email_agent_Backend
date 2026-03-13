# ⚙️ Smart AI Email Agent - Backend (API)

The core engine of the Email Agent, powered by **FastAPI**. It handles Gmail OAuth2 authentication, email processing, and AI response generation.

## 🧠 Core Logic
- **Gmail Integration:** Uses Google Python API to fetch and send messages.
- **AI Engine:** Leverages **Groq (LLaMA-3)** for high-speed, professional email drafting.
- **Database:** Uses **Supabase** (PostgreSQL) to manage email state and avoid duplicate processing.
- **Deployment:** Optimized for Docker and Hugging Face Spaces.

## 🛠️ Tech Stack
- **Language:** Python 3.11
- **Framework:** FastAPI
- **Database:** Supabase
- **AI Inference:** Groq SDK
- **Task Scheduling:** Long-polling/Auto-sync compatible.

## 🚀 Setup & Environment

1. **Install Requirements:**
   ```bash
   pip install -r requirements.txt



2. **Environment Variables (.env):**
Create a `.env` file with the following:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GROQ_API_KEY=your_groq_key
GMAIL_CREDENTIALS_JSON=your_credentials_string
GMAIL_TOKEN_JSON=your_token_string

```


3. **Run the API:**
```bash
python main.py

```



## 🐳 Docker Deployment

```bash
docker build -t email-agent-backend .
docker run -p 7860:7860 email-agent-backend

```
