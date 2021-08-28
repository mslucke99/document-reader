sudo apt install tesseract-ocr python3-pyaudio
pip3 install --upgrade setuptools pip pipenv
pipenv install

wget https://www.dropbox.com/s/r2ingd0l3zt8hxs/frozen_east_text_detection.tar.gz
tar -xvzf frozen_east_text_detection.tar.gz

echo "You may need to install tesseract on your system and set it up in your PATH environment variable."