import os
import uuid
from flask import Flask, request
from werkzeug.utils import secure_filename
from moviepy.editor import *

UPLOAD_FOLDER = "./video_files/"
ALLOWED_EXTENSIONS = {'mp4'}

def load_flask_server():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/status', methods=['GET'])
    def check_status():
        return {
            "status": "200",
            "message": "server is up and running!"
        }

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                return {
                    "status": "400",
                    "message": "no file part"
                }
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                return {
                    "status": "400",
                    "message": "filename empty"
                }

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                help_concat_and_save(file, filename,  app)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return {
                    "status": "200",
                    "message": "successfully uploaded {}".format(filename)
                }
    return app


def help_concat_and_save(file, filename, app):
    if os.path.isfile(UPLOAD_FOLDER + 'output.mp4'):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        tmp_output_name = str(uuid.uuid4) + '.mp4'
        out_video = VideoFileClip(UPLOAD_FOLDER + 'output.mp4')
        out_video.to_videofile(UPLOAD_FOLDER + tmp_output_name, fps=24, remove_temp=True)
        old = VideoFileClip(UPLOAD_FOLDER + tmp_output_name)
        current = VideoFileClip(UPLOAD_FOLDER + filename)
        clip = concatenate_videoclips([old, current])
        clip.to_videofile(UPLOAD_FOLDER + "output.mp4", fps=24, remove_temp=True)
        os.remove(UPLOAD_FOLDER + tmp_output_name)
        os.remove(UPLOAD_FOLDER + filename)
    else:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'output.mp4'))

