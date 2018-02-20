#!/bin/bash
sudo rm ../images/*
sleep 2
sudo python PythonCap.py
sleep 2
git add ../images/
git commit -m "push img automated script"
git push origin master

