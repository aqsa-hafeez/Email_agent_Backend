import asyncio
from fastapi import APIRouter, HTTPException, Body
from app.services.gmail_service import fetch_and_process_emails, send_gmail_reply
from app.database.supabase_client import supabase 

router = APIRouter()

@router.get("/process")
async def process_inbox():
    """Gmail se emails fetch karna, Supabase mein save karna aur front-end ko data bhejna"""
    raw_emails = fetch_and_process_emails()
    
    for email in raw_emails:
        # Check if email already exists in database
        existing = supabase.table("emails").select("*").eq("id", email['id']).execute()
        
        if not existing.data:
            # Yahan placeholder draft ban raha hai
            ai_draft = f"Hello,\n\nI've received your email regarding '{email['subject']}'. I am looking into it and will get back to you soon.\n\nBest regards,\nAqsa's Assistant"
            
            new_entry = {
                "id": email['id'],
                "thread_id": email['threadId'],
                "subject": email['subject'],
                "sender": email['sender'],
                "snippet": email['snippet'],
                "ai_draft": ai_draft,
                "is_sent": False
            }
            supabase.table("emails").insert(new_entry).execute()
    
    # Fresh data return karna backend se
    res = supabase.table("emails").select("*").order("created_at", desc=True).execute()
    return {"status": "success", "data": res.data}

@router.post("/approve-and-send")
async def approve_and_send(payload: dict = Body(...)):
    email_id = payload.get("email_id")
    res = supabase.table("emails").select("*").eq("id", email_id).execute()
    
    if not res.data:
        raise HTTPException(status_code=404, detail="Email record not found")
    
    email_entry = res.data[0]
    
    # Gmail API ke zariye reply bhejna
    success = send_gmail_reply(
        to_email=email_entry.get('sender'),
        subject=email_entry.get('subject'),
        body=email_entry.get('ai_draft'),
        thread_id=email_entry.get('thread_id')
    )
    
    if success:
        supabase.table("emails").update({"is_sent": True}).eq("id", email_id).execute()
        return {"status": "success", "message": "Email sent successfully"}
    
    raise HTTPException(status_code=500, detail="Failed to send email")