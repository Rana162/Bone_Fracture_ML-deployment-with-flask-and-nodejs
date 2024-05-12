from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
import cv2
import imghdr
import os

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model("C:/Users/ranaa.LAPTOP-C1H36I28/Downloads/BoneFracturedModel.h5")

# Define a function to preprocess the image
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (256, 256))  # Resize the image to match the model's input shape
    img = img / 255.0  # Normalize the pixel values to the range [0, 1]
    return img

# Route for the home page
@app.route('/')
def home():
    
    return render_template('index.html')


# Route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    # Check if the file is empty
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    # Check if the file is an image
    if file and imghdr.what(file.stream) in ['jpeg', 'png', 'gif', 'bmp']:
        # Save the image to a temporary directory
        filename = 'temp_image.jpg'
        file_path = os.path.join('temp', filename)
        file.save(file_path)
        
        # Preprocess the image
        img = preprocess_image(file_path)
        
        # Make prediction
        prediction = model.predict(np.expand_dims(img, axis=0))[0]
        
        # Cleanup: delete the temporary image file
        os.remove(file_path)
        
        # Convert the probability to a label
        if prediction > 0.5:
            result = " Not Fractured"
        else:
            result = " Fractured"
        
        return jsonify({"prediction": result})
    
    else:
        return jsonify({"error": "Invalid file type"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Change the port if needed

