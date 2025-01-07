from os import path

BASE_DIR_PATH: str = path.realpath(".")
ENTITIES_PATH: str = path.join(BASE_DIR_PATH, "entities")
DEFAULT_CONFIG_PATH: str = path.join(BASE_DIR_PATH, "integrations.toml")
APP_LOGGER_PATH: str = path.join(BASE_DIR_PATH, "logs", "lr-integrator.log")
INTEGRATION_LOGGER_PATH: str = path.join(BASE_DIR_PATH, "logs", "{}", "{}.log")
