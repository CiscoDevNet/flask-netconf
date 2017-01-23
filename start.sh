#!/bin/sh

#
# bootstrap the virtual env if necessary
#
if [ -f "v/bin/activate" ]
then
    echo virtual env already created
else
    virtualenv v
fi
source v/bin/activate

# Just install dependencies by default to pick up any changes
pip install -r requirements.txt

#
# run the data server
#
python app.py --path ./models

