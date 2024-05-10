#!/bin/bash
wget https://bootstrap.pypa.io/virtualenv/3.11/virtualenv.pyz
python3 virtualenv.pyz venv
source venv/bin/activate
pip install -r requirements.txt