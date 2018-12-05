#!/usr/bin/env python

import subprocess
import re

dhcp_client = ''
snippet_path = '/usr/lib/NetworkManager/conf.d/10-dhcp-dhclient.conf'
snippet_data = ("# Generated by leapp when upgrading from RHEL7 to RHEL8\n"
                "[main]\n"
                "dhcp=dhclient\n")

# Read the currently configured DHCP client from NetworkManager
# configuration. We use 'NM --print-config' that merges the main
# configuration file and other files in various directories in the
# right way.
subp = subprocess.Popen(('/usr/sbin/NetworkManager', '--print-config'), stdout=subprocess.PIPE)
conf, err = subp.communicate()
pattern = r'^\s*dhcp=(\w+)\s*$'
match = re.search(pattern, conf.decode('utf-8'), re.M)
if match:
    dhcp_client = match.group(1)

print("Current dhcp client: {}".format(dhcp_client))

if dhcp_client == '':
    # If the user didn't explicitly set a client, dhclient was used by
    # default. Drop a configuration snippet to keep it upon upgrade.
    try:
        with open(snippet_path, 'w') as f:
            f.write(snippet_data)
            print("Written the following to {}:\n{}\n".format(snippet_path, snippet_data))
    except IOError as e:
        self.log.warning('Write error: {}...'.format(e))
