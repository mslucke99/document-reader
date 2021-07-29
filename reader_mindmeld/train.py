#!/usr/bin/env python
# train.py
# originally cb_train.py
# VERSION 1.01 : LAST_CHANGED 2020-07-28

# Script to build everything
# Call with $ python cb_train.py in virtualenv
# https://www.mindmeld.com/docs/userguide/nlp.html
# https://www.mindmeld.com/docs/quickstart/07_train_the_natural_language_processing_classifiers.html

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

from mindmeld.components.nlp import NaturalLanguageProcessor
import mindmeld as mm
mm.configure_logs()
nlp = NaturalLanguageProcessor(app_path=".")
nlp.build()
nlp.dump()