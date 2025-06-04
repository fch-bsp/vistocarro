import os
import base64
from datetime import datetime
import shutil

class LocalStorage:
    def __init__(self):
        """Initialize local storage handler."""
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storage")
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure that necessary directories exist."""
        os.makedirs(os.path.join(self.base_dir, "uploads"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "reports"), exist_ok=True)
    
    def upload_file_object(self, file_content, object_key):
        """Save a file object to local storage.
        
        Args:
            file_content: The content of the file to save
            object_key: The key (path) where the file will be stored
        
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            # Create directory structure if needed
            full_path = os.path.join(self.base_dir, object_key)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Write file
            with open(full_path, 'wb') as f:
                if isinstance(file_content, str):
                    f.write(file_content.encode('utf-8'))
                else:
                    f.write(file_content)
            return True
        except Exception as e:
            print(f"Error saving file locally: {e}")
            return False
    
    def get_file_url(self, object_key):
        """Generate a local file URL.
        
        Args:
            object_key: The key (path) of the object
        
        Returns:
            str: Local file path
        """
        try:
            full_path = os.path.join(self.base_dir, object_key)
            return f"file://{os.path.abspath(full_path)}"
        except Exception as e:
            print(f"Error generating file URL: {e}")
            return None
    
    def download_file(self, object_key):
        """Read a file from local storage.
        
        Args:
            object_key: The key (path) of the object
        
        Returns:
            bytes: The content of the file
        """
        try:
            full_path = os.path.join(self.base_dir, object_key)
            with open(full_path, 'rb') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def get_presigned_url(self, object_key):
        """For compatibility with S3Handler, returns a local path.
        
        Args:
            object_key: The key (path) of the object
        
        Returns:
            str: Local file path
        """
        return self.get_file_url(object_key)