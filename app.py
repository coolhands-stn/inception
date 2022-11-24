import streamlit as st

from flask import Flask, render_template, request, redirect, url_for
from os.path import join, dirname, realpath
from glob import glob
import numpy as np
import os
import cv2, imutils
import tensorflow as tf


VIDEO = join(dirname(realpath(__file__)), "static/uploads/videos")
FRAMES = join(dirname(realpath(__file__)), "static/frames")
RESIZED = join(dirname(realpath(__file__)), "static/resized")

app = Flask(__name__, template_folder="template")
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        os.makedirs(VIDEO)
        if request.files:
            video = request.files["video"]
            video.save(os.path.join(VIDEO, video.filename))
            os.makedirs(FRAMES)
            return redirect(url_for("frames"))
    return render_template("index.html")