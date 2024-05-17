# from configparser import ConfigParser
#
#
# class MyException(Exception):
#     pass
#
#
# class MyConfig(ConfigParser):
#     def __init__(self, config_file):
#         super(MyConfig, self).__init__()
#
#         self.read(config_file)
#         self.validate_config()
#
#     def validate_config(self):
#         required_values = {
#             'server': {
#                 'timeout': None,
#                 'gc_mode': ('none', 'aggressive', 'smart', 'auto'),
#                 'mode': ('master')
#             },
#             'client': {
#                 'fallback': ('none', 'polling', 'auto'),
#                 'mode': ('master', 'slave')
#             }
#         }
#         """
#         Notice the different mode validations for global mode setting: we can
#         enforce different value sets for different sections
#         """
#
#         for section, keys in required_values.items():
#             if section not in self:
#                 raise MyException(
#                     'Missing section %s in the config file' % section)
#
#             for key, values in keys.items():
#                 if key not in self[section] or self[section][key] == '':
#                     raise MyException((
#                                               'Missing value for %s under section %s in ' +
#                                               'the config file') % (key, section))
#
#                 if values:
#                     if self[section][key] not in values:
#                         raise MyException((
#                                                   'Invalid value for %s under section %s in ' +
#                                                   'the config file') % (key, section))
#
# cfg = {}
#
# try:
#     # The example config file has an invalid value so cfg will stay empty first
#     cfg = MyConfig('config.ini')
# except MyException as e:
#     # Initially you'll see this due to the invalid value
#     print(e)
# else:
#     # Once you fix the config file you'll see this
#     print(cfg['client']['fallback'])
from hsc_gov_subscriber.utils.config import Config, ConfigValidation

ConfigValidation.validate()
