@echo off
REM ###################################
REM           start_dev.bat
REM ###################################

REM Nom du projet Docker Compose
set PROJECT_NAME=esaipctf-webhook

REM Supprimer les anciens conteneurs et images associés au docker-compose
docker compose -p %PROJECT_NAME% down --rmi local --volumes

REM Redémarrer les conteneurs
docker compose -p %PROJECT_NAME% up -d --build