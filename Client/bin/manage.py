#!/usr/bin/env python
# coding:utf-8

import os
import sys
BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BaseDir)
from core import main

if __name__ == '__main__':
    EntryPoint = main.Monitor()
