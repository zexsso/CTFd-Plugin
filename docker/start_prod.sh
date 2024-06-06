#!/bin/bash

#########################################
#               StartProd               #
#########################################

# Nom du projet Docker Compose
PROJECT_NAME="esaipctf-webhook"

# Supprimer les anciens conteneurs et images associés au docker-compose
docker compose -p $PROJECT_NAME down --rmi local --volumes

# Redémarrer les conteneurs
docker compose -p $PROJECT_NAME up -d --build