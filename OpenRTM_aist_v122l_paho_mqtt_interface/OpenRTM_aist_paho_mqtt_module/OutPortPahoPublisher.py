#!/usr/bin/env python3
# -*- coding: euc-jp -*-

##
# @file  OutPortPahoPublisher.py
# @brief OutPortPahoPublisher class
# @date   2020/09/15
# @author Daishi Yoshino
#
# Copyright (C) 2020
#     Daishi Yoshino
#     Revitalization Center
#     University of Aizu, Japan
# Originally under LGPL in OpenRTM-aist, http://www.openrtm.org/
#

from omniORB import any
from omniORB import CORBA
import OpenRTM_aist
import OpenRTM
import signal
import os
import time
import threading
import sys
import OpenRTM_aist_paho_mqtt_module.paho_client.PahoPublisher as PahoPublisher

# There was a Ctrl+C interruption or not
stop = False
# Constructor was called already or not
called = False

##
# @class OutPortPahoPublisher
# @brief OutPortPahoPublisher class
#
class OutPortPahoPublisher(OpenRTM_aist.InPortConsumer, PahoPublisher):
  """
  """

  ##
  # @brief Signal handler
  #
  @staticmethod
  def signal_handler(num, frame):
    global stop
    print(" Ctrl+C interrupted.")
    stop = True
    if called == False:
      os._exit(0)

  ##
  # @brief Shutdown hook
  #
  def catch_signal(self):
    while not stop:
      time.sleep(1)
    self.__del__()
    os._exit(0)

  ##
  # @brief Constructor
  #
  def __init__(self):
    global called
    PahoPublisher.__init__(self)
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("OutPortPahoPublisher")
    self._properties = None
    thread = threading.Thread(target=self.catch_signal)
    thread.daemon = True
    thread.start()
    called = True

    return

  ##
  # @brief Destructor
  #
  def __del__(self, CorbaConsumer=PahoPublisher):
    self._rtcout.RTC_PARANOID("~OutPortPahoPublisher()")
    print("[disconnecting from MQTT broker start]")
    PahoPublisher.paho_disconnect(self)
    print("[disconnecting from MQTT broker end]")
    PahoPublisher.__del__(self)
    return

  ##
  # @brief Initializing configuration
  #
  def init(self, prop):
    self._rtcout.RTC_TRACE("init()")
    self._properties = prop
    return

  ##
  # @brief Send data to the destination port
  #
  def put(self, data):
    self._rtcout.RTC_PARANOID("put()")

    try:
      rpdata = repr(data)
      PahoPublisher.paho_pub(self, rpdata)
      return self.PORT_OK
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return self.CONNECTION_LOST

  ##
  # @brief Publish InterfaceProfile information
  #
  def publishInterfaceProfile(self, properties):
    return

  ##
  # @brief Subscribe to the data sending notification
  #
  def subscribeInterface(self, properties):
    self._rtcout.RTC_TRACE("subscribeInterface()")

    if self.subscribePahoPublisher(properties):
      return True
    
    return False
    
  ##
  # @brief Unsubscribe the data send notification
  #
  def unsubscribeInterface(self, properties):
    self._rtcout.RTC_TRACE("unsubscribeInterface()")
    
    return

  ##
  # @brief Set properties relating to Paho Client
  #
  def subscribePahoPublisher(self, properties):
    self._rtcout.RTC_TRACE("subscribePahoPublisher()")
    
    PN_HOST = "host"
    PN_PORT = "port"
    PN_KPALV = "kpalv"
    PN_TOPIC = "topic"
    PN_QOS = "qos"
    PN_ID = "id"
    PN_CS = "cs"

    index0 = OpenRTM_aist.NVUtil.find_index(properties, PN_HOST)
    index1 = OpenRTM_aist.NVUtil.find_index(properties, PN_PORT)
    index2 = OpenRTM_aist.NVUtil.find_index(properties, PN_KPALV)
    index3 = OpenRTM_aist.NVUtil.find_index(properties, PN_TOPIC)
    index4 = OpenRTM_aist.NVUtil.find_index(properties, PN_QOS)
    index5 = OpenRTM_aist.NVUtil.find_index(properties, PN_ID)
    index6 = OpenRTM_aist.NVUtil.find_index(properties, PN_CS)

    tmp_host = "localhost"
    tmp_port = 1883
    str_port = "1883"
    tmp_kpalv = 60
    str_kpalv ="60"
    tmp_topic = "test"
    tmp_qos = 0
    str_qos = "0"
    tmp_id = ""
    tmp_cs = True
    str_cs = "True"

    if index0 < 0:
      print("Server address not found. Default server address '" + tmp_host + "' is used.")
    else:
      try:
        tmp_host = any.from_any(properties[index0].value, keep_structs=True)
        print("Server address: " + tmp_host)
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if not tmp_host:
      self._rtcout.RTC_ERROR("Server address has no string")
      return False

    if index1 < 0:
      print("Port number not found. Default port '" + str(tmp_port) + "' is used.")
    else:
      try:
        str_port = any.from_any(properties[index1].value, keep_structs=True)
        tmp_port = int(str_port)
        if tmp_port < 0 or tmp_port > 65535:
          tmp_port = 1883
        print("Port: " + str(tmp_port))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if not str_port:
      self._rtcout.RTC_ERROR("Port number has no string")
      return False

    if index2 < 0:
      print("Keepalive not found. Default keepalve '" + str(tmp_kpalv) + "' is used.")
    else:
      try:
        str_kpalv = any.from_any(properties[index2].value, keep_structs=True)
        tmp_kpalv = int(str_kpalv)
        if tmp_kpalv < 0 or tmp_kpalv > 86400:
          tmp_kpalv = 60
        print("keepalive: " + str(tmp_kpalv))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if not str_kpalv:
      self._rtcout.RTC_ERROR("Keepalive has no string")
      return False

    if index3 < 0:
      print("Topic not found. Default Topic '" + tmp_topic + "' is used.")
    else:
      try:
        tmp_topic = any.from_any(properties[index3].value, keep_structs=True)
        print("Topic: " + tmp_topic)
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if not tmp_topic:
      self._rtcout.RTC_ERROR("Topic has no string")
      return False

    if index4 < 0:
      print("QoS not found. Default QoS '" + str(tmp_qos) + "' is used.")
    else:
      try:
        str_qos = any.from_any(properties[index4].value, keep_structs=True)
        tmp_qos = int(str_qos)
        if tmp_qos < 0 or tmp_qos > 2:
          tmp_qos = 0
        print("QoS: " + str(tmp_qos))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if not str_qos:
      self._rtcout.RTC_ERROR("QoS has no string")
      return False

    if index5 < 0:
      print("Client ID not found. Random number ID is used.")
    else:
      try:
        tmp_id = any.from_any(properties[index5].value, keep_structs=True)
        print("Client ID: " + tmp_id)
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if index6 < 0:
      print("CleanSession not found. Default clean_session '" + str(tmp_cs) + "' is used.")
    else:
      try:
        str_cs = any.from_any(properties[index6].value, keep_structs=True)
        if str_cs == "False" or str_cs == "false" or str_cs == "FALSE" or str_cs == "f" or str_cs == "F" or str_cs == "0":
          tmp_cs = False
        print("Clean session: " + str(tmp_cs))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if not str_cs:
      self._rtcout.RTC_ERROR("Clean session has no string")
      return False

    print("[connecting to MQTT broker start]")
    PahoPublisher.paho_initialize(self, tmp_id, tmp_cs, tmp_topic, tmp_qos)
    PahoPublisher.paho_connect(self, tmp_host, tmp_port, tmp_kpalv)
    print("[connecting to MQTT broker end]")

    return True

  ##
  # @brief Return codes conversion
  #
  def convertReturnCode(self, ret):
    if ret == OpenRTM.PORT_OK:
      return self.PORT_OK

    elif ret == OpenRTM.PORT_ERROR:
      return self.PORT_ERROR

    elif ret == OpenRTM.BUFFER_FULL:
      return self.SEND_FULL

    elif ret == OpenRTM.BUFFER_TIMEOUT:
      return self.SEND_TIMEOUT

    elif ret == OpenRTM.UNKNOWN_ERROR:
      return self.UNKNOWN_ERROR

    else:
      return self.UNKNOWN_ERROR

##
# @brief Catch ctrl+c interruption
#
signal.signal(signal.SIGINT, OutPortPahoPublisher.signal_handler)

##
# @brief Initialize OutPortPahoPublisher module
#
def OutPortPahoPublisherInit(self):
  factory = OpenRTM_aist.InPortConsumerFactory.instance()
  factory.addFactory("paho_mqtt",
                     OutPortPahoPublisher,
                     OpenRTM_aist.Delete)
##
# @brief Register OutPortPahoPublisher module
#
def registerModule():
  print("[Paho Publisher initialization start]")
  OutPortPahoPublisherInit()
  print("[Paho Publisher initialization end]")
