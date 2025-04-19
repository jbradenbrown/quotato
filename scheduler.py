import json
import os
from datetime import datetime
import time
from typing import Dict, List, Any, Optional

# Simple string constants for job states
class JobState:
    PENDING = "pending"
    RUNNING = "running"
    WAITING = "waiting_for_reply"
    AWAITING_USER_INPUT = "awaiting_user_input"
    COMPLETED = "completed"
    FAILED = "failed"

class VendorJob:
    """Simple job class for tracking vendor interactions"""
    
    def __init__(self, vendor_id: str, vendor_name: str, service: str, details: str, contact_info: Dict):
        self.vendor_id = vendor_id
        self.vendor_name = vendor_name
        self.service = service
        self.details = details
        self.contact_info = contact_info  # Email, form URL, etc.
        self.state = JobState.PENDING
        self.history = []  # Simple list to track state changes
        self.result = None  # Will store quote or failure reason
        self.user_input_needed = None  # Question for user if needed
        
    def update_state(self, new_state: str, message: str = None):
        """Update job state with optional message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.state = new_state
        
        if message:
            entry = {"timestamp": timestamp, "state": new_state, "message": message}
            self.history.append(entry)
            
    def needs_user_input(self, question: str):
        """Mark this job as needing user input"""
        self.user_input_needed = question
        self.update_state(JobState.AWAITING_USER_INPUT, f"Needs input: {question}")
    
    def add_user_response(self, answer: str):
        """Add user's response to a question"""
        if self.user_input_needed:
            self.update_state(JobState.RUNNING, f"User provided: {answer}")
            self.user_input_needed = None
            return True
        return False
    
    def mark_complete(self, quote_info: Dict):
        """Mark job as complete with quote information"""
        self.result = quote_info
        self.update_state(JobState.COMPLETED, f"Quote received: {quote_info}")
    
    def mark_failed(self, reason: str):
        """Mark job as failed with reason"""
        self.result = {"error": reason}
        self.update_state(JobState.FAILED, reason)

class JobQueue:
    """Simple queue to manage vendor jobs"""
    
    def __init__(self):
        self.active_jobs = {}  # Dict of vendor_id -> VendorJob
        self.completed_jobs = {}  # Completed or failed jobs
    
    def add_job(self, job: VendorJob):
        """Add a job to the queue"""
        self.active_jobs[job.vendor_id] = job
    
    def get_job(self, vendor_id: str) -> Optional[VendorJob]:
        """Get a job by vendor ID"""
        return self.active_jobs.get(vendor_id) or self.completed_jobs.get(vendor_id)
    
    def get_jobs_by_state(self, state: str) -> List[VendorJob]:
        """Get all jobs in a particular state"""
        return [job for job in self.active_jobs.values() if job.state == state]
    
    def get_all_active_jobs(self) -> List[VendorJob]:
        """Get all active jobs"""
        return list(self.active_jobs.values())
    
    def complete_job(self, vendor_id: str):
        """Move job from active to completed"""
        if vendor_id in self.active_jobs:
            job = self.active_jobs.pop(vendor_id)
            self.completed_jobs[vendor_id] = job
    
    def get_status_counts(self) -> Dict[str, int]:
        """Get counts of jobs by state"""
        counts = {
            JobState.PENDING: 0,
            JobState.RUNNING: 0,
            JobState.WAITING: 0,
            JobState.AWAITING_USER_INPUT: 0,
            JobState.COMPLETED: 0,
            JobState.FAILED: 0
        }
        
        # Count active jobs
        for job in self.active_jobs.values():
            counts[job.state] += 1
            
        # Count completed/failed jobs
        for job in self.completed_jobs.values():
            counts[job.state] += 1
            
        return counts
