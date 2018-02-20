#!/bin/bash
rm ../images/*
sudo python PythonCap.py
sleep 2
git add ../images
git commit -m "push img automated script"
git push origin master

