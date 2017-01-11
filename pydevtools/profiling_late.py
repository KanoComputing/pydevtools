# profiling_late.py
#
# Copyright (C) 2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
#

'''
Module to enable profiling timepoints. This module is loaded
only if the configuration file exists, see profiling.py for more information
'''

import os
import sys
import yaml
import cProfile

from profiling import CONF_FILE, defaultConf

# load the configuration file or set default builtin settings
try:
    with open(CONF_FILE, 'r') as inp_conf:
        conf = yaml.load(inp_conf)
except:
    conf = yaml.safe_dump(defaultConf)

myProfile = cProfile.Profile()
app_name = sys.argv[0]
point_current = ""


def has_key(d, k):
    return type(d) is dict and k in d


def declare_timepoint(name, isStart):
    global myProfile
    global point_current
    cmd = None
    pythonProfile = False

    # Check if the app is contained in the profiling conf file
    if has_key(conf, app_name):
        # Check if the timepoint name is contained in the profiling conf file
        if has_key(conf[app_name], name):
            ct = conf[app_name][name]

            # Check if python profiler should be started for this timepoint
            if has_key(ct, 'python'):
                pythonProfile = True
                if isStart:
                    if point_current:
                        print 'Stop profiling for point "{0}" and do "{1}" instead'.format(point_current, name)
                        myProfile.disable()
                        myProfile.clear()
                    point_current = name
                    myProfile.enable()
                else:
                    if point_current != name:
                        print 'Can\'t stop point "{0}" since a profiling session for "{1}" is being run'.format(name, point_current)
                    else:
                        myProfile.disable()
                        # Check if the statfile location in specified
                        if ct['python']['statfile']:
                            try:
                                myProfile.dump_stats(ct['python']['statfile'])
                            except IOError as e:
                                if e.errno == 2:
                                    print 'Path to "{}" probably does not exist'.format(ct['python']['statfile'])
                                else:
                                    print 'dump_stats IOError: errno:{0}: {1} '.format(e.errno, e.strerror)
                        else:
                            print 'No statfile entry in profiling conf file "{}"'.format(CONF_FILE)
                        myProfile.clear()
                        point_current = ""
            else:
                print 'Profiling conf file doesnt enable the Python profiler for point {} at app {}'.format(name, app_name)

            # Check if we want to run some other command at this timepoint
            if isStart and has_key(ct, 'start_exec'):
                cmd = ct['start_exec']
                os.system(cmd)
            if not isStart and has_key(ct, 'end_exec'):
                cmd = ct['end_exec']
                os.system(cmd)
        else:
            print 'Profiling conf file doesnt include point:{} for app {}'.format(name, app_name)
    else:
        print 'Profiling conf file doesnt include app:{}'.format(app_name)

    print 'timepoint ', name, name, isStart, cmd, pythonProfile
