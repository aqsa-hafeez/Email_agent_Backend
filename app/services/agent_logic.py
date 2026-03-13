# # # # from langchain_groq import ChatGroq
# # # # from app.core.config import settings
# # # # from app.services.gmail_service import fetch_unread_emails
# # # # import json

# # # # llm = ChatGroq(api_key=settings.GROQ_API_KEY, model="llama-3.3-70b-versatile")

# # # # def analyze_my_inbox():
# # # #     # fetch_unread_emails ab 'id' aur 'threadId' bhi return karta hai
# # # #     data = fetch_unread_emails(5) 
    
# # # #     if not data:
# # # #         return []
    
# # # #     # Prompt mein humne IDs ko shamil kiya hai taake LLM inhein retain kare
# # # #     prompt = f"""
# # # #     Analyze these emails: {data}.
# # # #     Return a JSON list where each object includes the original 'id' and 'threadId'.
    
# # # #     Categories: Urgent, Work, Personal, Newsletter.
    
# # # #     Format: {{
# # # #         "id": "original_id",
# # # #         "thread_id": "original_threadId",
# # # #         "subject": "...",
# # # #         "sender": "...",
# # # #         "category": "...",
# # # #         "summary": "...",
# # # #         "action_item": "..."
# # # #     }}
# # # #     Strictly return ONLY JSON.
# # # #     """
    
# # # #     response = llm.invoke(prompt)
    
# # # #     try:
# # # #         # Markdown clean-up logic
# # # #         content = response.content.replace('```json', '').replace('```', '').strip()
# # # #         parsed_data = json.loads(content)
# # # #         return parsed_data
# # # #     except Exception as e:
# # # #         return {"error": "Failed to parse LLM response", "details": str(e), "raw": response.content}














# # # # import logging
# # # # import json
# # # # import re  # Regular expression use karenge JSON nikalne ke liye
# # # # from langchain_groq import ChatGroq
# # # # from app.core.config import settings
# # # # from app.services.gmail_service import fetch_unread_emails

# # # # logger = logging.getLogger(__name__)
# # # # llm = ChatGroq(api_key=settings.GROQ_API_KEY, model="llama-3.3-70b-versatile")

# # # # def analyze_my_inbox():
# # # #     logger.info("Agent starting inbox analysis...")
# # # #     data = fetch_unread_emails(5) 
    
# # # #     if not data:
# # # #         logger.warning("No unread emails found.")
# # # #         return []
    
# # # #     # System prompt ko mazeed strong banaya hai
# # # #     prompt = f"""
# # # #     You are a professional email analyzer. Analyze these emails: {data}.
    
# # # #     STRICT RULE: Return ONLY a valid JSON list. Do not include any conversational text, explanations, or markdown code blocks like ```json.
    
# # # #     Each object in the list MUST have:
# # # #     - "id": (string)
# # # #     - "thread_id": (string)
# # # #     - "subject": (string)
# # # #     - "sender": (string)
# # # #     - "category": (Urgent, Work, Personal, or Newsletter)
# # # #     - "summary": (short 1-sentence summary)
# # # #     - "action_item": (short suggestion)

# # # #     Example Format:
# # # #     [
# # # #         {{"id": "123", "thread_id": "456", "subject": "Hi", "sender": "test@test.com", "category": "Work", "summary": "Greetings", "action_item": "Reply"}}
# # # #     ]
# # # #     """
    
# # # #     try:
# # # #         response = llm.invoke(prompt)
# # # #         content = response.content.strip()
        
# # # #         logger.info(f"Raw LLM Response: {content[:100]}...") # Pehle 100 characters log karein

# # # #         # Regex use karein agar LLM ne ```json ... ``` ke andar wrap kiya ho
# # # #         json_match = re.search(r'\[\s*\{.*\}\s*\]', content, re.DOTALL)
# # # #         if json_match:
# # # #             clean_content = json_match.group(0)
# # # #         else:
# # # #             clean_content = content.replace('```json', '').replace('```', '').strip()

# # # #         parsed_data = json.loads(clean_content)
# # # #         logger.info("AI analysis and JSON parsing successful.")
# # # #         return parsed_data

# # # #     except Exception as e:
# # # #         logger.error(f"Parsing Failed! Raw content was: {content}")
# # # #         logger.error(f"Error Detail: {str(e)}")
# # # #         # Error aane par empty list return karein taake frontend crash na ho
# # # #         return []




# # # import logging
# # # import json
# # # from supabase import create_client, Client
# # # from app.core.config import settings
# # # from app.services.gmail_service import fetch_unread_emails
# # # from langchain_groq import ChatGroq

