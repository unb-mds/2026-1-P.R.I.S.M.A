#!/bin/bash
# entrypoint.sh

# Aplica as variáveis de ambiente atuais ao cron,
# caso contrário o cron do sistema não as enxerga
printenv | grep -v "no_proxy" >> /etc/environment

# Adiciona o cronjob do django_crontab
python src/manage.py crontab add

# Inicia o daemon do cron em background
cron

# Executa o comando principal (por exemplo, runserver)
exec "$@"
