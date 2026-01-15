#!/usr/bin/env python3
"""
ENS Legis Email Bot
Automated email categorization, response, and surveillance logging

Part of AI Clone OS - Incrimination Nation Campaign
Author: Travis Ryle (Principal)
Operator: ENS Legis (Digital Clone)
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Get the absolute path to the repository root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuration - use absolute paths
CONFIG_PATH = os.path.join(REPO_ROOT, "config", "email_config.json")
TEMPLATES_PATH = os.path.join(REPO_ROOT, "templates", "email")
SURVEILLANCE_LOG_PATH = os.path.join(REPO_ROOT, "data", "surveillance_log.json")
MEDIA_LIST_PATH = os.path.join(REPO_ROOT, "config", "media_list.csv")

# Email categories
CATEGORY_LEGAL = "Legal"
CATEGORY_MEDIA = "Media"
CATEGORY_SUPPORTER = "Supporter"
CATEGORY_VENDOR = "Vendor"
CATEGORY_SPAM = "Spam"
CATEGORY_UNKNOWN = "Unknown"


class EmailBot:
    """ENS Legis Email Automation Bot"""
    
    def __init__(self, credentials_path: str):
        """Initialize email bot with Gmail API credentials"""
        self.creds = self._load_credentials(credentials_path)
        self.service = None
        if self.creds:
            self.service = build('gmail', 'v1', credentials=self.creds)
        self.config = self._load_config()
        self.media_domains = self._load_media_list()
        
    def _load_credentials(self, path: str) -> Optional[Credentials]:
        """Load Gmail API credentials"""
        # Check if credentials file exists
        if not os.path.exists(path):
            print(f"Warning: Credentials file not found at {path}")
            print("Gmail API functionality will be disabled.")
            print("To enable, follow setup instructions in README.md")
            return None
        
        # TODO: Implement OAuth2 credential loading
        # This requires setting up Google Cloud Project and OAuth consent screen
        # For now, return None to allow bot to initialize without crashing
        print(f"Note: Credential loading not yet implemented for {path}")
        return None
    
    def _load_config(self) -> Dict:
        """Load email bot configuration"""
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_media_list(self) -> List[str]:
        """Load list of known media outlet domains"""
        if os.path.exists(MEDIA_LIST_PATH):
            with open(MEDIA_LIST_PATH, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        return []
    
    def categorize_email(self, email: Dict) -> str:
        """Categorize email based on subject, sender, and content
        
        Rules per ENS Legis Master Prompt:
        - FCRA/credit report keywords → Legal
        - Media outlet domains → Media  
        - Patreon/support keywords → Supporter
        - Everything else → analyze further or mark Unknown
        """
        subject = email.get('subject', '').lower()
        sender = email.get('from', '').lower()
        
        # Legal category triggers
        legal_keywords = ['fcra', 'credit report', 'dispute', 'violation', 
                         'litigation', 'complaint', 'legal', 'attorney']
        if any(keyword in subject for keyword in legal_keywords):
            return CATEGORY_LEGAL
        
        # Media category - check sender domain
        sender_domain = sender.split('@')[-1] if '@' in sender else ''
        if any(media_domain in sender_domain for media_domain in self.media_domains):
            return CATEGORY_MEDIA
        
        # Supporter category triggers
        supporter_keywords = ['patreon', 'subscribe', 'support', 'donation', 'contribute']
        if any(keyword in subject for keyword in supporter_keywords):
            return CATEGORY_SUPPORTER
        
        # Vendor category
        vendor_keywords = ['invoice', 'payment', 'printful', 'stripe', 'billing']
        if any(keyword in subject for keyword in vendor_keywords):
            return CATEGORY_VENDOR
        
        return CATEGORY_UNKNOWN
    
    def get_template(self, template_name: str) -> Optional[str]:
        """Load email response template"""
        template_path = os.path.join(TEMPLATES_PATH, f"{template_name}.txt")
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                return f.read()
        return None
    
    def send_auto_response(self, email: Dict, category: str) -> bool:
        """Send automated response based on category
        
        Per ENS Legis Master Prompt:
        - Legal → FCRA-Initial-Guidance template
        - Media → Media-Inquiry-Response template
        - Supporter → Thank-You-Patron template
        """
        template_map = {
            CATEGORY_LEGAL: "FCRA-Initial-Guidance",
            CATEGORY_MEDIA: "Media-Inquiry-Response",
            CATEGORY_SUPPORTER: "Thank-You-Patron"
        }
        
        template_name = template_map.get(category)
        if not template_name:
            return False
        
        template_content = self.get_template(template_name)
        if not template_content:
            print(f"Warning: Template {template_name} not found")
            return False
        
        # TODO: Implement actual email sending via Gmail API
        # For now, log the intended action
        self.log_action({
            'action': 'auto_response',
            'category': category,
            'template': template_name,
            'recipient': email.get('from'),
            'subject_original': email.get('subject')
        })
        
        return True
    
    def log_to_surveillance(self, email: Dict, category: str, action_taken: str):
        """Log email to surveillance database
        
        All inbound inquiries must be logged per ENS Legis protocol
        """
        log_entry = {
            'incident_id': self._generate_incident_id(),
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'source': 'email',
            'event_type': 'inbound_email',
            'category': category,
            'details': {
                'from': email.get('from'),
                'subject': email.get('subject'),
                'message_id': email.get('id'),
                'action_taken': action_taken
            },
            'evidence_hash': self._hash_email(email)
        }
        
        # Append to surveillance log
        self._append_to_log(log_entry)
    
    def _generate_incident_id(self) -> str:
        """Generate unique incident ID in format SL-YYYY-MMDD-NNN"""
        now = datetime.utcnow()
        date_str = now.strftime("%Y-%m%d")
        # In production, this would query existing logs to get next sequence number
        seq = "001"
        return f"SL-{date_str}-{seq}"
    
    def _hash_email(self, email: Dict) -> str:
        """Generate SHA-256 hash of email for chain of custody"""
        email_str = json.dumps(email, sort_keys=True)
        return hashlib.sha256(email_str.encode()).hexdigest()[:12]
    
    def _append_to_log(self, entry: Dict):
        """Append entry to surveillance log file"""
        # Ensure the directory exists
        log_dir = os.path.dirname(SURVEILLANCE_LOG_PATH)
        os.makedirs(log_dir, exist_ok=True)
        
        log_data = []
        if os.path.exists(SURVEILLANCE_LOG_PATH):
            with open(SURVEILLANCE_LOG_PATH, 'r') as f:
                log_data = json.load(f)
        
        log_data.append(entry)
        
        with open(SURVEILLANCE_LOG_PATH, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def log_action(self, action: Dict):
        """Log bot action for audit trail"""
        action['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        action['operator'] = 'ENS_Legis_Email_Bot'
        print(json.dumps(action, indent=2))
    
    def process_inbox(self, max_results: int = 10):
        """Process unread emails in inbox
        
        Main workflow:
        1. Fetch unread emails
        2. Categorize each email
        3. Send auto-response if applicable
        4. Log to surveillance database
        5. Mark as processed
        """
        if not self.service:
            print("Error: Gmail API service not initialized. Cannot process inbox.")
            print("Please set up credentials following the instructions in README.md")
            return
        
        try:
            # Query for unread emails
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print('No unread emails found.')
                return
            
            for msg in messages:
                # Get full message details
                message = self.service.users().messages().get(
                    userId='me',
                    id=msg['id']
                ).execute()
                
                email_data = self._parse_email(message)
                category = self.categorize_email(email_data)
                
                # Process based on category
                if category in [CATEGORY_LEGAL, CATEGORY_MEDIA, CATEGORY_SUPPORTER]:
                    self.send_auto_response(email_data, category)
                    action_taken = f"auto_response_sent: {category}"
                else:
                    action_taken = f"categorized_only: {category}"
                
                # Log to surveillance database
                self.log_to_surveillance(email_data, category, action_taken)
                
                # Mark as read/processed
                self.service.users().messages().modify(
                    userId='me',
                    id=msg['id'],
                    body={'removeLabelIds': ['UNREAD']}
                ).execute()
                
                print(f"Processed: {email_data.get('subject')} - Category: {category}")
                
        except HttpError as error:
            print(f'An error occurred: {error}')
    
    def _parse_email(self, message: Dict) -> Dict:
        """Parse Gmail message into simplified email dictionary"""
        headers = message.get('payload', {}).get('headers', [])
        
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        from_addr = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        
        return {
            'id': message['id'],
            'subject': subject,
            'from': from_addr,
            'threadId': message.get('threadId'),
            'snippet': message.get('snippet', '')
        }


def main():
    """Main entry point for email bot"""
    print("ENS Legis Email Bot - Initializing...")
    
    # In production, load credentials from secure location
    credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
    
    bot = EmailBot(credentials_path)
    
    # Process inbox
    print("Processing inbox...")
    bot.process_inbox(max_results=50)
    
    print("Email bot processing complete.")


if __name__ == "__main__":
    main()
