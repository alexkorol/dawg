from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    generated_images = []
    form_data = {}
    cost_per_image = {
        'Standard_1024x1024': 0.040,
        'Standard_1024x1792': 0.080,
        'Standard_1792x1024': 0.080,
        'HD_1024x1024': 0.080,
        'HD_1024x1792': 0.120,
        'HD_1792x1024': 0.120
    }

    if request.method == 'POST':
        form_data = request.form
        api_key = form_data.get('api_key')
        prompt = form_data.get('prompt')
        size = form_data.get('size')
        n = int(form_data.get('number_of_images', '1'))
        quality = 'HD' if form_data.get('quality') == 'on' else 'Standard'

        headers = {
            'Authorization': f'Bearer {api_key}',
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
                    'cost': cost_per_image[f'{quality}_{size}'],
                    'prompt': prompt
                })

        except requests.exceptions.HTTPError as err:
            error_message = str(err)

    return render_template('index.html', error_message=error_message, generated_images=generated_images, form_data=form_data)


if __name__ == '__main__':
    app.run(debug=True)