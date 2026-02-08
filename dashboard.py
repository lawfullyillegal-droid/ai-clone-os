#!/usr/bin/env python3
"""
ENS Legis Interactive Dashboard
Web-based control panel for AI Clone OS operations

Features:
- Bot status monitoring and control
- Surveillance log viewer with real-time updates
- Email categorization statistics
- Manual email processing interface
- System configuration management
"""

import os
import json
import threading
import time
from datetime import datetime, timezone
from flask import Flask, render_template, jsonify, request, send_from_directory
from pathlib import Path

# Import bot components
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bots.email_bot import EmailBot, SURVEILLANCE_LOG_PATH

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Bot state
bot_state = {
    'running': False,
    'last_run': None,
    'processed_count': 0,
    'error_count': 0,
    'status': 'stopped'
}

bot_thread = None
email_bot = None

# Configuration paths
REPO_ROOT = Path(__file__).parent
DATA_DIR = REPO_ROOT / 'data'
CONFIG_DIR = REPO_ROOT / 'config'

def ensure_directories():
    """Ensure required directories exist"""
    DATA_DIR.mkdir(exist_ok=True)
    CONFIG_DIR.mkdir(exist_ok=True)

ensure_directories()

# ============================================================================
# Dashboard Routes
# ============================================================================

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """Get current bot status"""
    return jsonify({
        'bot_state': bot_state,
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

@app.route('/api/logs')
def get_logs():
    """Get surveillance logs with optional filtering"""
    limit = request.args.get('limit', 100, type=int)
    category = request.args.get('category', None)
    
    try:
        if os.path.exists(SURVEILLANCE_LOG_PATH):
            with open(SURVEILLANCE_LOG_PATH, 'r') as f:
                logs = json.load(f)
            
            # Filter by category if specified
            if category and category != 'all':
                logs = [log for log in logs if log.get('category') == category]
            
            # Return most recent logs
            logs = logs[-limit:] if len(logs) > limit else logs
            logs.reverse()  # Most recent first
            
            return jsonify({
                'logs': logs,
                'total': len(logs)
            })
        else:
            return jsonify({
                'logs': [],
                'total': 0
            })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'logs': [],
            'total': 0
        }), 500

@app.route('/api/statistics')
def get_statistics():
    """Get email processing statistics"""
    try:
        if os.path.exists(SURVEILLANCE_LOG_PATH):
            with open(SURVEILLANCE_LOG_PATH, 'r') as f:
                logs = json.load(f)
            
            # Calculate statistics
            stats = {
                'total': len(logs),
                'by_category': {},
                'by_date': {},
                'recent_activity': []
            }
            
            # Count by category
            for log in logs:
                category = log.get('category', 'Unknown')
                stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
                
                # Extract date
                timestamp = log.get('timestamp', '')
                date = timestamp.split('T')[0] if 'T' in timestamp else 'Unknown'
                stats['by_date'][date] = stats['by_date'].get(date, 0) + 1
            
            # Get recent activity (last 10 entries)
            stats['recent_activity'] = logs[-10:] if len(logs) >= 10 else logs
            stats['recent_activity'].reverse()
            
            return jsonify(stats)
        else:
            return jsonify({
                'total': 0,
                'by_category': {},
                'by_date': {},
                'recent_activity': []
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/start', methods=['POST'])
def start_bot():
    """Start the email bot"""
    global bot_state, bot_thread, email_bot
    
    if bot_state['running']:
        return jsonify({'error': 'Bot is already running'}), 400
    
    try:
        # Initialize bot
        credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
        email_bot = EmailBot(credentials_path)
        
        # Start bot in background thread
        bot_state['running'] = True
        bot_state['status'] = 'running'
        bot_state['last_run'] = datetime.now(timezone.utc).isoformat()
        
        # Get check interval from environment or use default (5 minutes)
        check_interval = int(os.getenv('EMAIL_CHECK_INTERVAL', 300))
        
        def run_bot():
            global bot_state
            while bot_state['running']:
                try:
                    if email_bot and email_bot.service:
                        email_bot.process_inbox(max_results=50)
                        bot_state['processed_count'] += 1
                    bot_state['last_run'] = datetime.now(timezone.utc).isoformat()
                    # Wait between checks (configurable via EMAIL_CHECK_INTERVAL env var)
                    time.sleep(check_interval)
                except Exception as e:
                    bot_state['error_count'] += 1
                    print(f"Bot error: {e}")
                    time.sleep(60)  # Wait 1 minute on error
        
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Bot started successfully',
            'bot_state': bot_state
        })
    except Exception as e:
        bot_state['running'] = False
        bot_state['status'] = 'error'
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    """Stop the email bot"""
    global bot_state
    
    if not bot_state['running']:
        return jsonify({'error': 'Bot is not running'}), 400
    
    bot_state['running'] = False
    bot_state['status'] = 'stopped'
    
    return jsonify({
        'success': True,
        'message': 'Bot stopped successfully',
        'bot_state': bot_state
    })

@app.route('/api/bot/process-now', methods=['POST'])
def process_now():
    """Manually trigger email processing"""
    global email_bot
    
    try:
        credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
        if not email_bot:
            email_bot = EmailBot(credentials_path)
        
        if email_bot.service:
            email_bot.process_inbox(max_results=50)
            return jsonify({
                'success': True,
                'message': 'Email processing completed'
            })
        else:
            return jsonify({
                'error': 'Gmail API not configured. Please set up credentials.',
                'details': f'Place credentials.json at: {os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json")}',
                'help': 'See DEPLOYMENT.md for Gmail API setup instructions'
            }), 400
    except Exception as e:
        return jsonify({
            'error': f'Failed to process emails: {str(e)}',
            'help': 'Check logs and verify Gmail API credentials are configured correctly'
        }), 500

@app.route('/api/config', methods=['GET', 'POST'])
def manage_config():
    """Get or update bot configuration"""
    config_path = CONFIG_DIR / 'email_config.json'
    
    if request.method == 'GET':
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
            return jsonify(config)
        else:
            return jsonify({
                'auto_response_enabled': True,
                'check_interval': 300,
                'max_emails_per_check': 50
            })
    
    elif request.method == 'POST':
        try:
            config = request.get_json()
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return jsonify({'success': True, 'message': 'Configuration updated'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """Run the dashboard server"""
    print("=" * 70)
    print("ENS Legis AI Clone OS - Interactive Dashboard")
    print("=" * 70)
    print()
    print("Starting dashboard server...")
    print(f"Dashboard will be available at: http://localhost:5000")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    
    # Get host and port from environment or use defaults
    host = os.getenv('DASHBOARD_HOST', '0.0.0.0')
    port = int(os.getenv('DASHBOARD_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()
