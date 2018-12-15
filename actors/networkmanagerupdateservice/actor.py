from leapp.actors import Actor
from leapp.tags import ApplicationsPhaseTag, IPUWorkflowTag

import os
import six
import subprocess
from subprocess import CalledProcessError

class NetworkManagerUpdateService(Actor):
    name = 'network_manager_update_service'
    description = 'This actor updates NetworkManager services status when needed.'
    consumes = ()
    produces = ()
    tags = (ApplicationsPhaseTag, IPUWorkflowTag)

    def process(self):
        nm_enabled = self.unit_enabled('NetworkManager.service')
        nmwo_enabled = self.unit_enabled('NetworkManager-wait-online.service')
        self.log_services_state('initial', nm_enabled, nmwo_enabled)

        if not nm_enabled and nmwo_enabled:
            self.log.info('Disabling NetworkManager-wait-online.service')
            self.call(['systemctl', 'disable', 'NetworkManager-wait-online.service'])

            nm_enabled = self.unit_enabled('NetworkManager.service')
            nmwo_enabled = self.unit_enabled('NetworkManager-wait-online.service')
            self.log_services_state('after upgrade', nm_enabled, nmwo_enabled)

    def log_services_state(self, detail, nm, nmwo):
        self.log.info('Services state ({}):'.format(detail))
        self.log.info(' - NetworkManager            : {}'.format('enabled' if nm else 'disabled'))
        self.log.info(' - NetworkManager-wait-online: {}'.format('enabled' if nmwo else 'disabled'))

    def unit_enabled(self, name):
        try:
            ret_list = self.call(['systemctl', 'is-enabled', name])
            enabled = ret_list[0] == 'enabled'
        except CalledProcessError:
            enabled = False
        return enabled

    def call(self, args, split=True):
        r = None
        with open(os.devnull, mode='w') as err:
            if six.PY3:
                r = subprocess.check_output(args, stderr=err, encoding='utf-8')
            else:
                r = subprocess.check_output(args, stderr=err).decode('utf-8')
        if split:
            return r.splitlines()
        return r
