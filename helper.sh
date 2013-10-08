#!/bin/bash

if [ $# -eq 0 ]
then
    exit "No arguments supplied"
fi

if [ $1 == "-m" ]
then
    if [ -z $2 ]
    then
        exit "Need to supply branch name"
    fi
    echo "merging with master"
    git commit -a
    git checkout master
    git merge $2
    git push
    git checkout $2
fi

if [ $1 == "-tar" ]
then
    tar -cvzf fingpu-gui1.tar.gz *.py
    echo "compressing files"
fi

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

if [ $1 == "-o" ]
then
    echo "building executable"
    ~/programs/PyInstaller-2.1/pyinstaller.py --distpath=~/Repo/uct_projects/fingpu_interface -n FinGPU-gui -F runapp.py
fi

if [ $1 == "-d" ]
then
   echo "One Directory"
   ~/programs/PyInstaller-2.1/pyinstaller.py --distpath=~/Repo/uct_projects/fingpu_interface/dist -n FinGPU-gui runapp.py
fi

