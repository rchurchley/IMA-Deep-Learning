import cv2


def detectFace(filename):

    # load in haar cascade and attempt to detect a face
    face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face_2 = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    face_3 = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    img = cv2.imread(filename)
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(grayscale, 1.3, 1)

    # try another face if none are detected
    if len(faces) == 0:
        faces = face_2.detectMultiScale(grayscale, 1.3, 1)
    if len(faces) == 0:
        faces = face_3.detectMultiScale(grayscale, 1.3, 1)

    # draw a rectangle for each face in the file
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if len(faces) > 0:
        outfile = filename.split('.')[0] + '_faces.' \
            + filename.split('.')[1]
        cv2.imwrite(outfile)

    print '\nFaces: {}'.format(faces)
    if len(faces) > 0:
        return True
    else:
        return False


def filterImage(filename, filter_type):

    # determine type of filter to use
    if filter_type == 'face':
        return detectFace(filename)
