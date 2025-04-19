import random
import time
from typing import Dict, List, Optional
from scheduler import JobState, VendorJob
from langchain.output_parsers import JsonOutputParser

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI()

# Mock responses for email simulation
MOCK_RESPONSES = [
  "Thank you for your inquiry. We can replace your two windows for $850 total, including materials and labor. Let me know if you'd like to proceed.",
  "Thanks for reaching out. Could you please provide the dimensions of the windows that need replacement?",
  "Unfortunately we're fully booked for the next 3 months and cannot take on new projects at this time."
]

process_reply_template = PromptTemplate.from_template(textwrap.dedent(f"""
    This is an email from a potential service provider. I have 3 buckets: quote, needs_info, and decline.
    I need to know which bucket this email belongs in. If it is a quote, it must have a price or price range.
    If it needs_input, then it likely contains a question. If it suggests that the work cannot be done by them,
    then it is failed.
                                                                      
    Please return a json which contains a "type".
    If the reply is a quote, it must include a "quote amount", which should be a float.
    If the reply is a needs_info, it must include "questions", a list of questions ([str]).
    If the reply is a decline, it must include "reason", a reason given for being declined, if no reason is given, state so.
    The message body should be in a "contents".
                                                                      
    {body}
"""))


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
            
def process_vendor_reply(job: VendorJob, response: str):
    """Process a vendor reply (mock or real)"""

    chain = process_reply_template.format(body = response) | llm | JsonOutputParser

    response_json = chain.invoke()
    
    if response_json.type == "quote":
        # Vendor provided a quote
        job.mark_complete({
            "amount": response.get("quote_amount"),
            "description": response.get("content")
        })
        
    elif response_json.type == "need_info":
        # Vendor needs more information
        job.needs_user_input(response.get("questions"))
        
    elif response_json.type == "decline":
        # Vendor declined
        job.mark_failed(response.get("reason"))
        
    return job
