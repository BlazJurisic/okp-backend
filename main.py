from os import listdir
from os.path import isfile, join
from functools import reduce
from operator import add

import streamlit as st
from flask_endpoint import load_flask_server

if not hasattr(st, 'already_started_server'):
    st.already_started_server = True
    app = load_flask_server()
    app.run(port=8888)


PATH_TO_VIDEOS = './video_files/'

try:
    bytes = open(PATH_TO_VIDEOS + 'output.mp4', 'rb').read()

    st.video(bytes)
except Exception as e:
    st.write("nothing uploaded yet!")
