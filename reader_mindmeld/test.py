#!/usr/bin/env python
# test.py
# VERSION 1.0 : LAST_CHANGED 2020-05-27

# Script to build and evaluate given test.txt files
# Call with $ python cb_test.py in virtualenv
# https://www.mindmeld.com/docs/userguide/nlp.html#evaluate-nlp-performance

exec(open("train.py").read())
print(nlp.evaluate())