from datetime import datetime, timedelta
from typing import Optional
from config.settings import GEMINI_API_KEYS

class QuotaManager:
    def __init__(self):
        self.current_key_index = 0
        self.quota_reset_times = {}
        self.failed_attempts = {}
        
    def get_current_api_key(self) -> str:
        return GEMINI_API_KEYS[self.current_key_index]
    
    def rotate_api_key(self) -> Optional[str]:
        """Rotate to next available API key"""
        self.current_key_index = (self.current_key_index + 1) % len(GEMINI_API_KEYS)
        return self.get_current_api_key()
    
    def mark_quota_exceeded(self, api_key: str):
        """Mark an API key as exceeded and set reset time"""
        self.quota_reset_times[api_key] = datetime.now() + timedelta(hours=1)
        self.failed_attempts[api_key] = self.failed_attempts.get(api_key, 0) + 1
    
    def is_key_available(self, api_key: str) -> bool:
        """Check if an API key is available for use"""
        if api_key not in self.quota_reset_times:
            return True
       
        if datetime.now() > self.quota_reset_times[api_key]:
            del self.quota_reset_times[api_key]
            return True
            
        return False