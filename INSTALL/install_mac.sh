#!/bin/bash
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it from https://www.python.org/"
    exit
fi
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install ntplib
echo "Installation complete. To run the server:"
echo "source venv/bin/activate && python3 time_server.py"
