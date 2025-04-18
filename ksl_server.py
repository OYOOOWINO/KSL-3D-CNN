# -*- coding: utf-8 -*-
"""KSL SERVER

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZZgcrhfw5Mg7L-sP6Ev719Yf-rvw_U3z
"""

import multiprocessing

print("Number of cpu : ", multiprocessing.cpu_count())

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !sudo apt-get install python3-magic
# !pip install tqdm tensorflow opencv-python flask
# !pip install cloudinary flask-cors

import cloudinary
import cloudinary.uploader
import cloudinary.api
import json

CLOUDINARY_URL = "cloudinary://******:************"
config = cloudinary.config(cloud_name="*****", api_key="*****", api_secret="***")

from google.colab import drive
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from flask_cors import CORS, cross_origin
import urllib.request
from werkzeug.utils import secure_filename
import os
import numpy as np
import tensorflow as tf
import cv2
from collections import deque
import uuid

drive.mount("/content/drive")

templates_dir = "/content/drive/MyDrive/KSL/WebApp/build"
model_file = "/content/drive/MyDrive/KSL/Models/model.h5"
upload_folder = "/content/drive/MyDrive/KSL/WebApp/videos/"
IMAGE_HEIGHT, IMAGE_WIDTH = 270, 270
SEQUENCE_LENGTH = 8
CLASSES_LIST = ["work", "come", "go", "home", "hello"]

# Load Model
model = tf.keras.models.load_model(model_file)


def filter_dicts_by_previous_key(list_of_dicts):
    filtered_list = []

    previous_key = None
    for dictionary in list_of_dicts:
        current_key = next(iter(dictionary))  # Get the key of the current dictionary

        if previous_key is None or current_key != previous_key:
            filtered_list.append(dictionary)
            previous_key = current_key

    return filtered_list


def predictVideo(videoPath, outputPath, SEQUENCE_LENGTH):
    sentence_analytics = []
    sentence = []
    videoReader = cv2.VideoCapture(videoPath)
    videoWidth = int(videoReader.get(cv2.CAP_PROP_FRAME_WIDTH))
    videoHeight = int(videoReader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    videoWriter = cv2.VideoWriter(
        outputPath,
        cv2.VideoWriter_fourcc("M", "P", "4", "V"),
        videoReader.get(cv2.CAP_PROP_FPS),
        (videoWidth, videoHeight),
    )
    framesQueue = deque(maxlen=SEQUENCE_LENGTH)
    predictedClass = ""
    predictedProbabilities = ""

    while videoReader.isOpened():
        ok, frame = videoReader.read()
        if not ok:
            break

        resizedFrame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
        normalizedFrame = resizedFrame / 255
        framesQueue.append(normalizedFrame)

        if len(framesQueue) == SEQUENCE_LENGTH:
            predictedProbabilities = model.predict(np.expand_dims(framesQueue, axis=0))[
                0
            ]
            predictedLabel = np.argmax(predictedProbabilities)
            predictedClass = CLASSES_LIST[predictedLabel]
            classProbability = predictedProbabilities[predictedLabel]
            _object = {}
            _object[predictedClass] = float(classProbability)
            sentence.append(_object)
        cv2.putText(
            frame, predictedClass, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )
        videoWriter.write(frame)
    videoWriter.release()
    videoWriter.release()
    print(sentence)
    return sentence


output_video_file_path = (
    f"/content/drive/MyDrive/KSL/TaggedVideo/hr_flip_v_051_from.mp4"
)
input_video_file_path = f"/content/drive/MyDrive/KSL/TaggedVideo/cnjfopifwVIfklflkD-202ffkleflk30905_home.mp4"

# Perform Action Recognition on the Test Video.
# predictVideo(input_video_file_path, output_video_file_path, SEQUENCE_LENGTH)

app = Flask(__name__, static_folder=templates_dir, static_url_path="/")
app.secret_key = "secret key"
app.config["UPLOAD_FOLDER"] = upload_folder
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
CORS(app)


def predict_on_video(video_file_path, output_file_path):
    # Load LRCN model
    LRCN_model = model

    # Initialize video reader and writer
    video_reader = cv2.VideoCapture(video_file_path)
    frame_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video_reader.get(cv2.CAP_PROP_FPS)
    video_writer = cv2.VideoWriter(
        output_file_path,
        cv2.VideoWriter_fourcc("M", "P", "4", "V"),
        fps,
        (frame_width, frame_height),
    )

    # Prepare to collect frames
    frames_queue = deque(maxlen=SEQUENCE_LENGTH)
    predicted_class_name = ""

    while video_reader.isOpened():
        ret, frame = video_reader.read()
        if not ret:
            break

        # Preprocess the frame
        resized_frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
        normalized_frame = resized_frame / 255.0
        frames_queue.append(normalized_frame)

        if len(frames_queue) == SEQUENCE_LENGTH:
            # Predict action
            frame_sequence = np.expand_dims(list(frames_queue), axis=0)
            predictions = LRCN_model.predict(frame_sequence)[0]
            predicted_class = np.argmax(predictions)
            predicted_class_name = CLASSES_LIST[predicted_class]

        # Overlay text on the frame
        cv2.putText(
            frame,
            predicted_class_name,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        video_writer.write(frame)

    # Clean up
    video_reader.release()
    video_writer.release()


# Example usage

testVideo = f"/content/drive/MyDrive/KSL/Classes/home/crop_VID20231027182812_home.mp4"
result = f"/content/drive/MyDrive/KSL/result.mp4"
predict_on_video(testVideo, result)

from google.colab.output import eval_js

print(eval_js("google.colab.kernel.proxyPort(5000)"))


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/upload", methods=["POST"])
@cross_origin()
def upload_video():
    file_to_upload = request.files["file"]
    filename = secure_filename(file_to_upload.filename)
    print(filename)
    if filename != "":
        unq_id = uuid.uuid1()
        file_to_upload.filename = str(unq_id) + "_" + filename
        # Save to drive
        file_to_upload.save(os.path.join(upload_folder, file_to_upload.filename))
        # upload to cloudinary
        # Set the asset's public ID and allow overwriting the asset with new versions
        upload_response = cloudinary.uploader.upload(
            os.path.join(upload_folder, file_to_upload.filename),
            resource_type="video",
            public_id=file_to_upload.filename,
            unique_filename=False,
            overwrite=True,
        )
        results = {"fileName": file_to_upload.filename, "srcURL": upload_response}
        return jsonify(results)


@app.route("/predict", methods=["POST"])
def predict():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        request_data = request.get_json()
        file_name = request_data["fileName"]
        predictions = predictVideo(
            os.path.join(upload_folder, file_name),
            os.path.join(upload_folder, "predition.mp4"),
            SEQUENCE_LENGTH,
        )
        filtered_data = filter_dicts_by_previous_key(predictions)
        print(filtered_data)
        return jsonify(filtered_data)
    else:
        return "Content-Type not supported!"


if __name__ == "__main__":
    app.run()
