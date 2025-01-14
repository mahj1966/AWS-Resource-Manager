from flask import Flask, render_template, request, jsonify
from resources.ec2 import EC2Resource
from resources.rds import RDSResource
from resources.s3 import S3Resource

app = Flask(__name__)

# Initialize resource handlers
resources = {
    'ec2': EC2Resource(),
    'rds': RDSResource(),
    's3': S3Resource()
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_terraform():
    resource_type = request.json.get('resource_type')
    config = request.json.get('config')
    
    if resource_type not in resources:
        return jsonify({'error': 'Invalid resource type'}), 400
    
    try:
        terraform_config = resources[resource_type].generate_config(config)
        return jsonify({'config': terraform_config})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 