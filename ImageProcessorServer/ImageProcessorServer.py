import flask
import base64
import io
import constants
from PIL import Image
from flask import jsonify, send_file, request


app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Logic for opening image from directory (CLIENT)
#ENCODES INTO STRING AND ALLOWS YOU TO PLACE INTO JSON
# filename = "spaceneedle.jpg"
# img = Image.open(filename, mode='r')
# img_byte_arr = io.BytesIO()
# img.save(img_byte_arr, format='JPEG')
# encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')


#GRAB THE IMG FROM POST ENDPOINT, DECODE AND MANIPULATE IT (SERVER)


# Convert the color image to grey scale image
def greyScale(img):
    greyScaleImage = img.convert("L")
    return greyScaleImage

# Rotate the image by n degrees
def rotate(img, degrees):
    rotated = img.rotate(degrees)
    return rotated

# Rotate image left
def rotateLeft(img):
    rotateLeft  = img.transpose(Image.ROTATE_90)
    return rotateLeft

# Rotate image right
def rotateRight(img):
    rotateRight = img.transpose(Image.ROTATE_270)
    return rotateRight

# Flip image left/right
def flipHorizontal(img):
    flipHorizontal = img.transpose(Image.FLIP_LEFT_RIGHT)
    return flipHorizontal

# Flip image up/down
def flipVertical(img):
    flipVertical = img.transpose(Image.FLIP_TOP_BOTTOM)
    return flipVertical

# Resize image, n must be greater than 0
# To half, the width and height of image n = 0.5
def resize(img, percentage):
    resizedImage = img.resize((round(img.size[0]*percentage), round(img.size[1]*percentage)))
    return resizedImage

# Generates a thumbnail that is 128 x 128 of the photo
def generateThumbnail(img):
    size = 128, 128
    thumbnail = img.thumbnail(size)
    return thumbnail



#KEY WORDS: flipVertical, flipHorizontal, rotateLeft, rotateRight, greyScale, rotate-90, resize-.5
# payload = {
#     'image' : encoded_img,
#     'operations' : "rotate-30"
# }

@app.route('/transform', methods=['GET'])
def transform():
    payload = {
         'image' : encoded_img,
         'operations' : "rotate-30"
     }
    operations = payload['operations']
    img2 = Image.open(io.BytesIO(base64.b64decode(encoded_img)))
    oplist = operations.split(",")

    for op in oplist:
        if op == constants.FLIPVERTICAL:
            img2 = flipVertical(img2)
        elif op == constants.FLIPHORIZONTAL:
            img2 = flipHorizontal(img2)
        elif op == constants.ROTATERIGHT:
            img2 = rotateRight(img2)
        elif op == constants.ROTATELEFT:
            img2 = rotateLeft(img2)
        elif op == constants.GREYSCALE:
            img2 = greyScale(img2)
        elif op == constants.GENERATETHUMBNAIL:
            img2 = generateThumbnail(img2)
        elif op.startswith(constants.ROTATE):
            #get substring of after 'rotate-'
            args = op.split('-')
            degrees = int(args[1])
            img2 = rotate(img2, degrees)
        elif op.startswith(constants.RESIZE):
            #get substring of after 'resize-'
            args = op.split('-')
            percentage = float(args[1])
            img2 = resize(img2, percentage)
        else:
            #send error back to user of invalid operation
            print("Invalid Operation")

    img2.show()
    #if unable to split or invalid operation.... send error
    

        # create file-object in memory
    file_object = io.BytesIO()

    # write PNG in file-object
    img2.save(file_object, 'JPEG')

    # move to beginning of file so `send_file()` it will read from start    
    file_object.seek(0)

    return send_file(file_object, mimetype='image/JPEG')
    #return jsonify(payload)

@app.route('/transformimage', methods = ['POST'])
def transformImageHandler():
    # print (request.is_json)
    # content = request.get_json()
    # print (content)
    # return 'JSON posted'
    content = request.get_json()
    #try catch?
    encoded_image = content['image']
    operations = content['operations']
    img3 = Image.open(io.BytesIO(base64.b64decode(encoded_image)))
    oplist = operations.split(",")

    for op in oplist:
        if op == constants.FLIPVERTICAL:
            img3 = flipVertical(img3)
        elif op == constants.FLIPHORIZONTAL:
            img3 = flipHorizontal(img3)
        elif op == constants.ROTATERIGHT:
            img3 = rotateRight(img3)
        elif op == constants.ROTATELEFT:
            img3 = rotateLeft(img3)
        elif op == constants.GREYSCALE:
            img3 = greyScale(img3)
        elif op == constants.GENERATETHUMBNAIL:
            img3 = generateThumbnail(img3)
        elif op.startswith(constants.ROTATE):
            #get substring of after 'rotate-'
            args = op.split('-')
            degrees = int(args[1])
            img3 = rotate(img3, degrees)
        elif op.startswith(constants.RESIZE):
            #get substring of after 'resize-'
            args = op.split('-')
            percentage = float(args[1])
            img3 = resize(img3, percentage)
        else:
            #send error back to user of invalid operation
            print("Invalid Operation")

    #img3.show()
    #if unable to split or invalid operation.... send error
    

        # create file-object in memory
    file_object = io.BytesIO()

    # write PNG in file-object
    img3.save(file_object, 'JPEG')

    # move to beginning of file so `send_file()` it will read from start    
    file_object.seek(0)

    return send_file(file_object, mimetype='image/JPEG')

@app.route('/', methods=['GET'])
def home():
    return 
app.run()
