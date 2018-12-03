from leapp.actors import Actor
from leapp.models import NetworkManagerInfo
from leapp.tags import FactsPhaseTag
import subprocess
import re

class NetworkManagerScanner(Actor):
    name = 'network_manager_scanner'
    description = 'This actor provides a basic info about NetworkManager configuration.'
    consumes = ()
    produces = (NetworkManagerInfo,)
    tags = (FactsPhaseTag,)

    def process(self):
        nm_info = self.get_nm_info()
        self.produce(nm_info)
        self.log.info('Finished scanning NM info')

    def get_nm_info(self):
        nm_info = NetworkManagerInfo()
        subp = subprocess.Popen(('/usr/sbin/NetworkManager', '--print-config'), stdout=subprocess.PIPE)
        conf, err = subp.communicate()

        pattern = r'^\s*dhcp=(\w+)\s*$'
        match = re.search(pattern, conf.decode('utf-8'), re.M)
        if match:
            nm_info.dhcp = match.group(1)

        return nm_info
