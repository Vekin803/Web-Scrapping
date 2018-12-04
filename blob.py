import base64
from pathlib import Path

#  ("A158WEA-1EF/A158WEA-1EF.jpg", "rb")
with open(Path('A158WEA-1EF/A158WEA-1EF.jpg'), 'rb') as imageFile:
    imgcode = base64.b64encode(imageFile.read())
    print(dir(imageFile))
    print(imageFile.read())

# fh = open("imageToSave.png", "wb")
# fh.write(base64.b64decode(str))
# fh.close()

imgcode = base64.b64encode(data.content)
fh = open("imageToSave.png", "wb")
fh.write(base64.b64decode(imgcode))
fh.close()
