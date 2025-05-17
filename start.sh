#!/bin/bash

# Upgrade pip (no apt!)
pip install -U pip

# Clone the repo to a safe path
if [ -z "$UPSTREAM_REPO" ]; then
  echo "Cloning main Repository"
  git clone https://github.com/MrMKN/PROFESSOR-BOT professorbot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO"
  git clone "$UPSTREAM_REPO" professorbot
fi

# Go to the project directory
cd professorbot || exit

# Install Python dependencies
pip install -U -r requirements.txt --force-reinstall

# Start bot
echo "Starting Bot....✨"
python3 bot.py
