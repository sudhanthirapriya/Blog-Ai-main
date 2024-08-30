from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Set Cohere API key from environment variable
cohere_api_key = os.getenv('COHERE_API_KEY')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
    
    try:
        headers = {
            'Authorization': f'Bearer {cohere_api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': 'command-xlarge-nightly',  # Use the correct model
            'prompt': prompt,
            'max_tokens': 500
        }
        response = requests.post(
            'https://api.cohere.ai/v1/generate',  # Correct API endpoint
            headers=headers,
            json=payload
        )
        
        # Log the response for debugging
        print("Response Status Code:", response.status_code)
        print("Response JSON:", response.json())
        
        response_data = response.json()
        if 'error' in response_data:
            raise Exception(response_data['error'])
        
        # Handle response based on observed format
        # This assumes the response is a simple text string, adjust based on actual structure
        if 'text' in response_data:
            generated_text = response_data['text']
        elif 'generations' in response_data:
            generated_text = response_data['generations'][0]['text']
        else:
            raise Exception('Unexpected response format')

        return jsonify({'response': generated_text.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
