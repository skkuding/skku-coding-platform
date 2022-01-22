#! /bin/bash
set -x

# Install Python packages
python3 -m pip install wheel
python3 -m pip install -r /workspace/backend/deploy/requirements.txt

# Django Setup
echo `cat /dev/urandom | head -1 | md5sum | head -c 32` > /workspace/backend/data/config/secret.key
python3 /workspace/backend/manage.py migrate
python3 /workspace/backend/manage.py inituser --username root --password rootroot --action create_super_admin

# Add `judge-server-dev` container to database
echo "
from conf.models import JudgeServer
from django.utils import timezone

JudgeServer.objects.create(
    hostname='hostname',
    judger_version='version',
    cpu_core=1,
    memory_usage=0,
    cpu_usage=0,
    ip='127.0.0.1',
    service_url='$JUDGE_SERVER_URL',
    last_heartbeat=timezone.now()
)
" | python3 /workspace/backend/manage.py shell

# Register judge server token
echo "
from options.options import SysOptions
SysOptions.judge_server_token='$JUDGE_SERVER_TOKEN'
" | python3 /workspace/backend/manage.py shell

# Install Node packages
yarn --cwd /workspace/frontend install
yarn --cwd /workspace/frontend cypress install
