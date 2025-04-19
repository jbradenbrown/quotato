from tools.vendor_finder import get_mock_vendors
from tools.email_writer import generate_quote_email
from tools.email_sender import send_email
from tools.form_writer import generate_form_submission
from tools.report_generator import generate_report
from tools.email_receiver import check_for_replies
from scheduler import JobQueue, VendorJob, JobState
import os
import time
import random
from dotenv import load_dotenv

load_dotenv()

SERVICE = "window replacement"
CITY = "Seattle"
DETAILS = "We have two cracked windows in a single-family home."
USER_NAME = "Jeffrey Brown"
USER_EMAIL = "jeff@example.com"

def main():
    print(f"🥔 Quotato: Finding quotes for {SERVICE} in {CITY}")
    
    # Initialize job queue
    queue = JobQueue()
    
    # Find vendors
    vendors = get_mock_vendors(SERVICE, CITY)
    print(f"Found {len(vendors)} vendors")
    
    # Create jobs for each vendor
    for vendor in vendors:
        # Determine contact method
        contact_info = {}
        if "email" in vendor:
            contact_info = {"type": "email", "email": vendor["email"]}
        elif "contact_form_url" in vendor:
            contact_info = {"type": "form", "url": vendor["contact_form_url"]}
        else:
            contact_info = {"type": "unknown"}
        
        # Create job
        job = VendorJob(
            vendor_id=vendor.get("name", "unknown"),
            vendor_name=vendor["name"],
            service=SERVICE,
            details=DETAILS,
            contact_info=contact_info
        )
        
        # Add job to queue and process initial contact
        queue.add_job(job)
        process_initial_contact(job)
    
    # Simulation loop
    max_iterations = 10
    for iteration in range(max_iterations):
        print(f"\n--- Iteration {iteration + 1} ---")
        
        # Check for replies
        check_for_replies(queue)
        
        # Print current status
        print_job_status(queue)
        
        # Small delay between iterations
        time.sleep(1)
    
    # Generate final report
    generate_final_report(queue, vendors)

def process_initial_contact(job):
    """Send initial contact to vendor"""
    job.update_state(JobState.RUNNING, "Initiating contact")
    
    try:
        if job.contact_info["type"] == "email":
            # Prepare and send email
            body = generate_quote_email(job.service, job.details, CITY)
            send_email(
                to_email=job.contact_info["email"],
                subject=f"Quote request: {job.service} in {CITY}",
                body=body,
                from_email=USER_EMAIL,
                smtp_user=os.getenv("SMTP_USER"),
                smtp_pass=os.getenv("SMTP_PASS")
            )
            job.update_state(JobState.WAITING, "Email sent, awaiting reply")
        
        elif job.contact_info["type"] == "form":
            # Prepare form submission
            form_content = generate_form_submission(
                job.service, CITY, job.details, USER_NAME, USER_EMAIL
            )
            job.update_state(JobState.WAITING, "Form submission prepared")
        
        else:
            job.mark_failed("No contact method available")
    
    except Exception as e:
        job.mark_failed(f"Contact initiation failed: {str(e)}")

def print_job_status(queue):
    """Print detailed status of all jobs"""
    status_counts = queue.get_status_counts()
    
    print("Job Status:")
    for state, count in status_counts.items():
        print(f"  {state.capitalize()}: {count}")
    
    # Print details of jobs needing attention
    waiting_jobs = queue.get_jobs_by_state(JobState.WAITING)
    if waiting_jobs:
        print("\nWaiting Jobs:")
        for job in waiting_jobs:
            print(f"  {job.vendor_name}: Waiting for reply")
    
    input_jobs = queue.get_jobs_by_state(JobState.AWAITING_USER_INPUT)
    if input_jobs:
        print("\nJobs Needing User Input:")
        for job in input_jobs:
            print(f"  {job.vendor_name}: {job.user_input_needed}")

def generate_final_report(queue, vendors):
    """Generate comprehensive report of vendor interactions"""
    responses = {}
    
    # Combine active and completed jobs
    all_jobs = list(queue.active_jobs.values()) + list(queue.completed_jobs.values())
    
    for job in all_jobs:
        if job.state == JobState.COMPLETED:
            responses[job.vendor_name] = f"Quote received: ${job.result.get('amount', 'N/A')}"
        elif job.state == JobState.FAILED:
            responses[job.vendor_name] = f"Failed: {job.result.get('error', 'Unknown error')}"
        elif job.state == JobState.AWAITING_USER_INPUT:
            responses[job.vendor_name] = f"Needs info: {job.user_input_needed}"
        else:
            responses[job.vendor_name] = f"Status: {job.state}"
    
    # Generate and save report
    generate_report(vendors, responses)
    print("✅ Report generated and saved to report.md")

if __name__ == "__main__":
    main()
