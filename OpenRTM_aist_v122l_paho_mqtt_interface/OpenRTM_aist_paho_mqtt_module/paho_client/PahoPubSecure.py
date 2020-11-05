#!/usr/bin/python3
# -*- coding: euc-jp -*-

##
# @file   PahoPubSecure.py
# @brief  PahoPubSecure class
# @date   2020/11/04
# @author Daishi Yoshino
#
# Copyright (C) 2020
#     Daishi Yoshino
#     Revitalization Center
#     University of Aizu, Japan
#

import paho.mqtt.client as mqtt
from OpenRTM_aist_paho_mqtt_module.paho_client.PahoPublisher import PahoPublisher

##
# @class PahoPubSecure
# @brief PahoPubSecure class
#
class PahoPubSecure(PahoPublisher):

  ##
  # @brief Constructor
  #
  def __init__(self):
    PahoPublisher.__init__(self)
    print("PahoPubSecure constructor was called.")

  ##
  # @brief Destructor
  #
  def __del__(self):
    PahoPublisher.__del__(self)
    print("PahoPubSecure destructor was called.")

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

    pahop = PahoPubSecure()
    pahop.paho_initialize()
    pahop.paho_secure_set()
    pahop.paho_connect()
    pahop.paho_pub("Hello Paho!")
    pahop.paho_disconnect()

    del pahop
