# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # class Settings:
# #     GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# #     SENDER_EMAIL = os.getenv("SENDER_EMAIL")
# #     APP_PASSWORD = os.getenv("APP_PASSWORD")
# #     # Scopes ko wapis sirf readonly kar dein kyunke SMTP alag se kaam karega
# #     GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# # settings = Settings()








# import os
# import logging
# from dotenv import load_dotenv

# logger = logging.getLogger(__name__)
# load_dotenv()

# class Settings:
#     GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#     SENDER_EMAIL = os.getenv("SENDER_EMAIL")
#     APP_PASSWORD = os.getenv("APP_PASSWORD")
#     GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

#     def __init__(self):
#         # Validation logging
#         if not self.GROQ_API_KEY:
#             logger.error("GROQ_API_KEY is missing in .env file!")
#         else:
#             logger.info("GROQ_API_KEY loaded successfully.")

# settings = Settings()











import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    APP_PASSWORD = os.getenv("APP_PASSWORD")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

    def validate(self):
        missing = [k for k, v in self.__dict__.items() if not v and not k.startswith("__")]
        if missing:
            logger.error(f"Missing config: {missing}")
        else:
            logger.info("✅ All environment variables loaded.")

settings = Settings()
settings.validate()