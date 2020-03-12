import json
import requests
import base64
import io
import urllib.request
from PIL import Image

def encodeImage():
    #Select file here by changing the name of the file
    #Make sure the file is in the same directory as the client
    filename = "spaceneedle.jpg"
    img = Image.open(filename, mode='r')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return encoded_img

def main():
    encoded_img = encodeImage()
    payload = {
        'image' : encoded_img,
        'operations' : "rotate-30,flipVertical,greyScale,rotateLeft,resize-.5"
    }
    jsonPayload = json.dumps(payload)

    postEndpointURL = "http://localhost:5000/transformimage"
    

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url = postEndpointURL, data=jsonPayload, headers=headers)
    img = Image.open(io.BytesIO(response.content))
    img.show()


if __name__ == "__main__":
    main()
