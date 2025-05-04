import logging
import os
from pathlib import Path
import tempfile
import time
from datetime import datetime
import platform

class TimestampedFileHandler(logging.FileHandler):
    """
    Handler que cria um novo arquivo de log com timestamp quando atinge o tamanho máximo
    """
    def __init__(self, filename, max_bytes=10485760, encoding='utf-8'):
        self.max_bytes = max_bytes
        self.base_filename = filename
        self.current_filename = self._get_new_filename()
        Path(self.current_filename).parent.mkdir(parents=True, exist_ok=True)
        super().__init__(self.current_filename, encoding=encoding)

    def _get_new_filename(self):
        """Gera um novo nome de arquivo com timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base, ext = os.path.splitext(self.base_filename)
        return f"{base}_{timestamp}{ext}"

    def emit(self, record):
        """Verifica o tamanho do arquivo antes de escrever"""
        if self.should_rollover(record):
            self.do_rollover()
        super().emit(record)

    def should_rollover(self, record):
        """Determina se precisa criar um novo arquivo"""
        if self.stream is None:
            return False
        msg = self.format(record)
        return self.stream.tell() + len(msg.encode('utf-8')) > self.max_bytes

    def do_rollover(self):
        """Fecha o arquivo atual e abre um novo"""
        if self.stream:
            self.stream.close()
        self.current_filename = self._get_new_filename()
        self.stream = self._open()

class MeuLogger:
    def __init__(self, nome: str, arquivo_logger: str = 'aplicacao.log', 
                 nivel: int = logging.DEBUG, bytesMax: int = 10485760):
        self.__logger = logging.getLogger(nome)
        self.__logger.setLevel(level=nivel)
        
        # Configuração do formatador
        formatador = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        
        # Configuração do arquivo de log
        if arquivo_logger:
            self._configure_file_handler(arquivo_logger, formatador, bytesMax)
        
        # Configuração do console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatador)
        self.__logger.addHandler(console_handler)
        
        # Garante que não há handlers duplicados
        self._remove_duplicate_handlers()

    def _configure_file_handler(self, arquivo_logger, formatador, bytesMax):
        """
        Configura o handler de arquivo com fallback para diretório temporário
        """
        primary_path = Path('logs') / arquivo_logger
        fallback_path = Path(tempfile.gettempdir()) / 'AutoProducao' / 'logs' / arquivo_logger
        
        # Tenta primeiro o caminho principal
        try:
            handler = TimestampedFileHandler(
                str(primary_path),
                max_bytes=bytesMax,
                encoding='utf-8'
            )
            handler.setFormatter(formatador)
            self.__logger.addHandler(handler)
            return
        except (PermissionError, OSError) as e:
            print(f"Falha ao acessar {primary_path}: {e}")
        
        # Fallback para diretório temporário
        try:
            handler = TimestampedFileHandler(
                str(fallback_path),
                max_bytes=bytesMax,
                encoding='utf-8'
            )
            handler.setFormatter(formatador)
            self.__logger.addHandler(handler)
            print(f"Usando diretório temporário para logs: {fallback_path}")
        except Exception as e:
            print(f"Falha crítica ao configurar logger de arquivo: {e}")

    def _remove_duplicate_handlers(self):
        """
        Remove handlers duplicados do mesmo tipo
        """
        handlers = self.__logger.handlers
        seen = set()
        
        for handler in handlers[:]:
            key = (type(handler), getattr(handler, 'base_filename', None))
            if key in seen:
                self.__logger.removeHandler(handler)
            else:
                seen.add(key)

    def debug(self, mensagem: str):
        self.__logger.debug(msg=mensagem)

    def info(self, mensagem: str):
        self.__logger.info(msg=mensagem)

    def warning(self, mensagem: str):
        self.__logger.warning(msg=mensagem)

    def error(self, mensagem: str):
        self.__logger.error(msg=mensagem)

    def critical(self, mensagem: str):
        self.__logger.critical(msg=mensagem)