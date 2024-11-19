import os
from flask import Flask, jsonify,request
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
from flask_cors import CORS


app = Flask(__name__, static_folder='static')

CORS(app)


disease_info = pd.read_csv('disease_info.csv' , encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv',encoding='cp1252')

model = CNN.CNN(39)    
model.load_state_dict(torch.load("plantmodel2.pt"))
model.eval()

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index




@app.route('/api/predict',methods=['POST'])


def predict():

        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400


        image = request.files['image']
        filename = image.filename
        file_path = os.path.join('static/uploads', filename)
        image.save(file_path)
        
        pred = prediction(file_path)

        title = disease_info['disease_name'][pred]
        description =disease_info['description'][pred]
        prevent = disease_info['Possible Steps'][pred]
        image_url = disease_info['image_url'][pred]
        supplement_name = supplement_info['supplement name'][pred]
        supplement_image_url = supplement_info['supplement image'][pred]
        supplement_buy_link = supplement_info['buy link'][pred]
        

        response = {
            'title': title,
            'description': description,
            'prevent': prevent,
            'image_url': image_url,
            'supplement_name': supplement_name,
            'supplement_image_url': supplement_image_url,
            'supplement_buy_link': supplement_buy_link
        }
        
        return jsonify(response),200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)