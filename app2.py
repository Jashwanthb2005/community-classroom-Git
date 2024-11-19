import os
from flask import Flask, request, jsonify
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
from flask_cors import CORS

# Initialize Flask app and enable CORS
app = Flask(__name__, static_folder='static')

CORS(app)

# Load disease and supplement info
disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv', encoding='cp1252')

# Load the trained CNN model
model = CNN.CNN(39)
model.load_state_dict(torch.load("plant_disease_model_1_latest.pt"))
model.eval()

def prediction(image_path):
    """Process the uploaded image and predict the disease"""
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)  # Get the predicted class index
    return index

@app.route('/api/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    # Save the uploaded image
    image = request.files['image']
    filename = image.filename
    file_path = os.path.join('static/uploads', filename)
    image.save(file_path)

    # Perform prediction
    pred = prediction(file_path)

    # Fetch prediction details from the CSV data
    title = disease_info['disease_name'][pred]
    description = disease_info['description'][pred]
    prevent = disease_info['Possible Steps'][pred]
    image_url = disease_info['image_url'][pred]
    supplement_name = supplement_info['supplement name'][pred]
    supplement_image_url = supplement_info['supplement image'][pred]
    supplement_buy_link = supplement_info['buy link'][pred]

    # Prepare the response
    response = {
        'title': title,
        'description': description,
        'prevent': prevent,
        'image_url': image_url,
        'supplement_name': supplement_name,
        'supplement_image_url': supplement_image_url,
        'supplement_buy_link': supplement_buy_link
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
