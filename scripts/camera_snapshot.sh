#!/bin/bash
cd ..
sleep 5
fswebcam /images/slika2.jpg
sleep 5
git add *
git commit -m "push img automated script"
git push origin master