# # # logger = logging.getLogger(__name__)
# # # supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
# # # llm = ChatGroq(api_key=settings.GROQ_API_KEY, model="llama-3.3-70b-versatile")

# # # def sync_and_generate_drafts():
# # #     # Step 1: Gmail se nayi emails lao aur Supabase mein save karo
# # #     raw_emails = fetch_unread_emails(10)
# # #     for mail in raw_emails:
# # #         supabase.table("emails").upsert({
# # #             "id": mail["id"],
# # #             "thread_id": mail["threadId"],
# # #             "subject": mail["subject"],
# # #             "sender": mail["sender"],
# # #             "snippet": mail["snippet"]
# # #         }).execute()
    
# # #     # Step 2: Supabase se wo emails uthao jin ka AI response abhi tak nahi bana
# # #     records = supabase.table("emails").select("*").eq("is_processed", False).execute()
    
# # #     for record in records.data:
# # #         logger.info(f"Generating draft for email: {record['subject']}")
        
# # #         prompt = f"Write a professional reply to this email: {record['snippet']}. Return ONLY the reply text."
# # #         response = llm.invoke(prompt)
        
# # #         # Step 3: Response ko Supabase mein save karo
# # #         supabase.table("emails").update({
# # #             "ai_draft": response.content,
# # #             "is_processed": True
# # #         }).eq("id", record["id"]).execute()

# # #     return {"status": "success", "message": "Drafts generated and stored."}




















# # import logging
# # import json
# # from supabase import create_client, Client
# # from langchain_groq import ChatGroq
# # from app.core.config import settings
# # from app.services.gmail_service import fetch_unread_emails

# # logger = logging.getLogger(__name__)
# # supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
# # llm = ChatGroq(api_key=settings.GROQ_API_KEY, model="llama-3.3-70b-versatile")

# # def sync_and_generate_drafts():
# #     # 1. Store in Supabase
# #     emails = fetch_unread_emails(5)
# #     for mail in emails:
# #         supabase.table("emails").upsert({
# #             "id": mail["id"],
# #             "thread_id": mail["threadId"],
# #             "subject": mail["subject"],
# #             "sender": mail["sender"],
# #             "snippet": mail["snippet"]
# #         }).execute()

# #     # 2. Get emails without drafts
# #     records = supabase.table("emails").select("*").eq("is_processed", False).execute()
    
# #     for record in records.data:
# #         prompt = f"Write a 1-sentence professional reply to: {record['snippet']}. Return ONLY the reply."
# #         response = llm.invoke(prompt)
        
# #         # 3. Store response
# #         supabase.table("emails").update({
# #             "ai_draft": response.content,
# #             "is_processed": True
# #         }).eq("id", record["id"]).execute()
# #         logger.info(f"Draft generated for: {record['id']}")

# #     return records.data

















# import logging
# import json
# from supabase import create_client, Client
# from langchain_groq import ChatGroq
# from app.core.config import settings
# from app.services.gmail_service import fetch_unread_emails

# logger = logging.getLogger(__name__)

# # Initialize Supabase and LLM
# supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
# llm = ChatGroq(api_key=settings.GROQ_API_KEY, model="llama-3.3-70b-versatile")

# def sync_and_generate_drafts():
#     # 1. Gmail se nayi emails fetch karein aur Supabase mein save karein
#     logger.info("Fetching new emails from Gmail...")
#     raw_emails = fetch_unread_emails(5)
    
#     for mail in raw_emails:
#         supabase.table("emails").upsert({
#             "id": mail["id"],
#             "thread_id": mail["threadId"],
#             "subject": mail["subject"],
#             "sender": mail["sender"],
#             "snippet": mail["snippet"]
#         }).execute()
    
#     # 2. Database se wo emails uthao jo abhi tak process nahi huin (is_processed = False)
#     logger.info("Checking database for unprocessed emails...")
#     records = supabase.table("emails").select("*").eq("is_processed", False).execute()
    
#     if not records.data:
#         logger.info("No new emails to process.")
#         return []

#     processed_results = []
    
#     for record in records.data:
#         logger.info(f"LLM is analyzing email: {record['subject']}")
        
#         # LLM Prompt: Hum category aur draft dono ek saath mangwayenge
#         prompt = f"""
#         You are an AI Email Assistant. Analyze the following email:
#         Subject: {record['subject']}
#         From: {record['sender']}
#         Content: {record['snippet']}

#         Tasks:
#         1. Categorize it (Urgent, Work, Personal, or Newsletter).
#         2. Write a professional and concise 1-sentence reply draft.
#         3. Write a 1-sentence summary of the email.

