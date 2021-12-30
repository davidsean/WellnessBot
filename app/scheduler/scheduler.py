#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scheduler
=========
Modified: 2020-05-22
Dependencies:
-------------
```
import numpy as np
import time
import logging
```
Copyright © 2021 Incuvers. All rights reserved.
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""
import asyncio
import logging
import time
from tabulate import tabulate
import threading_sched as sched


class Scheduler:
    """
    Creates scheduler objects for executing image captures (experiment) and setpoint changes
    (protocol) at precise instances in time.
    """

    def __init__(self):
        """
        Create a new scheduler object and accompanying runner thread.
        """
        self._log = logging.getLogger(__name__)
        self.sch = sched.scaled_scheduler(time.time, time.sleep)
        # start the scheduler on init (raises RuntimeError on failure)
        # scheduler is always active while main thread is active
        self._log.debug(self)

    def __str__(self) -> str:
        """
        Scheduler represented by its queue using the 'tabulate' library
        """
        return "\n" + str(tabulate(
            self.sch.queue, headers=['Time', 'Priority', 'Action', 'Argument', 'kwargs'], floatfmt=(".3f")
        ))

    async def _runner(self) -> None:
        """
        This method is called @ Scheduler __init__ and executes the scheduler runner which executes
        the scheduled events at the scheduled time.
        """
        # loop active while main thread is live: Once __main__ exits the thread terminates
        while True:
            if self.sch.empty():
                # TEMP while no protocol setpoints are pending (IDLE state)
                asyncio.sleep(1)
            else:
                try:
                    self.sch.run()
                except BaseException as exc:  # temp raise
                    self._log.exception("Scheduler encountered a callback execution problem: %s",
                                        exc)

    def populate(self, time: int, priority: int, callback, args={}):
        """
        Schedules the payload events into the scheduler. Executed once a payload is set to exec
        Note: for the current version all scheduled events are uneditable once they are set.
        :param time: absolute epoch time to execute the setpoint change event
        :param priority: protocol layer selection (no purpose here)
        :param callback: scheduled callback event
        :param args: arguments for callback event
        """
        self.sch.enterabs(time, priority, callback, argument=args, kwargs={})
        self._log.debug("Added callback: %s to scheduler at time: %s and priority: %s",
                        callback, time, priority)

    def purge_queue(self):
        """
        Purges scheduler of all scheduled events.
        :raises: RuntimeError
        """
        for _, event in enumerate(self.sch.queue):
            self.sch.cancel(event)
            self._log.info("Cancelled event: %s", event)
