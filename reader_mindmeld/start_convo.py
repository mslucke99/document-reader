#!/usr/bin/env python
# start_convo.py
# VERSION 1.0 : LAST_CHANGED 2021-07-29         # literally one year later than previously exactly

# Script to build and run interactive testing, conversationally
# Call with $ python demo_convo.py -train in virtualenv
# https://www.mindmeld.com/docs/userguide/nlp.html#run-the-nlp-pipeline
# https://www.mindmeld.com/docs/blueprints/home_assistant.html

from mindmeld.components.dialogue import Conversation
from mindmeld.components.nlp import NaturalLanguageProcessor
import sys

if (sys.argv.count('-train')):
    exec(open("train.py").read())
else:
    nlp = NaturalLanguageProcessor(app_path=".")
    nlp.load()
conv = Conversation(nlp=nlp, app_path=".")

# read events from tsv, may or may not be done in final afternoon workflow
#TODO implement

print("Convo Demo: Ctrl-C to exit\n")
# 1: Greetings exchanged
# can easily be replaced with an exchange of greetings
resp = "Hello, what do you need assistance with?\n"
query = input(resp)
resp = conv.say(query)[0] + "\n >>> "

while True:
  query = input(resp)
  resp = conv.say(query)[0] + "\n >>> "