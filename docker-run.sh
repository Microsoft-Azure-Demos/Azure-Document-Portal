#!/bin/bash

docker run -d \
  --name document-portal \
  -p 80:8000 \
  --env-file .env \
  --restart unless-stopped \
  azure-document-portal:1.3