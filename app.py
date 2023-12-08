from flask import Flask, render_template, request
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

# Assuming your OpenAI API key is set as an environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    generated_images = []
    cost_per_image = {
        'Standard_1024x1024': 0.040,
        'Standard_1024x1792': 0.080,
        'Standard_1792x1024': 0.080,
        'HD_1024x1024': 0.080,
        'HD_1024x1792': 0.120,
        'HD_1792x1024': 0.120
    }

    if request.method == 'POST':
        prompt = request.form.get('prompt')
        quality = request.form.get('quality')
        size = request.form.get('size')
        n = int(request.form.get('number_of_images'))

        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': 'dall-e-3',
            'prompt': prompt,
            'n': n,
            'size': size
        }

        try:
            response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=data)
            response.raise_for_status()
            result = response.json()

            for item in result['data']:
                generated_images.append({
                    'url': item['url'],
                    'cost': cost_per_image[f'{quality}_{size}']
                })

        except requests.exceptions.HTTPError as err:
            error_message = str(err)

    return render_template('index.html', error_message=error_message, generated_images=generated_images)


if __name__ == '__main__':
    app.run(debug=True)
