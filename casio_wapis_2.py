import os
from pathlib import Path

rutaDiscoDuro = "\\\\192.168.1.254\\W\\Multimedia\\Casio\\Relojes"
item = "A158WEA-1EF"


if os.path.exists(Path(rutaDiscoDuro + "\\" + item)):
    print("La carpeta del articulo {} ya existe".format(item))
else:
    os.mkdir(rutaDiscoDuro + "\\" + item)