from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
import cv2
import imghdr
import os

app = Flask(__name__)

model = tf.keras.models.load_model("C:/Users/ranaa.LAPTOP-C1H36I28/Downloads/BoneFracturedModel.h5")

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (256, 256))
    img = img / 255.0
    return img

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image data provided"})

        file = request.files['image']

        if file.filename == '':
            return jsonify({"error": "No selected file"})

        if file and imghdr.what(file.stream) in ['jpeg', 'png', 'gif', 'bmp']:
            # Ensure the 'temp' directory exists
            temp_dir = 'temp'
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Generate a unique filename
            filename = 'temp_image.jpg'
            file_path = os.path.join(temp_dir, filename)

            # If the file already exists, delete it
            if os.path.exists(file_path):
                os.remove(file_path)

            # Save the file
            file.save(file_path)

            # Preprocess the image
            img = preprocess_image(file_path)

            # Make prediction
            prediction = model.predict(np.expand_dims(img, axis=0))[0]

            # Remove the temporary image file
            os.remove(file_path)

            # Determine result based on prediction
            if prediction > 0.5:
                result = "Not Fractured"
            else:
                result = "Fractured"

            return jsonify({"prediction": result})
        else:
            return jsonify({"error": "Invalid file type"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(port=3000,debug=True)
