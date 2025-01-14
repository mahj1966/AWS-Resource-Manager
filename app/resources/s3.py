from . import BaseResource
import re

class S3Resource(BaseResource):
    def __init__(self):
        super().__init__()
        self.resource_type = 's3'
    
    def validate_config(self, config):
        # Required fields validation
        if 'bucket_name' not in config:
            raise ValueError("Bucket name is required")
        
        # Bucket name validation
        if not re.match(r'^[a-z0-9][a-z0-9.-]*[a-z0-9]$', config['bucket_name']):
            raise ValueError("Invalid bucket name format")
        
        # Versioning validation
        if 'versioning' in config and not isinstance(config['versioning'], bool):
            raise ValueError("Versioning must be a boolean value")
        
        # Encryption validation
        if config.get('encryption_type') not in [None, 'AES256', 'aws:kms']:
            raise ValueError("Invalid encryption type") 