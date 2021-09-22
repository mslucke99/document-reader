# layoutdetection.py
#
# author: Michael Lucke
# last edited: 2021/09/22
# 
# notes
# some of this code is from https://huggingface.co/transformers/model_doc/layoutlmv2.html

from transformers import LayoutLMv2Processor
from PIL import Image

TESTING = True
processor = LayoutLMv2Processor.from_pretrained("microsoft/layoutlmv2-base-uncased")

#image = Image.open("name_of_your_document - can be a png file, pdf, etc.").convert("RGB")
#question = "What's his name?"
#encoding = processor(image, question, return_tensors="pt")
#print(encoding.keys())
# dict_keys(['input_ids', 'token_type_ids', 'attention_mask', 'bbox', 'image'])

def process(image, question):
    encoding = processor(image, question, return_tensors="pt")
    return encoding

def test():
    question="This is a placeholder"
    import cv2 as cv
    cap = cv.VideoCapture(0)
    hasFrame, frame = cap.read()
    if hasFrame:
        processoutput = process(frame, question)
        print(processoutput.keys())
        for key in processoutput.keys():
            print(processoutput[key])


if TESTING:
    test()