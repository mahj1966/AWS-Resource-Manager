from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader
import os

class BaseResource(ABC):
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader('app/templates/terraform')
        )
    
    @abstractmethod
    def validate_config(self, config):
        """Validate resource configuration"""
        pass
    
    def generate_config(self, config):
        """Generate Terraform configuration"""
        self.validate_config(config)
        template = self.env.get_template(f'{self.resource_type}.tf.j2')
        return template.render(**config) 