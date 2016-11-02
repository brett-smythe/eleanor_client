"""Settings for eleanor_client"""
import os
import ConfigParser

eleanor_url = ''
eleanor_port = 5000

path_to_here = os.path.abspath(__file__)
local_settings_path = "{0}/{1}".format(path_to_here, 'local_settings.py')
if os.path.isfile(local_settings_path):
    import local_settings
    eleanor_url = local_settings.eleanor_url
    eleanor_port = local_settings.eleanor_port
else:
    config = ConfigParser.ConfigParser()
    config.read('/etc/opt/aquatic_services/service_locations.cfg')
    eleanor_url = config.get('Eleanor', 'ip_address')


