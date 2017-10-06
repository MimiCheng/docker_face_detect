import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from PIL import Image, ImageDraw
import face_recognition

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    filelist = [ f for f in os.listdir(app.config['UPLOAD_FOLDER'])]
    for f in filelist:
        os.remove(app.config['UPLOAD_FOLDER']+f)
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = face_recognition.load_image_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        face_landmarks_list = face_recognition.face_landmarks(image)
        imageIn = os.path.join(app.config['UPLOAD_FOLDER'],filename)

        if (face_landmarks_list):
            for i,face_landmarks in enumerate(face_landmarks_list):

                # Print the location of each facial feature in this image
                facial_features = [
                        'chin',
                        'left_eyebrow',
                        'right_eyebrow',
                        'nose_bridge',
                        'nose_tip',
                        'left_eye',
                        'right_eye',
                        'top_lip',
                        'bottom_lip'
                ]
                # Let's trace out each facial feature in the image with a line!
                pil_image = Image.fromarray(image)
                d = ImageDraw.Draw(pil_image)
                textResult = ""
                for facial_feature in facial_features:
                    print("The {} in face {} has the following points: {}".format(facial_feature, i, face_landmarks[facial_feature]))
                    d.line(face_landmarks[facial_feature], width=3)
                    #textResult += face_landmarks[facial_feature] + "\n"
                    #d.point(face_landmarks[facial_feature])
                pil_image.save(os.path.join(app.config['UPLOAD_FOLDER'], "{}_out.jpg".format( os.path.splitext(filename)[0])))

            imageOut = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], "{}_out.jpg".format( os.path.splitext(filename)[0])))
            return render_template('index.html', result = True, image_in=imageIn, image_out=imageOut, tagResult=face_landmarks_list)

        else:
            return render_template('index.html', result = True, image_in=imageIn)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        #return redirect(url_for('uploaded_file', filename="{}_out.jpg".format(os.path.splitext(filename)[0])))
    else:
        return redirect('/')

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("5000"),
        debug=False
    )
