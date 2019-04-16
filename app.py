from __future__ import division, print_function

# required by model
from keras.layers import Conv2D, UpSampling2D, Input, MaxPooling2D
from keras.layers import InputLayer, concatenate, Reshape
from keras.layers.core import RepeatVector
from keras.models import Model
import tensorflow as tf

# for server
from keras.models import load_model
from keras.preprocessing.image import array_to_img, img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb, rgb2gray, gray2rgb
from skimage.io import imsave
import numpy as np
import os
import cv2
from PIL import Image
import base64
from io import BytesIO
from json import dumps

# coding=utf-8
import glob
import re

# Flask utils
from flask import Flask, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

#disable warnings
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
tf.logging.set_verbosity(tf.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/group.h5'

# Load your trained model
model = load_model(MODEL_PATH)

print('Model loaded. Start serving...')

def model_predict(img_path, model):
    img = cv2.imread(img_path, cv2.COLOR_BGR2RGB)
    width, height, channels = img.shape
    og_size = (width,height)

    gray = []
    gray.append(img_to_array(img))
    gray = np.array(gray, dtype=float)
    gray = rgb2lab(1.0/255*gray)[:,:,:,0]
    gray = gray.reshape(gray.shape+(1,))

    IMG_SIZE = 256
    img = cv2.resize(img,(IMG_SIZE, IMG_SIZE))

    color_me = []
    color_me.append(img_to_array(img))
    color_me = np.array(color_me, dtype=float)
    temp = color_me

    color_me = rgb2lab(1.0/255*color_me)[:,:,:,0]
    color_me = color_me.reshape(color_me.shape+(1,))

    # Predict
    output = model.predict(color_me)
    output = output * 128

    cur = np.zeros((width, height, 3))
    cur[:,:,0] = gray[0][:,:,0]
    out_new = cv2.resize(output[0],(height, width))
    cur[:,:,1:] = out_new
    res_img = lab2rgb(cur)
    imsave("result.jpg",res_img)
    
    # res_img = Image.fromarray(np.uint8(res_img))
    res_img = Image.open("result.jpg")
    output = BytesIO()
    res_img.save(output, format='JPEG')
    # output.seek(0)
    # im_data = output.getvalue()
    im_data = base64.b64encode(output.getvalue())
    # json_data = dumps(im_data)

    return im_data


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        result = model_predict(file_path, model)

        return result
    return None


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('', 5001), app)
    http_server.serve_forever()
