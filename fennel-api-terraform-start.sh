#!/bin/bash
sudo apt-get update
sudo apt-get install -y docker.io
export DEBUG=False
export ADMIN_NAME="Fennel Labs"
export ADMIN_EMAIL="info@fennellabs.com"
export EMAIL_HOST=smtp.sendgrid.net
export EMAIL_PORT=465
export EMAIL_USERNAME=apikey
export EMAIL_PASSWORD=$(gsutil cat gs://whiteflag-0-admin/email_password.sh)
export DEFAULT_FROM_EMAIL="info@fennellabs.com"
export SERVER_EMAIL="info@fennellabs.com"
export SECRET_KEY=$(gsutil cat gs://whiteflag-0-admin/api-secret-key.sh)
export POSTGRES_DB=$(gsutil cat gs://whiteflag-0-admin/postgres_db.sh)
export POSTGRES_USER=postgres
export POSTGRES_PASS=$(gsutil cat gs://whiteflag-0-admin/postgres_pass.sh)
export POSTGRES_NAME=fennel_api
gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin us-east1-docker.pkg.dev
docker run -dit -e DEBUG -e ADMIN_NAME -e ADMIN_EMAIL -e EMAIL_HOST -e EMAIL_PORT -e EMAIL_USERNAME -e EMAIL_PASSWORD -e DEFAULT_FROM_EMAIL -e SERVER_EMAIL -e SECRET_KEY -e POSTGRES_DB -e POSTGRES_USER -e POSTGRES_PASS -e POSTGRES_NAME -e FENNEL_CLI_IP -e FENNEL_API_IP -e FENNEL_KEYSERVER_IP -e FENNEL_SUBSERVICE_IP -p 80:1234 --name fennel-api us-east1-docker.pkg.dev/whiteflag-0/fennel-docker-registry/fennel-api:latest
docker exec -it fennel-api /opt/app/build-dev.sh