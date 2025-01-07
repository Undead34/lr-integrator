import os
import logging

from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from logging.handlers import RotatingFileHandler

import toml
import humanfriendly

from .constants import INTEGRATION_LOGGER_PATH

# Clase base abstracta para cualquier integración
class Integration(ABC):
    def __init__(self, interval: int):
        self.interval = interval

    @abstractmethod
    def write(self):
        pass


# Ejemplo de una clase específica para integraciones REST
class APIRESTIntegration(Integration):
    def __init__(
        self,
        name: str,
        interval: int,
        endpoint: str,
        method: str,
        headers: dict,
        querystring: dict,
        auth_type: str,
        auth_token: str,
        auth_expiration: str,
        pagination_strategy: str,
        pagination_next_key: str,
        pagination_elements_key: str,
        logger: logging.Logger
    ):
        super().__init__(interval)
        self.name = name
        self.endpoint = endpoint
        self.method = method
        self.headers = headers
        self.querystring = querystring
        self.auth_type = auth_type
        self.auth_token = auth_token
        self.auth_expiration = auth_expiration
        self.pagination_strategy = pagination_strategy
        self.pagination_next_key = pagination_next_key
        self.pagination_elements_key = pagination_elements_key
        self.logger = logger
        self.results: list[str] = [""]

    def write(self):
        for r in self.results:
            self.logger.info(r)

# Fábrica de integraciones
class BuildIntegrations:
    def __init__(self, cfg_path: Optional[str]):
        self.config_file = toml.load(cfg_path)
        self.integrations: List[Integration] = []
        self._parse_config()

    def _parse_config(self):
        sources = self.config_file.get("sources", [])

        if isinstance(sources, dict):
            sources = [sources]

        for source in sources:
            try:
                name = source.get("name", "undefined")
                source_type = source.get("type")
                interval = source.get("interval", 60)
                enabled = source.get("enabled", False)

                if not enabled:
                    continue

                if source_type == "rest":
                    config: dict = source.get("config")

                    # Config
                    endpoint = config.get("endpoint")
                    method = config.get("method")
                    headers = config.get("headers")
                    querystring = config.get("querystring")

                    # Autenticación
                    authentication: dict = config.get("authentication")
                    auth_type = authentication.get("type")
                    auth_token = authentication.get("token")
                    auth_expiration = authentication.get("expiration")

                
                    # Config de paginación
                    pagination: dict = config.get("pagination")
                    pagination_strategy = pagination.get("strategy")
                    pagination_next_key = pagination.get("next_key")
                    pagination_elements_key = pagination.get("elements_key")


                    # Logger
                    logger: dict = config.get("logger")
                    logger_max_files = logger.get("max_files", 5)
                    logger_size = logger.get("size", "10MB")

                    logger = self._get_logger(name, logger_max_files, logger_size)

                    # Creamos instancia de nuestra integración REST
                    integration = APIRESTIntegration(
                        name,
                        interval,
                        endpoint,
                        method,
                        headers,
                        querystring,
                        auth_type,
                        auth_token,
                        auth_expiration,
                        pagination_strategy,
                        pagination_next_key,
                        pagination_elements_key,
                        logger
                    )

                    self.integrations.append(integration)
                else:
                    print(f"Tipo de fuente '{source_type}' no soportado todavía.")
                    continue
            except Exception as e:
                logging.getLogger(__name__).error("{e}")

    def load_integrations(self) -> List[Integration]:
        """
        Retorna la lista de integraciones que se generaron a partir del TOML.
        """
        return self.integrations

    def _get_logger(self, name, max_files, size) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        log_file = INTEGRATION_LOGGER_PATH.format(name, name)
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        max_file_size_bytes = humanfriendly.parse_size(size)

        file_handler = RotatingFileHandler(log_file, maxBytes=max_file_size_bytes, backupCount=max_files, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger
