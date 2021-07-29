#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reader_mindmeld __init__.py


"""This module contains a template MindMeld application"""
from mindmeld import Application

app = Application(__name__)

from root import app
#import greeting
#import informative

__all__ = ['app']