# make zip file of everything in this directory except .env and .git and .gitignore
import os
import zipfile
import shutil
import sys


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        if root.startswith('.\.git') or root.startswith('.\.test'):
            continue
        for file in files:
            if file != '.env' and file != '.gitignore' and file != '.git' and file != "build.zip" and file != "setup.py":
                ziph.write(os.path.join(root, file))


if __name__ == '__main__':
    zipf = zipfile.ZipFile('build.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('.', zipf)
    zipf.close()
