# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from app.core.config import settings

# def send_test_email(receiver_email, subject, body):
#     if not settings.SENDER_EMAIL or not settings.APP_PASSWORD:
#         print("❌ Error: SENDER_EMAIL or APP_PASSWORD missing in .env")
#         return False

#     try:
#         message = MIMEMultipart()
#         message["From"] = settings.SENDER_EMAIL
#         message["To"] = receiver_email
#         message["Subject"] = subject
#         message.attach(MIMEText(body, "plain"))

#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
        
#         # Yahan settings se credentials uthaye ja rahe hain
#         server.login(settings.SENDER_EMAIL, settings.APP_PASSWORD)
#         server.send_message(message)
#         server.quit()
        
#         print(f"✅ SMTP Success: Sent to {receiver_email}")
#         return True
#     except Exception as e:
#         print(f"❌ SMTP Error Detail: {e}")
#         return False










import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

logger = logging.getLogger(__name__)

def send_test_email(receiver_email, subject, body):
    logger.info(f"Starting SMTP process to {receiver_email}")
    
    if not settings.SENDER_EMAIL or not settings.APP_PASSWORD:
        logger.error("SMTP Credentials missing in .env configuration!")
        return False

    try:
        message = MIMEMultipart()
        message["From"] = settings.SENDER_EMAIL
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        logger.info("Connecting to smtp.gmail.com...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        server.login(settings.SENDER_EMAIL, settings.APP_PASSWORD)
        logger.info("SMTP Login successful.")
        
        server.send_message(message)
        server.quit()
        
        logger.info(f"Email sent successfully to {receiver_email}")
        return True
    except Exception as e:
        logger.error(f"SMTP Error: {str(e)}")
        return False