from PIL import Image, ImageDraw

import face_recognition

image = face_recognition.load_image_file("/mnt/docker-face-detection/083_084.jpg")
face_landmarks_list = face_recognition.face_landmarks(image)
print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

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
    for facial_feature in facial_features:
        print("The {} in face {} has the following points: {}".format(facial_feature, i, face_landmarks[facial_feature]))
        #d.line(face_landmarks[facial_feature])
        d.point(face_landmarks[facial_feature])
    pil_image.save("{}.jpg".format(i))
