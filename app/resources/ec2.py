from . import BaseResource
import re

class EC2Resource(BaseResource):
    def __init__(self):
        super().__init__()
        self.resource_type = 'ec2'
        
        # Define valid instance types
        self.valid_instance_types = [
            't3.micro', 't3.small', 't3.medium',
            'c5.large', 'c5.xlarge',
            'r5.large', 'r5.xlarge'
        ]
    
    def validate_config(self, config):
        # Required fields validation
        required_fields = ['instance_type', 'ami_id', 'name']
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Instance name validation
        if not re.match(r'^[a-zA-Z0-9-]+$', config['name']):
            raise ValueError("Instance name must contain only letters, numbers, and hyphens")
        
        # Instance type validation
        if config['instance_type'] not in self.valid_instance_types:
            raise ValueError(f"Invalid instance type. Must be one of: {', '.join(self.valid_instance_types)}")
        
        # AMI ID validation
        if not re.match(r'^ami-[a-f0-9]{8,17}$', config['ami_id']):
            raise ValueError("Invalid AMI ID format")
        
        # Volume size validation
        if 'root_volume_size' in config:
            size = int(config['root_volume_size'])
            if size < 8 or size > 16384:
                raise ValueError("Root volume size must be between 8 and 16384 GB")
        
        # IOPS validation
        if config.get('root_volume_type') in ['io1', 'io2'] and 'iops' in config:
            iops = int(config['iops'])
            if iops < 100 or iops > 64000:
                raise ValueError("IOPS must be between 100 and 64000")
        
        # Security group validation
        if 'vpc_security_group_ids' in config:
            sg_ids = config['vpc_security_group_ids'].split(',')
            for sg_id in sg_ids:
                if not re.match(r'^sg-[a-f0-9]{8,17}$', sg_id.strip()):
                    raise ValueError(f"Invalid security group ID format: {sg_id}")
        
        # Subnet validation
        if 'subnet_id' in config and not re.match(r'^subnet-[a-f0-9]{8,17}$', config['subnet_id']):
            raise ValueError("Invalid subnet ID format")
        
        # VPC validation
        if 'vpc_id' in config and not re.match(r'^vpc-[a-f0-9]{8,17}$', config['vpc_id']):
            raise ValueError("Invalid VPC ID format") 