#         Return ONLY a JSON object in this format:
#         {{
#             "category": "...",
#             "summary": "...",
#             "ai_draft": "..."
#         }}
#         """
        
#         try:
#             response = llm.invoke(prompt)
#             # JSON clean-up logic
#             content = response.content.replace('```json', '').replace('```', '').strip()
#             ai_data = json.loads(content)

#             # 3. AI ka response wapis Supabase mein save karein
#             supabase.table("emails").update({
#                 "category": ai_data.get("category"),
#                 "summary": ai_data.get("summary"),
#                 "ai_draft": ai_data.get("ai_draft"),
#                 "is_processed": True
#             }).eq("id", record["id"]).execute()
            
#             logger.info(f"✅ Draft and category stored for: {record['subject']}")
#             processed_results.append(ai_data)

#         except Exception as e:
#             logger.error(f"❌ LLM Processing Error for {record['id']}: {str(e)}")

#     # Final processed data wapis bhejein (Ab null nahi hoga!)
#     final_data = supabase.table("emails").select("*").order("created_at", desc=True).limit(5).execute()
#     return final_data.data












import logging
import json
import os
from supabase import create_client, Client
from langchain_groq import ChatGroq
from app.core.config import settings
from app.services.gmail_service import fetch_unread_emails

# Logger setup
logger = logging.getLogger(__name__)

# Initialize Supabase and LLM
# Ensure these are in your settings/config or .env
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
llm = ChatGroq(api_key=settings.GROQ_API_KEY, model="llama-3.3-70b-versatile")

def sync_and_generate_drafts():
    """
    1. Fetches unread emails from Gmail.
    2. Syncs them with Supabase.
    3. Uses LLM to generate drafts for unprocessed emails.
    4. Returns the latest emails with their AI analysis.
    """
    try:
        # STEP 1: Fetch new emails from Gmail
        logger.info("Step 1: Fetching unread emails from Gmail...")
        raw_emails = fetch_unread_emails(5)
        
        if raw_emails:
            for mail in raw_emails:
                # Upsert ensures we don't create duplicates based on 'id'
                supabase.table("emails").upsert({
                    "id": mail["id"],
                    "thread_id": mail["threadId"],
                    "subject": mail["subject"],
                    "sender": mail["sender"],
                    "snippet": mail["snippet"]
                }).execute()
            logger.info(f"Successfully synced {len(raw_emails)} emails to Supabase.")
        else:
            logger.info("No new unread emails found in Gmail.")

        # STEP 2: Find emails in DB that haven't been processed by AI yet
        logger.info("Step 2: Checking for unprocessed emails in DB...")
        records = supabase.table("emails").select("*").eq("is_processed", False).execute()
        
        if not records.data:
            logger.info("No unprocessed emails found. Moving to return latest data.")
        else:
            # STEP 3: Generate AI analysis for each unprocessed email
            for record in records.data:
                logger.info(f"AI analyzing email: {record['subject']}")
                
                prompt = f"""
                You are a professional AI Email Assistant. Analyze this email:
                Subject: {record['subject']}
                From: {record['sender']}
                Content: {record['snippet']}

                Tasks:
                1. Categorize it (Urgent, Work, Personal, or Newsletter).
                2. Write a professional, concise 1-sentence reply draft.
                3. Write a 1-sentence summary.

                Return ONLY a JSON object:
                {{
                    "category": "...",
                    "summary": "...",
                    "ai_draft": "..."
                }}
                """
                
                try:
                    response = llm.invoke(prompt)
                    # Clean the response to ensure valid JSON
                    clean_content = response.content.replace('```json', '').replace('```', '').strip()
                    ai_data = json.loads(clean_content)

                    # Update the record in Supabase
                    supabase.table("emails").update({
                        "category": ai_data.get("category"),
                        "summary": ai_data.get("summary"),
                        "ai_draft": ai_data.get("ai_draft"),
                        "is_processed": True
                    }).eq("id", record["id"]).execute()
                    
                    logger.info(f"✅ AI analysis stored for: {record['subject']}")
                
                except Exception as ai_err:
                    logger.error(f"❌ Error during LLM generation for {record['id']}: {ai_err}")

        # STEP 4: Always return the latest 5 emails (processed or not)
        # This prevents empty responses in Swagger/Lovable
        logger.info("Step 3: Fetching latest records to return...")
        final_data = supabase.table("emails")\
            .select("*")\
            .order("created_at", desc=True)\
            .limit(5)\
            .execute()
            
        return final_data.data

    except Exception as e:
        logger.error(f"Critical Error in sync_and_generate_drafts: {str(e)}")
        return []