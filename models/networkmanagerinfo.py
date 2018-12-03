from leapp.models import Model, fields
from leapp.topics import NetworkManagerInfoTopic

class NetworkManagerInfo(Model):
    topic = NetworkManagerInfoTopic
    dhcp = fields.String('')
