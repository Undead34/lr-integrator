import schedule

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .build_integrations import Integration

class Scheduler:
    def __init__(self):
        pass

    def _process(self, integration: 'Integration'):
        integration.write()

    def add(self, integration: 'Integration'):
        schedule.every(integration.interval).seconds.do(self._process, integration)

    def run(self):
        while True:
            schedule.run_pending()
        
