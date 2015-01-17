#!/bin/bash

# This part uses virtualenv to create a localized python configuration

if [ ! -d venv  ]; then
    virtualenv venv/
fi

. venv/bin/activate

pip install -r requirements.txt
