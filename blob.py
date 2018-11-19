import base64
 
with open("AW-590-1AER/AW-590-1AER.jpg", "rb") as imageFile:
    str = base64.b64encode(imageFile.read())
    # print(str)

fh = open("imageToSave.png", "wb")
fh.write(base64.b64decode(str))
fh.close()
