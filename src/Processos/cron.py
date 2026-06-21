import logging

from Processos.services import sincronizar_processos_legislativos

logger = logging.getLogger(__name__)


def sincronizar_bases_cron():
    """
    Função chamada pelo django_crontab para sincronização periódica
    dos processos legislativos da Câmara e do Senado.

    Configurada em settings.py CRONJOBS para rodar de hora em hora.
    """
    try:
        novos = sincronizar_processos_legislativos()
        logger.info("Sincronização cron concluída: %d processos criados", novos)
    except Exception as exc:
        logger.error("Erro na sincronização cron: %s", exc, exc_info=True)
