#! /bin/bash
set -x

# Install Python packages
python3 -m pip install wheel
python3 -m pip install -r /workspace/backend/deploy/requirements.txt

# Django Setup
echo `cat /dev/urandom | head -1 | md5sum | head -c 32` > /workspace/backend/data/config/secret.key
python3 /workspace/backend/manage.py migrate
python3 /workspace/backend/manage.py inituser --username root --password rootroot --action create_super_admin

# Install Node packages
yarn --cwd /workspace/frontend install
