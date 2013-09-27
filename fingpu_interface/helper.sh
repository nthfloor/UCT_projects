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

if [ $1 == "-b" ]
then
    echo "building executable"
    ~/programs/PyInstaller-2.1/pyinstaller.py --distpath=~/Repo/uct_projects/fingpu_interface/dist -n FinGPU-gui -F runapp.py
fi

