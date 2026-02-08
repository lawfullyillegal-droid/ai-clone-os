#!/usr/bin/env python3
"""
Tests for the ENS Legis Interactive Dashboard
"""

import os
import sys
import json
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard import app


class TestDashboardAPI(unittest.TestCase):
    """Test dashboard API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_dashboard_index(self):
        """Test main dashboard page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ENS Legis AI Clone OS', response.data)
    
    def test_status_endpoint(self):
        """Test status API endpoint"""
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('bot_state', data)
        self.assertIn('timestamp', data)
        
        # Check bot_state structure
        bot_state = data['bot_state']
        self.assertIn('running', bot_state)
        self.assertIn('status', bot_state)
        self.assertIn('processed_count', bot_state)
        self.assertIn('error_count', bot_state)
    
    def test_logs_endpoint(self):
        """Test logs API endpoint"""
        response = self.client.get('/api/logs')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('logs', data)
        self.assertIn('total', data)
        self.assertIsInstance(data['logs'], list)
        self.assertIsInstance(data['total'], int)
    
    def test_logs_with_filters(self):
        """Test logs endpoint with filters"""
        response = self.client.get('/api/logs?category=Legal&limit=10')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('logs', data)
    
    def test_statistics_endpoint(self):
        """Test statistics API endpoint"""
        response = self.client.get('/api/statistics')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('total', data)
        self.assertIn('by_category', data)
        self.assertIn('by_date', data)
        self.assertIn('recent_activity', data)
    
    def test_config_get(self):
        """Test config GET endpoint"""
        response = self.client.get('/api/config')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
    
    def test_bot_stop_when_not_running(self):
        """Test stopping bot when it's not running"""
        response = self.client.post('/api/bot/stop')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
