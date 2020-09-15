#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file   InPortPahoSubscriber.py
# @brief  InPortPahoSubscriber class
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
import OpenRTM_aist
import OpenRTM__POA,OpenRTM
import signal
import os
import time
import threading
import sys
import OpenRTM_aist_paho_mqtt_module.paho_client.PahoSubscriber as PahoSubscriber

# There was a Ctrl+C interruption or not
stop = False
# Constructor was called already or not
called = False

##
# @class InPortPahoSubscriber
# @brief InPortPahoSubscriber class
#
class InPortPahoSubscriber(OpenRTM_aist.InPortProvider, PahoSubscriber):
    
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
    OpenRTM_aist.InPortProvider.__init__(self)
    PahoSubscriber.__init__(self)

    self.setInterfaceType("paho_mqtt")
    
    self._buffer = None
    self._profile = None
    self._listeners = None

    orb = OpenRTM_aist.Manager.instance().getORB()

    callback = self.on_message
    PahoSubscriber.set_on_message(self, callback)

    thread = threading.Thread(target=self.catch_signal)
    thread.daemon = True
    thread.start()
    called = True

    return

  ##
  # @brief Destructor
  #
  def __del__(self):
    print("[disconnecting from MQTT broker start]")
    PahoSubscriber.paho_disconnect(self)
    print("[disconnecting from MQTT broker end]")
    PahoSubscriber.__del__(self)
    return

  ##
  # @brief Exit
  #
  def exit(self):
    oid = OpenRTM_aist.Manager.instance().getPOA().servant_to_id(self)
    OpenRTM_aist.Manager.instance().getPOA().deactivate_object(oid)

  ##
  # @brief Initializing configuration
  #
  def init(self, prop):
    pass

  ##
  # @brief Set buffer
  #
  def setBuffer(self, buffer):
    self._buffer = buffer
    return

  ##
  # @brief Set listener
  #
  def setListener(self, info, listeners):
    self._profile = info
    self._listeners = listeners
    return

  ##
  # @brief Call back function when received MQTT message
  #
  def on_message(self, mqttc, obj, msg):
    try:
      self._rtcout.RTC_PARANOID("InPortPahoSubscriber.on_message()")
      data = eval(msg.payload)
            
      if not self._buffer:
        self.onReceiverError(data)
        return OpenRTM.PORT_ERROR

      self._rtcout.RTC_PARANOID("received data size: %d", len(data))

      self.onReceived(data)

      if not self._connector:
        return OpenRTM.PORT_ERROR

      ret = self._connector.write(data)

      return self.convertReturn(ret, data)

    except:
      self._rtcout.RTC_TRACE(OpenRTM_aist.Logger.print_exception())
      return OpenRTM.UNKNOWN_ERROR

  ##
  # @brief Return codes conversion
  #
  def convertReturn(self, status, data):
    if status == OpenRTM_aist.BufferStatus.BUFFER_OK:
      self.onBufferWrite(data)
      return OpenRTM.PORT_OK
            
    elif status == OpenRTM_aist.BufferStatus.BUFFER_ERROR:
      self.onReceiverError(data)
      return OpenRTM.PORT_ERROR

    elif status == OpenRTM_aist.BufferStatus.BUFFER_FULL:
      self.onBufferFull(data)
      self.onReceiverFull(data)
      return OpenRTM.BUFFER_FULL

    elif status == OpenRTM_aist.BufferStatus.BUFFER_EMPTY:
      return OpenRTM.BUFFER_EMPTY

    elif status == OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET:
      self.onReceiverError(data)
      return OpenRTM.PORT_ERROR

    elif status == OpenRTM_aist.BufferStatus.TIMEOUT:
      self.onBufferWriteTimeout(data)
      self.onReceiverTimeout(data)
      return OpenRTM.BUFFER_TIMEOUT

    else:
      self.onReceiverError(data)
      return OpenRTM.UNKNOWN_ERROR

  ##
  # @brief Publish Interface information
  #
  def publishInterface(self, properties):
    self._rtcout.RTC_TRACE("publishInterace()")

    if self.subscribePahoSubscriber(properties):
      return True

    return False

  ##
  # @brief Set properties relating to Paho Client
  #
  def subscribePahoSubscriber(self, properties):
    self._rtcout.RTC_TRACE("subscribePahoSubscriber()")

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

    #if not tmp_id:
    #  self._rtcout.RTC_ERROR("Client ID has no string")
    #  return False

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
    PahoSubscriber.paho_initialize(self, tmp_id, tmp_cs, tmp_topic, tmp_qos)
    PahoSubscriber.paho_connect(self, tmp_host, tmp_port, tmp_kpalv)
    print("[connecting to MQTT broker end]")

    return True


  ##
  # @brief Connector data listener functions
  #
  def onBufferWrite(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE].notify(self._profile, data)
    return

  def onBufferFull(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_FULL].notify(self._profile, data)
    return

  def onBufferWriteTimeout(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE_TIMEOUT].notify(self._profile, data)
    return

  def onBufferWriteOverwrite(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_OVERWRITE].notify(self._profile, data)
    return

  def onReceived(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED].notify(self._profile, data)
    return

  def onReceiverFull(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_FULL].notify(self._profile, data)
    return

  def onReceiverTimeout(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_TIMEOUT].notify(self._profile, data)
    return

  def onReceiverError(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_ERROR].notify(self._profile, data)
    return


##
# @brief Catch ctrl+c interruption
#
signal.signal(signal.SIGINT, InPortPahoSubscriber.signal_handler)

##
# @brief Initialize InPortPahoSubscriber module
#
def InPortPahoSubscriberInit(self):
  factory = OpenRTM_aist.InPortProviderFactory.instance()
  factory.addFactory("paho_mqtt",
                     InPortPahoSubscriber,
                     OpenRTM_aist.Delete)

##
# @brief Register InPortPahoSubscriber module
#
def registerModule():
  print("[Paho Subscriber initialization start]")
  InPortPahoSubscriberInit()
  print("[Paho Subscriber initialization end]")
