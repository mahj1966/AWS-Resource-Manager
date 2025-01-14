from . import BaseResource
import re

class RDSResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.resource_type = 'rds'
    
    def validate_config(self, config):
        # Required fields validation
        required_fields = ['identifier', 'engine', 'instance_class', 'username', 'password']
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Identifier validation
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9-]*[a-zA-Z0-9]$', config['identifier']):
            raise ValueError("Invalid identifier format")
        
        # Storage validation
        if 'allocated_storage' in config:
            storage = int(config['allocated_storage'])
            if storage < 20 or storage > 65536:
                raise ValueError("Allocated storage must be between 20 and 65536 GB")
        
        # IOPS validation
        if config.get('storage_type') == 'io1' and 'iops' in config:
            iops = int(config['iops'])
            if iops < 1000 or iops > 256000:
                raise ValueError("IOPS must be between 1000 and 256000") 