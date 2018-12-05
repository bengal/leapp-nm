#!/usr/bin/env python

import subprocess
import re
import gi
gi.require_version('NM', '1.0')
from gi.repository import GLib, NM

def is_hexstring(s):
    arr = s.split(':')
    for a in arr:
        if len(a) != 1 and len(a) != 2:
            return False
        try:
            h = int(a, 16)
        except ValueError as e:
            return False
    return True

dhcp_client = 'dhclient'
subp = subprocess.Popen(('/usr/sbin/NetworkManager', '--print-config'), stdout=subprocess.PIPE)
conf, err = subp.communicate()
pattern = r'^\s*dhcp=(\w+)\s*$'
match = re.search(pattern, conf.decode('utf-8'), re.M)
if match:
    dhcp_client = match.group(1)

client = NM.Client.new(None)

if dhcp_client != 'dhclient':
    exit(0)

for c in client.get_connections():
    print(' * processing connection {} ({})'.format(c.get_uuid(), c.get_id()))
    s_ip4 = c.get_setting_ip4_config()
    client_id = s_ip4.get_dhcp_client_id()
    if client_id is not None:
        print('  - client id : {}'.format(client_id))
        if not is_hexstring(client_id):
            new_client_id = ':'.join(hex(ord(x))[2:] for x in client_id)
            print('  - new       : {}'.format(new_client_id))
            s_ip4.set_property(NM.SETTING_IP4_CONFIG_DHCP_CLIENT_ID, new_client_id)
            c.commit_changes(True, None)
