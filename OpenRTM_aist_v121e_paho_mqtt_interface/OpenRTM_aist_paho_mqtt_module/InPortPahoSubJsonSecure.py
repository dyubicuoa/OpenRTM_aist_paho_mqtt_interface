#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file   InPortPahoSubJsonSecure.py
# @brief  InPortPahoSubJsonSecure class
# @date   2020/12/10
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
import RTC
import time
import sys
from OpenRTM_aist_paho_mqtt_module.paho_client.PahoSubSecure import PahoSubSecure
from OpenRTM_aist_paho_mqtt_module.reserializer.DataTypeFormat import DataTypeFormat

##
# @class InPortPahoSubJsonSecure
# @brief InPortPahoSubJsonSecure class
#
class InPortPahoSubJsonSecure(OpenRTM_aist.InPortProvider, PahoSubSecure):
    
  """
  """

  ##
  # @brief Constructor
  #
  def __init__(self):
    OpenRTM_aist.InPortProvider.__init__(self)
    PahoSubSecure.__init__(self)

    self.setInterfaceType("mqtts_json")
    
    self._buffer = None
    self._profile = None
    self._listeners = None

    callback = self.on_message
    PahoSubSecure.set_on_message(self, callback)

    self._mgr = OpenRTM_aist.Manager.instance()
    self._mgr.addManagerActionListener(ManagerActionListener(self))

    return

  ##
  # @brief Destructor
  #
  def __del__(self):
    PahoSubSecure.__del__(self)
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
      self._rtcout.RTC_PARANOID("InPortPahoSubJsonSecure.on_message()")
      data = msg.payload

      cdrmsg = self.__formatter.reserializeFromJsonToCdr(data)

      if not self._buffer:
        #self.onReceiverError(data)
        self.onReceiverError(cdrmsg)
        return OpenRTM.PORT_ERROR

      self._rtcout.RTC_PARANOID("received data size: %d", len(data))

      #self.onReceived(data)
      self.onReceived(cdrmsg)

      if not self._connector:
        return OpenRTM.PORT_ERROR

      #ret = self._connector.write(data)
      ret = self._connector.write(cdrmsg)

      #return self.convertReturn(ret, data)
      return self.convertReturn(ret, cdrmsg)

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

    if self.subscribePahoSubJsonSecure(properties):
      return True

    return False

  ##
  # @brief Find index of the properties
  #
  # acceptable properties:
  #     {<key>, dataport.<key>, dataport.inport.<key>}
  #
  def findProp(self, properties, key):
    index = OpenRTM_aist.NVUtil.find_index(properties, key)
    if index >= 0: return index
    index = OpenRTM_aist.NVUtil.find_index(properties, 'dataport.' + key)
    if index >= 0: return index
    index = OpenRTM_aist.NVUtil.find_index(properties, 'dataport.inport.' + key)
    if index >= 0: return index
    return -1

  ##
  # @brief Set properties relating to Paho Client
  #
  def subscribePahoSubJsonSecure(self, properties):
    self._rtcout.RTC_TRACE("subscribePahoSubJsonSecure()")

    PN_HOST = "host"
    PN_PORT = "msport"
    PN_KPALV = "kpalv"
    PN_TOPIC = "topic"
    PN_QOS = "qos"
    PN_ID = "id"
    PN_CS = "cs"
    PN_CACERT = "cacert"
    PN_CLTCERT = "cltcert"
    PN_CLTKEY = "cltkey"

    index0 = self.findProp(properties, PN_HOST)
    index1 = self.findProp(properties, PN_PORT)
    index2 = self.findProp(properties, PN_KPALV)
    index3 = self.findProp(properties, PN_TOPIC)
    index4 = self.findProp(properties, PN_QOS)
    index5 = self.findProp(properties, PN_ID)
    index6 = self.findProp(properties, PN_CS)
    index7 = self.findProp(properties, PN_CACERT)
    index8 = self.findProp(properties, PN_CLTCERT)
    index9 = self.findProp(properties, PN_CLTKEY)

    tmp_host = "localhost"
    tmp_port = 8883
    tmp_kpalv = 60
    tmp_topic = "test"
    tmp_qos = 0
    tmp_id = ""
    tmp_cs = True
    tmp_cacert = "./ca.crt"
    tmp_cltcert = "./client.crt"
    tmp_cltkey = "./client.key"

    if index0 < 0:
      print("Server address not found. Default server address '" + tmp_host + "' is used.")
    else:
      try:
        tmp_host = any.from_any(properties[index0].value, keep_structs=True)
        if not tmp_host:
          self._rtcout.RTC_ERROR("Server address has no string.")
          return False
        print("Server address: " + tmp_host)
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if index1 < 0:
      print("Port number not found. Default port '" + str(tmp_port) + "' is used.")
    else:
      try:
        str_port = any.from_any(properties[index1].value, keep_structs=True)
        if not str_port:
          self._rtcout.RTC_ERROR("Port number has no string.")
          return False
        tmp_port = int(str_port)
        if tmp_port < 0 or tmp_port > 65535:
          tmp_port = 8883
        print("Port: " + str(tmp_port))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if index2 < 0:
      print("Keepalive not found. Default keepalve '" + str(tmp_kpalv) + "' is used.")
    else:
      try:
        str_kpalv = any.from_any(properties[index2].value, keep_structs=True)
        if not str_kpalv:
          self._rtcout.RTC_ERROR("Keepalive has no string.")
          return False
        tmp_kpalv = int(str_kpalv)
        if tmp_kpalv < 0 or tmp_kpalv > 86400:
          tmp_kpalv = 60
        print("keepalive: " + str(tmp_kpalv))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if index3 < 0:
      print("Topic not found. Default Topic '" + tmp_topic + "' is used.")
    else:
      try:
        tmp_topic = any.from_any(properties[index3].value, keep_structs=True)
        if not tmp_topic:
          self._rtcout.RTC_ERROR("Topic has no string.")
          return False
        print("Topic: " + tmp_topic)
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if index4 < 0:
      print("QoS not found. Default QoS '" + str(tmp_qos) + "' is used.")
    else:
      try:
        str_qos = any.from_any(properties[index4].value, keep_structs=True)
        if not str_qos:
          self._rtcout.RTC_ERROR("QoS has no string.")
          return False
        tmp_qos = int(str_qos)
        if tmp_qos < 0 or tmp_qos > 2:
          tmp_qos = 0
        print("QoS: " + str(tmp_qos))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if index5 < 0:
      print("Client ID not found. Random number ID is used.")
    else:
      try:
        tmp_id = any.from_any(properties[index5].value, keep_structs=True)
        if not tmp_id:
          tmp_id = ""
          print("Client ID has no string. Random number ID is used.")
        else:
          print("Client ID: " + tmp_id)
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if index6 < 0:
      print("CleanSession not found. Default clean_session '" + str(tmp_cs) + "' is used.")
    else:
      try:
        str_cs = any.from_any(properties[index6].value, keep_structs=True)
        if not str_cs:
          self._rtcout.RTC_ERROR("Clean session has no string.")
          return False
        if str_cs == "False" or str_cs == "false" or str_cs == "FALSE" or str_cs == "f" or str_cs == "F" or str_cs == "0":
          tmp_cs = False
        print("Clean session: " + str(tmp_cs))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if index7 < 0:
      print("Path to CA certificate file not found. Default path '" + tmp_cacert + "' is used.")
    else:
      try:
        tmp_cacert = any.from_any(properties[index7].value, keep_structs=True)
        if not tmp_cacert:
          self._rtcout.RTC_ERROR("Path to CA certificate file has no string.")
          return False
        print("Path to CA certificate file: " + tmp_cacert)
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if index8 < 0:
      print("Path to client certificate file not found. Default path '" + tmp_cltcert + "' is used.")
    else:
      try:
        tmp_cltcert = any.from_any(properties[index8].value, keep_structs=True)
        if not tmp_cltcert:
          self._rtcout.RTC_ERROR("Path to client certificate file has no string.")
          return False
        print("Path to client certificate file: " + tmp_cltcert)
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if index9 < 0:
      print("Path to client key file not found. Default path '" + tmp_cltkey + "' is used.")
    else:
      try:
        tmp_cltkey = any.from_any(properties[index9].value, keep_structs=True)
        if not tmp_cltkey:
          self._rtcout.RTC_ERROR("Path to client key file has no string.")
          return False
        print("Path to client key file: " + tmp_cltkey)
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    self.generateDataTypeInfo(properties)

    if self.__datatype and self.__endian:
      self.__formatter = DataTypeFormat(self.__datatype, self.__endian)
    else:
      self._rtcout.RTC_ERROR("DataType or Endian is unknown.")
      return False

    print("[connecting to MQTT broker start]")
    PahoSubSecure.paho_initialize(self, tmp_id, tmp_cs, tmp_topic, tmp_qos)
    PahoSubSecure.paho_secure_set(self, tmp_cacert, tmp_cltcert, tmp_cltkey)
    PahoSubSecure.paho_connect(self, tmp_host, tmp_port, tmp_kpalv)
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
  # @brief Generate information about datatype and endian
  #
  def generateDataTypeInfo(self, properties):
    PN_DATA_TYPE = "dataport.data_type"
    PN_ENDIAN = "dataport.serializer.cdr.endian"

    DELIMITER1 = "RTC/"
    DELIMITER2 = ":"
    PREFIX = "RTC."

    tmp_datatype = None
    tmp_endian = None

    indexDT = OpenRTM_aist.NVUtil.find_index(properties, PN_DATA_TYPE)
    if indexDT < 0:
      print("  Can not find DataType.")
      self._rtcout.RTC_ERROR("DataType is not set.")
      return False
    else:
      try:
        tmp_datatype = any.from_any(properties[indexDT].value, keep_structs=True)
        if not tmp_datatype:
          self._rtcout.RTC_ERROR("DataType has no string.")
          return False
        print("  DataType: " + tmp_datatype)
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    indexED = OpenRTM_aist.NVUtil.find_index(properties, PN_ENDIAN)
    if indexED < 0:
      print("  Can not find Endian.")
      self._rtcout.RTC_ERROR("Endian is not set.")
      return False
    else:
      try:
        tmp_endian = any.from_any(properties[indexED].value, keep_structs=True)
        if not tmp_endian:
          self._rtcout.RTC_ERROR("Endian has no string.")
          return False
        #print("  Endian: " + tmp_endian)
        tmp_endian = OpenRTM_aist.split(tmp_endian, ",")
        tmp_endian = OpenRTM_aist.normalize(tmp_endian)
        print("  Normalized endian: " + tmp_endian)
        if tmp_endian == "little":
          self.__endian = True
        elif tmp_endian == "big":
          self.__endian = False
        else:
          self.__endian = None
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    check1 = tmp_datatype.find(DELIMITER1)
    check2 = tmp_datatype.rfind(DELIMITER2)
    if check1 >= 0 and check2 >= 0:
      tmp_datatype = tmp_datatype[check1+len(DELIMITER1):check2]
    tmp_datatype = PREFIX + tmp_datatype
    self.__datatype = OpenRTM_aist.instantiateDataType(eval(tmp_datatype))

##
# @class ManagerActionListener
# @brief ManagerActionListener class
#
class ManagerActionListener:
  def __init__(self, InPortPahoSubJsonSecure):
    self._InPortPahoSubJsonSecure = InPortPahoSubJsonSecure

  def preShutdown(self):
    pass

  ##
  # @brief Clean up mqtt communication module instance when RTC exit
  #
  def postShutdown(self):
    print("[disconnecting from MQTT broker start]")
    self._InPortPahoSubJsonSecure.paho_disconnect()
    print("[disconnecting from MQTT broker end]")

  def preReinit(self):
    pass

  def postReinit(self):
    pass

##
# @brief Initialize InPortPahoSubJsonSecure module
#
def InPortPahoSubJsonSecureInit(self):
  factory = OpenRTM_aist.InPortProviderFactory.instance()
  factory.addFactory("mqtts_json",
                     InPortPahoSubJsonSecure,
                     OpenRTM_aist.Delete)

##
# @brief Register InPortPahoSubJsonSecure module
#
def registerModule():
  print("[Secure Paho Subscriber initialization start]")
  InPortPahoSubJsonSecureInit()
  print("[Secure Paho Subscriber initialization end]")
