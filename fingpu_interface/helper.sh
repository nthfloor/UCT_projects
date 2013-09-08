#!/bin/bash

# sample code
# if [ $1 == "-m" ]
# then
#     echo "msg here"
# fi

if [ $1 == "-c" ]
then
    rm *.pyc
    echo "cleaned directory"
fi

if [ $1 == "-r" ]
then
    echo "runapp"
    python runapp.py
fi

