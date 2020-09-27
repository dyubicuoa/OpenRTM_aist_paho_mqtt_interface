#!/usr/bin/python3
# -*- coding: euc-jp -*-

##
# @file   PahoPublisher.py
# @brief  PahoPublisher class
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
# @class PahoPublisher
# @brief PahoPublisher class
#
class PahoPublisher():

  ##
  # @brief Constructor
  #
  def __init__(self):
    self.__pubcl = mqtt.Client(protocol=mqtt.MQTTv311)
    print("PahoPublisher constructor was called.")

  ##
  # @brief Destructor
  #
  def __del__(self):
    print("PahoPublisher destructor was called.")

  ##
  # @brief Call back function when succeeded to connect to broker
  #
  def on_connect(self, mqttc, obj, flags, rc):
    #print("rc: "+str(rc))
    if(rc == 0):
      print("connected to broker.")
    else:
      print("failed to connect to broker with code "+str(rc)+".")

  ##
  # @brief Call back function when succeeded to disconnect from broker
  #
  def on_disconnect(self, client, userdata, rc):
    print("disconnected from broker with code "+str(rc)+".")

  ##
  # @brief Initialize paho client
  # @param pclientid Client ID
  # @param pcleansession Whether to keep the session information
  # @param ptopic Topic group
  # @param pqos Quality of MQTT messaging service
  #
  def paho_initialize(self, pclientid="", pcleansession=True, pmaxinflight=20, ptopic="test", pqos=0):
    self.__clientid = pclientid
    self.__cleansession = pcleansession
    self.__maxinflight = pmaxinflight
    self.__topic = ptopic
    self.__qos = pqos
    self.__pubcl.reinitialise(self.__clientid, self.__cleansession)
    if self.__qos > 0:
      self.__pubcl.max_inflight_messages_set(self.__maxinflight)
    self.__pubcl.on_connect = self.on_connect
    self.__pubcl.on_disconnect = self.on_disconnect

  ##
  # @brief Connect to MQTT broker
  # @param phost MQTT broker endpoint address
  # @param pport MQTT messaging service port number
  # @param pkeepalive Lifetime of client
  #
  def paho_connect(self, phost="localhost", pport=1883, pkeepalive=60):
    self.__host = phost
    self.__port = pport
    self.__keepalive = pkeepalive
    self.__pubcl.connect(self.__host, self.__port, self.__keepalive)
    self.__pubcl.loop_start()

  ##
  # @brief Disconnect from MQTT broker
  #
  def paho_disconnect(self):
    self.__pubcl.loop_stop(True)
    self.__pubcl.disconnect()

  ##
  # @brief Publish a MQTT message
  # @param pdata Message payload
  #
  def paho_pub(self, pdata):
    self.__pubcl.publish(self.__topic, pdata, self.__qos)
    
if __name__ == '__main__':

    pahop = PahoPublisher()
    pahop.paho_initialize()
    pahop.paho_connect()
    pahop.paho_pub("Hello Paho!")
    pahop.paho_disconnect()

    del pahop
