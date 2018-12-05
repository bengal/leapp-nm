#!/usr/bin/env python

import os
import six
import subprocess
from subprocess import CalledProcessError

def call(args, split=True):
    ''' Call external processes with some additional sugar '''
    r = None
    with open(os.devnull, mode='w') as err:
        if six.PY3:
            r = subprocess.check_output(args, stderr=err, encoding='utf-8')
	else:
            r = subprocess.check_output(args, stderr=err).decode('utf-8')
    if split:
        return r.splitlines()
    return r

def unit_enabled(name):
    try:
        ret_list = call(['systemctl', 'is-enabled', name])
        enabled = ret_list[0] == 'enabled'
    except CalledProcessError:
        enabled = False
    return enabled

nm_enabled = unit_enabled('NetworkManager.service')
nmwo_enabled = unit_enabled('NetworkManager-wait-online.service')

print('SERVICES STATE:')
print(' * NetworkManager service enabled             : {}'.format(nm_enabled))
print(' * NetworkManager-wait-online service enabled : {}'.format(nmwo_enabled))

if not nm_enabled and nmwo_enabled:
    print('Disabling NetworkManager-wait-online.service')

    call(['systemctl', 'disable', 'NetworkManager-wait-online.service'])

    print('SERVICES STATE:')
    print(' * NetworkManager service enabled             : {}'.format(unit_enabled('NetworkManager.service')))
    print(' * NetworkManager-wait-online service enabled : {}'.format(unit_enabled('NetworkManager-wait-online.service')))
