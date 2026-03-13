import os.path
import base64
import logging
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from app.core.config import settings

logger = logging.getLogger(__name__)

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', settings.GMAIL_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', settings.GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def fetch_unread_emails(limit=10):
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', q="is:unread", maxResults=limit).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            m = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = m['payload']['headers']
            emails.append({
                "id": msg['id'],
                "threadId": m.get('threadId'),
                "subject": next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject"),
                "sender": next((h['value'] for h in headers if h['name'] == 'From'), "Unknown"),
                "snippet": m.get('snippet')
            })
        return emails
    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        return []

# Ye wo function hai jiski wajah se error aa raha tha
def fetch_and_process_emails():
    """Fetches unread emails to be processed by AI in the routes"""
    logger.info("Orchestrating email fetch...")
    return fetch_unread_emails(limit=5)

def send_gmail_reply(to_email, subject, body, thread_id):
    try:
        service = get_gmail_service()
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = f"Re: {subject}"
        message['In-Reply-To'] = thread_id
        message['References'] = thread_id
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': raw, 'threadId': thread_id}).execute()
        return True
    except Exception as e:
        logger.error(f"Gmail Send Error: {e}")
        return False