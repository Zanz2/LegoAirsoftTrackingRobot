#!/bin/bash
fswebcam ../images/slika2.jpg
cd ..
git add *
git commit -m "push img automated script"
git push origin master

