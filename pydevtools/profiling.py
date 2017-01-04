# -*- coding: utf-8 -*-
"""
  pydevtools.profiling
  ~~~~~~~~~~~~~~~~~~~~
  :copyright: (c) 2017 Kano Computing Ltd.
  :license: GPL, see LICENSE for more details.

This module is intended to allow profiling of individual 'transitions'.
It should be low overhead if its configuration file does not exist, which
will be the case on production images.

For this reason the main logic is in a different module, profiling_late,
which is only loaded if the configuration file is detected.

To declare a transition, at the start do
  declare_timepoint("transition_name",True)
and at the end do
  declare_timepoint("transition_name",False)

The configuration file can enable profiling for each individual time point.

Example 1: Enable python profiling in the "load" timepoint of make-pong,
saving the profile data to /tmp/make-pong/load.prof

/usr/bin/make-pong:
    load:
        python:
            statfile: /tmp/make-pong-load.prof

Example 2: Run a command at start and end of a timepoint (e.g. perf or bootchartd)

/usr/bin/make-pong:
    load:
        start_exec:
            touch /tmp/pong_load_started
        end_exec:
            touch /tmp/pong_load_ended
"""

import os
CONF_FILE = '/etc/kano-profiling.conf'

isConf = os.path.exists(CONF_FILE)


def declare_timepoint(name, isStart):
    if not isConf:
        return
    else:
        import kano.profiling_late
        kano.profiling_late.declare_timepoint(name, isStart)
