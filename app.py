from PIL import Image
from os.path import join, dirname, realpath
from glob import glob

import streamlit as st
import numpy as np
import tensorflow as tf
import numpy as np

import os
import cv2
import imutils


# Loading images to frontend
def load_image(image_file):
	img = Image.open(image_file)
	return img

st.text("Stany Ganyani R204442S")
st.text("Tungamiraishe Mukwena R204452G")


# User search query
search_query = st.text_input("enter object to query", "search query",key="search_query" )

# Allow user to upload video
video = st.file_uploader(label="upload video", type="mp4", key="video_upload_file")

# Continue only if video is uploaded successfully
if(video is not None):
    # Notify user
    st.text("video has been uploaded")
    # Gather video meta data
    file_details = {"filename":video.name, "filetype":video.type,
                    "filesize":video.size}
    # Show on ui
    st.write(file_details)
    # save video
    with open(video.name, "wb") as f:
        f.write(video.getbuffer())
    # Notify user
    st.success("file saved")

    # Show video on ui 
    video_file = open(file_details['filename'], 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    # Create frames for the video and save 
    def create_frames():
        images_array = []
        cap = cv2.VideoCapture(video.name)
        index = 0

        while True:
            ret, frame = cap.read()
            if ret == False:
                cap.release()
                break
            if frame is None:
                break
            else:
                if index == 0:
                    images_array.append(frame)
                    cv2.imwrite(f"frames/{index}.jpeg", frame)

                else:
                    if index % 10 == 0:
                        images_array.append(frame)
                    cv2.imwrite(f"frames/{index}.jpeg", frame)

            index += 1
        return np.array(images_array)
    

    # Create frames
    images_array = create_frames()

    # Continue only if frames have been successfully created 
    if len(images_array) > 0:
        frame_paths = glob(f"frames/*.jpeg")
        for path in frame_paths:
            st.image(load_image(path),width=250)

    # Resize the frames for the model
    def resize_frames():
        frame_paths = glob(f"frames/*.jpeg")
        index = 0
        width, height = (299, 299)

        for frame in frame_paths:
            image = cv2.imread(frame)
            image_resized = cv2.resize(image, (299, 299))
            cv2.imwrite("resized/%i.jpeg"%index, image_resized)
            
            index += 1  

    # Resize the frames for the model 
    resize_frames()

    # Classify frames
    def predict():
        def fetch_frames():
            frame_paths = glob(f"resized/*.jpeg")
            query_frames_array = []

            for frame in frame_paths:
                image = cv2.imread(frame)
                image = np.expand_dims(image, axis=0)
                query_frames_array.append(image)
            return np.array(query_frames_array)

        query_frames_array = fetch_frames()
        video_frame_classifier = tf.keras.models.load_model("inception_saved")
        query_results = video_frame_classifier.predict(query_frames_array)
        decoded_query_results = tf.keras.applications.inception_v3.decode_predictions(query_results, top=5)
        return decoded_query_results

    # Fetch decoded results from predictions
    decoded_results = predict()

    # Show results to ui
    def showResults(decoded_response):
        st.text("running show results function")
        for i in range(len(decoded_response)):
            class_tupple = decoded_response[i]
            _id, frame_class, frame_prob = class_tupple[0]
            image_index = i
            if search_query == "":
                pass
            elif search_query == frame_class:
                image_index = i
                break
        return i, frame_class

    # Show results to ui
    image_index, frame_class = showResults(decoded_results)

    # Present results to user on ui
    if search_query == frame_class:
        st.text("we have found the frame matching your seqrch query")
        st.text(frame_class)
    else:
        st.text("sorry, we could not find the frame matching your seqrch query")
        st.text("you can visually go through the above frames to search for your search query")
        st.text("last frame of the video")

    # Load image to frontend
    st.image(load_image(f"frames/{image_index}.jpeg"),width=250)




