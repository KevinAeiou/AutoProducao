import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
import tempfile

class MeuLogger:
    def __init__(self, nome: str, arquivoLogger: str= 'aplicacao.log', nivel: int = logging.DEBUG, bytesMax: int=10485760, contadorBackup: int= 5):
        self.__logger = logging.getLogger(nome)
        self.__logger.setLevel(level= nivel)
        formatador = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        formatador.datefmt = '%d/%m/%Y %I:%M:%S %p'
        if arquivoLogger:
            try:
                caminhoLogger: str= 'logs'
                arquivoLogger= caminhoLogger + '/' + arquivoLogger
                if not os.path.exists(arquivoLogger):
                    os.makedirs(arquivoLogger)
                    with open(arquivoLogger, 'w', encoding= 'utf-8') as arquivo:
                        arquivo.write('')
                if self.__logger.handlers:
                    self.__logger.handlers.clear()
                file_handler = RotatingFileHandler(arquivoLogger, maxBytes= bytesMax, backupCount=contadorBackup, encoding= 'utf-8')
                file_handler.setFormatter(formatador)
                self.__logger.addHandler(file_handler)
            except PermissionError as e:
                temp_log = Path(tempfile.gettempdir()) / 'AutoProducao' / arquivoLogger
                temp_log.parent.mkdir(parents=True, exist_ok=True)
                if self.__logger.handlers:
                    self.__logger.handlers.clear()
                file_handler = RotatingFileHandler(
                    str(temp_log),
                    maxBytes=bytesMax,
                    backupCount=contadorBackup,
                    encoding='utf-8'
                )
                file_handler.setFormatter(formatador)
                self.__logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatador)
        self.__logger.addHandler(console_handler)

    def debug(self, menssagem: str):
        self.__logger.debug(msg= menssagem)

    def info(self, menssagem: str):
        self.__logger.info(msg= menssagem)

    def warning(self, menssagem: str):
        self.__logger.warning(msg= menssagem)

    def error(self, menssagem: str):
        self.__logger.error(msg= menssagem)

    def critical(self, menssagem: str):
        self.__logger.critical(msg= menssagem)