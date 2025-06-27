"""
Security utilities for MCP task callbacks
"""
import secrets
import hashlib
import time
import hmac
import base64
from typing import Optional
from urllib.parse import urlencode, urlparse, parse_qs
from app.core.config import settings


class SecureCallbackManager:
    """Manages secure callback URLs with token signatures"""
    
    def __init__(self, secret_key: Optional[str] = None):
        """Initialize with a secret key for signing"""
        self.secret_key = secret_key or secrets.token_hex(32)
    
    def _encode_base64(self, data: str) -> str:
        """Encode string to base64 URL-safe format"""
        return base64.urlsafe_b64encode(data.encode('utf-8')).decode('utf-8').rstrip('=')
    
    def _decode_base64(self, encoded_data: str) -> str:
        """Decode base64 URL-safe format to string"""
        # Add padding if needed
        padding = 4 - len(encoded_data) % 4
        if padding != 4:
            encoded_data += '=' * padding
        
        return base64.urlsafe_b64decode(encoded_data.encode('utf-8')).decode('utf-8')
    
    def generate_api_callback_url(self, task_id: str, expires_in: int = 3600) -> str:
        """
        Generate a secure callback URL that points back to the API
        
        Args:
            task_id: The task ID for verification
            expires_in: Token expiration time in seconds (default: 1 hour)
            
        Returns:
            str: Secure callback URL pointing to the API
        """
        # Generate a unique token
        token = secrets.token_hex(32)
        
        # Create expiration timestamp
        expires_at = int(time.time()) + expires_in
        
        # Create signature data
        signature_data = f"{task_id}:{expires_at}:{token}"
        
        # Generate HMAC signature
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            signature_data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Encode task_id and signature to base64
        encoded_task_id = self._encode_base64(task_id)
        encoded_signature = self._encode_base64(signature)
        
        # Build callback URL pointing to the API (ensure no double slashes)
        api_url = settings.API_URL.rstrip('/')
        callback_url = f"{api_url}/agents/mcp/callback"
        
        # Add security parameters
        query_params = {
            'task_id': encoded_task_id,
            'token': token,
            'expires_at': str(expires_at),
            'signature': encoded_signature
        }
        
        # Construct the full URL
        secure_url = f"{callback_url}?{urlencode(query_params)}"
        
        return secure_url
    
    def verify_callback_token(self, encoded_task_id: str, token: str, 
                            expires_at: str, encoded_signature: str) -> tuple[bool, Optional[str]]:
        """
        Verify the callback token signature
        
        Args:
            encoded_task_id: The base64 encoded task ID
            token: The token from the callback
            expires_at: The expiration timestamp
            encoded_signature: The base64 encoded signature to verify
            
        Returns:
            tuple: (is_valid, decoded_task_id)
        """
        try:
            # Decode task_id and signature
            task_id = self._decode_base64(encoded_task_id)
            signature = self._decode_base64(encoded_signature)
            
            # Check if token has expired
            if int(time.time()) > int(expires_at):
                return False, None
            
            # Recreate signature data
            signature_data = f"{task_id}:{expires_at}:{token}"
            
            # Generate expected signature
            expected_signature = hmac.new(
                self.secret_key.encode('utf-8'),
                signature_data.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures (constant-time comparison)
            is_valid = hmac.compare_digest(signature, expected_signature)
            return is_valid, task_id if is_valid else None
            
        except (ValueError, TypeError, Exception):
            return False, None
    
    def extract_callback_params(self, url: str) -> Optional[dict]:
        """
        Extract callback parameters from a secure URL
        
        Args:
            url: The secure callback URL
            
        Returns:
            dict: Parameters if valid, None otherwise
        """
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            
            encoded_task_id = query_params.get('task_id', [None])[0]
            token = query_params.get('token', [None])[0]
            expires_at = query_params.get('expires_at', [None])[0]
            encoded_signature = query_params.get('signature', [None])[0]
            
            if not all([encoded_task_id, token, expires_at, encoded_signature]):
                return None
            
            # Verify the token and get decoded task_id
            is_valid, decoded_task_id = self.verify_callback_token(
                encoded_task_id, token, expires_at, encoded_signature
            )
            
            if not is_valid or not decoded_task_id:
                return None
            
            return {
                'task_id': decoded_task_id,
                'encoded_task_id': encoded_task_id,
                'token': token,
                'expires_at': expires_at,
                'encoded_signature': encoded_signature
            }
            
        except Exception:
            return None


# Global instance
callback_manager = SecureCallbackManager() 