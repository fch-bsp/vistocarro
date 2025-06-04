import boto3
import os
from dotenv import load_dotenv

class S3Handler:
    def __init__(self):
        """Initialize S3 client with credentials from environment variables."""
        load_dotenv()
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket_name = os.getenv('S3_BUCKET')
    
    def upload_file_object(self, file_content, object_key):
        """Upload a file object to S3 bucket.
        
        Args:
            file_content: The content of the file to upload
            object_key: The key (path) where the file will be stored in S3
        
        Returns:
            bool: True if upload was successful, False otherwise
        """
        try:
            self.s3_client.put_object(
                Body=file_content,
                Bucket=self.bucket_name,
                Key=object_key
            )
            return True
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return False
    
    def get_presigned_url(self, object_key, expiration=3600):
        """Generate a presigned URL for an S3 object.
        
        Args:
            object_key: The key (path) of the object in S3
            expiration: URL expiration time in seconds (default: 1 hour)
        
        Returns:
            str: Presigned URL for the object
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_key
                },
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            print(f"Error generating presigned URL: {e}")
            return None
    
    def download_file(self, object_key):
        """Download a file from S3.
        
        Args:
            object_key: The key (path) of the object in S3
        
        Returns:
            bytes: The content of the downloaded file
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return response['Body'].read()
        except Exception as e:
            print(f"Error downloading from S3: {e}")
            return None