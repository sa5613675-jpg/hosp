#!/bin/bash
cd /workspaces/hosp
git add -A
git commit -m "Feature: Pharmacy Management UI with sales and profit tracking"
git push origin $(git branch --show-current)
python manage.py runserver 0.0.0.0:8000
