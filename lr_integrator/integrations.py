from typing import Optional, Iterator
from .build_integrations import BuildIntegrations
from .constants import DEFAULT_CONFIG_PATH

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .build_integrations import Integration

class Integrations:
    integrations: list['Integration']

    def __init__(self, cfg_path: Optional[str] = None):
        cfg_path = cfg_path if cfg_path is not None else DEFAULT_CONFIG_PATH
        self.integrations = BuildIntegrations(cfg_path).load_integrations()

    def __iter__(self) -> Iterator:
        return iter(self.integrations)
