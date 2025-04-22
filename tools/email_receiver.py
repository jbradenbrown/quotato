import random
import time
import textwrap
import sys
from typing import Dict, List, Optional
from scheduler import JobState, VendorJob
from langchain_core.output_parsers import JsonOutputParser

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI()

process_reply_template = PromptTemplate.from_template(textwrap.dedent("""
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


def get_manual_reply(job: VendorJob) -> str:
    """
    Prompt user to manually input a reply for a specific job
    """
    print(f"\n📧 Preparing reply for job: {job.vendor_name}")
    print(f"Service: {job.service}")
    print(f"Details: {job.details}")
    print("\nPlease type your reply (press Ctrl+D or Ctrl+Z when finished):")
    
    # Collect multi-line input
    lines = sys.stdin.readlines()
    response = ''.join(lines).strip()
    
    return response

def check_for_replies(job_queue):
    """
    Check for vendor replies, with option for manual input
    """
    waiting_jobs = job_queue.get_jobs_by_state(JobState.WAITING)
    
    if not waiting_jobs:
        print("No jobs currently waiting for replies.")
        return
    
    print("\n🔍 Jobs Waiting for Replies:")
    for i, job in enumerate(waiting_jobs, 1):
        print(f"{i}. {job.vendor_name} - {job.service}")
    
    try:
        choice = input("\nEnter the number of the job you want to reply to (or press Enter to skip): ")
        
        if choice.strip():
            job_index = int(choice) - 1
            if 0 <= job_index < len(waiting_jobs):
                selected_job = waiting_jobs[job_index]
                
                # Get manual reply from user
                manual_response = get_manual_reply(selected_job)
                
                if manual_response:
                    process_vendor_reply(selected_job, manual_response)
                else:
                    print("No reply entered. Skipping.")
            else:
                print("Invalid job selection.")
    except ValueError:
        print("Invalid input. Skipping manual reply.")
            
def process_vendor_reply(job: VendorJob, response: str):
    """Process a vendor reply"""
    try:
        chain = process_reply_template | llm | JsonOutputParser()
        response_json = chain.invoke({'body':response})
        
        if response_json["type"] == "quote":
            # Vendor provided a quote
            job.mark_complete({
                "amount": response_json.get("quote_amount"),
                "description": response_json.get("contents")
            })
            
        elif response_json["type"] == "needs_info":
            # Vendor needs more information
            job.needs_user_input(response_json.get("questions", []))
            
        elif response_json["type"] == "decline":
            # Vendor declined
            job.mark_failed(response_json.get("reason", "No specific reason given"))
        
        else:
            job.mark_failed("Unable to categorize response")
        
        return job
    
    except Exception as e:
        print(f"Error processing reply: {e}")
        job.mark_failed(f"Processing error: {str(e)}")
        return job
