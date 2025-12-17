import os
import numpy as np
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import random

# Define a flask app
app = Flask(__name__)

# Mock model class for simulation
class MockModel:
    def predict(self, x):
        # Return a random prediction array
        return [np.random.dirichlet(np.ones(15), size=1)[0]]

model = MockModel()

def model_predict(img_path, model):
    # Simulated processing time
    import time
    time.sleep(1)
    return model.predict(None)

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        if 'file' not in request.files:
            return "No file uploaded"
            
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        
        if not os.path.exists(os.path.join(basepath, 'uploads')):
            os.makedirs(os.path.join(basepath, 'uploads'))
            
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        disease_class = ['Pepper bell Bacterial spot', 'Pepper bell healthy', 'Potato Early blight',
                         'Potato Late blight', 'Potato healthy', 'Tomato Bacterial spot', 'Tomato Early blight',
                         'Tomato Late blight', 'Tomato Leaf Mold', 'Tomato Septoria leaf spot',
                         'Tomato Spider mites Two spotted spider mite', 'Tomato Target Spot',
                         'Tomato Tomato YellowLeaf Curl Virus', 'Tomato Tomato mosaic virus', 'Tomato healthy']
        
        a = preds[0]
        ind = np.argmax(a)
        result = disease_class[ind]
        return result
    return None

if __name__ == '__main__':
    # Using a different port to avoid conflicts
    app.run(port=7001, debug=True)
