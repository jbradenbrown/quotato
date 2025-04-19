import random
import time
from typing import Dict, List, Optional
from scheduler import JobState, VendorJob

# Mock responses for email simulation
MOCK_RESPONSES = [
    {
        "type": "quote",
        "content": "Thank you for your inquiry. We can replace your two windows for $850 total, including materials and labor. Let me know if you'd like to proceed.",
        "quote_amount": 850
    },
    {
        "type": "need_info",
        "content": "Thanks for reaching out. Could you please provide the dimensions of the windows that need replacement?",
        "question": "What are the dimensions of the windows?"
    },
    {
        "type": "decline",
        "content": "Unfortunately we're fully booked for the next 3 months and cannot take on new projects at this time.",
        "reason": "Vendor unavailable"
    }
]

def check_for_replies(job_queue):
    """
    Mock function to simulate email replies from vendors
    
    In a real implementation, this would check an email inbox
    """
    waiting_jobs = job_queue.get_jobs_by_state(JobState.WAITING)
    
    for job in waiting_jobs:
        # Simulate a 30% chance of getting a reply for each job that's waiting
        if random.random() < 0.3:
            # Choose a random response type
            mock_response = random.choice(MOCK_RESPONSES)
            process_vendor_reply(job, mock_response)
            
def process_vendor_reply(job: VendorJob, response: Dict):
    """Process a vendor reply (mock or real)"""
    response_type = response.get("type")
    
    if response_type == "quote":
        # Vendor provided a quote
        job.mark_complete({
            "amount": response.get("quote_amount"),
            "currency": "USD",
            "description": response.get("content")
        })
        
    elif response_type == "need_info":
        # Vendor needs more information
        job.needs_user_input(response.get("question"))
        
    elif response_type == "decline":
        # Vendor declined
        job.mark_failed(response.get("reason"))
        
    return job
