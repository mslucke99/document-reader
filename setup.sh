# pip install tesseract-ocr
# pip install opencv
pip3 install --upgrade pip
pip3 install -r requirements.txt
wget https://www.dropbox.com/s/r2ingd0l3zt8hxs/frozen_east_text_detection.tar.gz?dl=1
tar -xvzf frozen_east_text_detection.tar.gz

echo "You may need to install tesseract on your system and set it up in your PATH environment variable."