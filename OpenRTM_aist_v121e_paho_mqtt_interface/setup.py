from setuptools import setup

install_requires = [
  'OpenRTM-aist-Python',
  'paho-mqtt'
]

packages = [
  'OpenRTM_aist_paho_mqtt_module',
  'OpenRTM_aist_paho_mqtt_module.paho_client',
  'OpenRTM_aist_paho_mqtt_module.reserializer'
]

setup(
  name='OpenRTM_aist_paho_mqtt_module',
  version='0.6.2',
  description='MQTT interface modules on OpenRTM-aist',
  author='Daishi Yoshino',
  author_email = 'daishi-y@u-aizu.ac.jp',
  url='https://github.com/dyubicuoa/OpenRTM_aist_paho_mqtt_interface',
  license='MIT',
  packages=packages,
  install_requires=install_requires
)
