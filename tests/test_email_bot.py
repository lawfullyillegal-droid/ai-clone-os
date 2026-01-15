#!/usr/bin/env python3
"""
Tests for ENS Legis Email Bot

Part of AI Clone OS - Incrimination Nation Campaign
"""

import pytest
from bots.email_bot import EmailBot, CATEGORY_LEGAL, CATEGORY_MEDIA, CATEGORY_SUPPORTER, CATEGORY_VENDOR, CATEGORY_UNKNOWN


class TestEmailBot:
    """Test suite for EmailBot functionality"""
    
    def test_bot_initialization_without_credentials(self):
        """Test that bot can initialize without crashing when credentials are missing"""
        bot = EmailBot("nonexistent_credentials.json")
        assert bot is not None
        assert bot.service is None  # Service should be None without credentials
        assert bot.config is not None
        assert bot.media_domains is not None
    
    def test_categorize_legal_email(self):
        """Test categorization of legal-related emails"""
        bot = EmailBot("nonexistent_credentials.json")
        
        email = {
            'subject': 'FCRA Violation Inquiry',
            'from': 'user@example.com'
        }
        category = bot.categorize_email(email)
        assert category == CATEGORY_LEGAL
        
        email = {
            'subject': 'Credit report dispute',
            'from': 'user@example.com'
        }
        category = bot.categorize_email(email)
        assert category == CATEGORY_LEGAL
    
    def test_categorize_supporter_email(self):
        """Test categorization of supporter emails"""
        bot = EmailBot("nonexistent_credentials.json")
        
        email = {
            'subject': 'Patreon subscription',
            'from': 'supporter@example.com'
        }
        category = bot.categorize_email(email)
        assert category == CATEGORY_SUPPORTER
        
        email = {
            'subject': 'I want to support your campaign',
            'from': 'supporter@example.com'
        }
        category = bot.categorize_email(email)
        assert category == CATEGORY_SUPPORTER
    
    def test_categorize_vendor_email(self):
        """Test categorization of vendor emails"""
        bot = EmailBot("nonexistent_credentials.json")
        
        email = {
            'subject': 'Invoice for services',
            'from': 'billing@vendor.com'
        }
        category = bot.categorize_email(email)
        assert category == CATEGORY_VENDOR
    
    def test_categorize_unknown_email(self):
        """Test categorization of unknown emails"""
        bot = EmailBot("nonexistent_credentials.json")
        
        email = {
            'subject': 'Random subject',
            'from': 'unknown@example.com'
        }
        category = bot.categorize_email(email)
        assert category == CATEGORY_UNKNOWN
    
    def test_process_inbox_without_credentials(self):
        """Test that process_inbox handles missing credentials gracefully"""
        bot = EmailBot("nonexistent_credentials.json")
        # Should not crash
        bot.process_inbox()
    
    def test_get_template_nonexistent(self):
        """Test getting a non-existent template"""
        bot = EmailBot("nonexistent_credentials.json")
        template = bot.get_template("NonexistentTemplate")
        assert template is None
