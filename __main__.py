#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

if sys.version_info < (3, 10):
    print("LogRhythm Report Tool requires Python 3.10 or higher.")
    sys.exit(1)

from lr_integrator import Integrations, Scheduler, logger

def run():
    integrations  = Integrations()
    scheduler = Scheduler()

    for integration in integrations:
        scheduler.add(integration)
    
    scheduler.run()

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        logger.log("Keyboard Interrupt")
        sys.exit(0)
    except Exception as e:
        logger.error(f"{e}")
        sys.exit(1)
