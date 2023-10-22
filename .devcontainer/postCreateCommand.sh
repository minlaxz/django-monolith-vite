#!/bin/bash

set -euo pipefail

sudo chown vscode:vscode /workspaces/django-monolith-vite/django_monolith_vite/frontend/node_modules

cd /workspaces/django-monolith-vite/django_monolith_vite/frontend && yarn
cd /workspaces/django-monolith-vite/django_monolith_vite/ && pip install -r requirements.txt
