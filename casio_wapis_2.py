import os
from pathlib import Path

if os.path.exists(Path('.vscode')):
    print('True')
else:
    print('False')