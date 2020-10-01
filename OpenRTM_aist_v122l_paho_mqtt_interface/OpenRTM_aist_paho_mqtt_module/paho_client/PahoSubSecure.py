#!/usr/bin/python3
# -*- coding: euc-jp -*-

##
# @file   PahoSubSecure.py
# @brief  PahoSubSecure class
# @date   2020/09/07
# @author Daishi Yoshino
#
# Copyright (C) 2020
#     Daishi Yoshino
#     Revitalization Center
#     University of Aizu, Japan
#

import paho.mqtt.client as mqtt

##
# @class PahoSubSecure
# @brief PahoSubSecure class
#
class PahoSubSecure():

  ##
  # @brief Constructor
  #
  def __init__(self):
    self.__subcl = mqtt.Client(protocol=mqtt.MQTTv311)
    print("PahoSubSecure constructor was called.")

  ##
  # @brief Destructor
  #
  def __del__(self):
    print("PahoSubSecure destructor was called.")

  ##
  # @brief Call back function when succeeded to connect to broker
  #
  def on_connect(self, mqttc, obj, flags, rc):
    if(rc == 0):
      print("connected to broker.")
      self.__subcl.subscribe(self.__topic, self.__qos)
    else:
      print("failed to connect to broker with code "+str(rc)+".")

  ##
  # @brief Call back function when succeeded to disconnect from broker
  #
  def on_disconnect(self, client, userdata, rc):
    print("disconnected from broker with code "+str(rc)+".")

  ##
  # @brief Call back function when started to subscribe messages
  #
  def on_subscribe(self, mqttc, obj, mid, granted_qos):
    print("Subscription started: "+str(mid)+" "+str(granted_qos))

  ##
  # @brief Call back function when received a message
  #
  def on_message(self, mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

  ##
  # @brief Initialize paho client
  # @param pclientid Client ID
  # @param pcleansession Whether to keep the session information
  # @param ptopic Topic group
  # @param pqos Quality of MQTT messaging service
  #
  def paho_initialize(self, pclientid="", pcleansession=True, ptopic="test", pqos=0):
    self.__clientid = pclientid
    self.__cleansession = pcleansession
    self.__topic = ptopic
    self.__qos = pqos
    self.__subcl.reinitialise(self.__clientid, self.__cleansession)
    self.__subcl.on_connect = self.on_connect
    self.__subcl.on_disconnect = self.on_disconnect
    self.__subcl.on_subscribe = self.on_subscribe
    self.__subcl.on_message = self.on_message

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
    self.__subcl.tls_set(ca_certs=self.__cacert, certfile=self.__clientcert, keyfile=self.__clientkey, cert_reqs = mqtt.ssl.CERT_REQUIRED, tls_version = mqtt.ssl.PROTOCOL_TLSv1_2, ciphers = None)
    self.__subcl.tls_insecure_set(False)

  ##
  # @brief Connect to MQTT broker
  # @param phost MQTT broker endpoint address
  # @param pport MQTT messaging service port number
  # @param pkeepalive Lifetime of client
  #
  def paho_connect(self, phost="localhost", pport=8883, pkeepalive=60):
    self.__host = phost
    self.__port = pport
    self.__keepalive = pkeepalive
    self.__subcl.connect(self.__host, self.__port, self.__keepalive)
    self.__subcl.loop_start()
    # You should select loop_forever method, if you use this code as a mqtt subscriber client.
    #self.__subcl.loop_forever()

  ##
  # @brief Disconnect from MQTT broker
  #
  def paho_disconnect(self):
    self.__subcl.loop_stop(True)
    self.__subcl.disconnect()

  ##
  # @brief Set the call back function
  #
  def set_on_message(self, func):
    self.__subcl.on_message = func

if __name__ == '__main__':

    pahos = PahoSubSecure()
    pahos.paho_initialize()
    pahos.paho_secure_set()
    try:
      pahos.paho_connect()
    except KeyboardInterrupt:
      pahos.paho_disconnect()

    del pahos
