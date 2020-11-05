#!/usr/bin/python3
# -*- coding: euc-jp -*-

##
# @file   PahoSubSecure.py
# @brief  PahoSubSecure class
# @date   2020/11/04
# @author Daishi Yoshino
#
# Copyright (C) 2020
#     Daishi Yoshino
#     Revitalization Center
#     University of Aizu, Japan
#

import paho.mqtt.client as mqtt
from OpenRTM_aist_paho_mqtt_module.paho_client.PahoSubscriber import PahoSubscriber

##
# @class PahoSubSecure
# @brief PahoSubSecure class
#
class PahoSubSecure(PahoSubscriber):

  ##
  # @brief Constructor
  #
  def __init__(self):
    PahoSubscriber.__init__(self)
    print("PahoSubSecure constructor was called.")

  ##
  # @brief Destructor
  #
  def __del__(self):
    PahoSubscriber.__del__(self)
    print("PahoSubSecure destructor was called.")

  ##
  # @brief Specify the paths to secure communication related files
  # @param pcacert Path to certificate of certificate authority
  # @param pcltcert Path to certificate of MQTT client
  # @param pcltkey Path to private key of MQTT client
  #
  def paho_secure_set(self, pcacert="./ca.crt", pcltcert="./client.crt", pcltkey="./client.key"):
    self.__cacert = pcacert
    self.__clientcert = pcltcert
    self.__clientkey = pcltkey
    self.get_client().tls_set(ca_certs=self.__cacert, certfile=self.__clientcert, keyfile=self.__clientkey, cert_reqs = mqtt.ssl.CERT_REQUIRED, tls_version = mqtt.ssl.PROTOCOL_TLSv1_2, ciphers = None)
    self.get_client().tls_insecure_set(False)

if __name__ == '__main__':

    pahos = PahoSubSecure()
    pahos.paho_initialize()
    pahos.paho_secure_set()
    try:
      pahos.paho_connect()
    except KeyboardInterrupt:
      pahos.paho_disconnect()

    del pahos
