#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortPahoPubJson.py
# @brief OutPortPahoPubJson class
# @date   2020/12/10
# @author Daishi Yoshino
#
# Copyright (C) 2020
#     Daishi Yoshino
#     Revitalization Center
#     University of Aizu, Japan
# Originally under LGPL in OpenRTM-aist, http://www.openrtm.org/
#

from omniORB import *
import OpenRTM_aist
import OpenRTM
import RTC
import time
import sys
from OpenRTM_aist_paho_mqtt_module.paho_client.PahoPublisher import PahoPublisher
from OpenRTM_aist_paho_mqtt_module.reserializer.DataTypeFormat import DataTypeFormat

##
# @class OutPortPahoPubJson
# @brief OutPortPahoPubJson class
#
class OutPortPahoPubJson(OpenRTM_aist.InPortConsumer, PahoPublisher):
  """
  """

  ##
  # @brief Constructor
  #
  def __init__(self):
    PahoPublisher.__init__(self)
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("OutPortPahoPubJson")
    self._properties = None

    self._mgr = OpenRTM_aist.Manager.instance()
    self._mgr.addManagerActionListener(ManagerActionListener(self))

    return

  ##
  # @brief Destructor
  #
  def __del__(self, CorbaConsumer=PahoPublisher):
    self._rtcout.RTC_PARANOID("~OutPortPahoPubJson()")
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
      jsonmsg = self.__formatter.reserializeFromCdrToJson(data)
      #PahoPublisher.paho_pub(self, data)
      PahoPublisher.paho_pub(self, jsonmsg)
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

    if self.subscribePahoPubJson(properties):
      return True
    
    return False
    
  ##
  # @brief Unsubscribe the data send notification
  #
  def unsubscribeInterface(self, properties):
    self._rtcout.RTC_TRACE("unsubscribeInterface()")
    
    return

  ##
  # @brief Find index of the properties
  #
  # acceptable properties:
  #     {<key>, dataport.<key>, dataport.outport.<key>}
  #
  def findProp(self, properties, key):
    index = OpenRTM_aist.NVUtil.find_index(properties, key)
    if index >= 0: return index
    index = OpenRTM_aist.NVUtil.find_index(properties, 'dataport.' + key)
    if index >= 0: return index
    index = OpenRTM_aist.NVUtil.find_index(properties, 'dataport.outport.' + key)
    if index >= 0: return index
    return -1

  ##
  # @brief Set properties relating to Paho Client
  #
  def subscribePahoPubJson(self, properties):
    self._rtcout.RTC_TRACE("subscribePahoPubJson()")
    
    PN_HOST = "host"
    PN_PORT = "msport"
    PN_KPALV = "kpalv"
    PN_TOPIC = "topic"
    PN_QOS = "qos"
    PN_ID = "id"
    PN_CS = "cs"
    PN_MAXIF = "maxif"
    PN_RETAIN = "retain"
    PN_WILL = "will"
    PN_CLRRM = "clrrm"

    index0 = self.findProp(properties, PN_HOST)
    index1 = self.findProp(properties, PN_PORT)
    index2 = self.findProp(properties, PN_KPALV)
    index3 = self.findProp(properties, PN_TOPIC)
    index4 = self.findProp(properties, PN_QOS)
    index5 = self.findProp(properties, PN_ID)
    index6 = self.findProp(properties, PN_CS)
    index7 = self.findProp(properties, PN_MAXIF)
    index8 = self.findProp(properties, PN_RETAIN)
    index9 = self.findProp(properties, PN_WILL)
    indexA = self.findProp(properties, PN_CLRRM)

    tmp_host = "localhost"
    tmp_port = 1883
    tmp_kpalv = 60
    tmp_topic = "test"
    tmp_qos = 0
    tmp_id = ""
    tmp_cs = True
    tmp_maxif = 20
    tmp_retain = False
    tmp_will = False
    tmp_willmsg = None
    clear_retained_msg = False

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
          tmp_port = 1883
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
      print("MaxInflight not found. Default max_inflight '" + str(tmp_maxif) + "' is used.")
    else:
      try:
        str_maxif = any.from_any(properties[index7].value, keep_structs=True)
        if not str_maxif:
          self._rtcout.RTC_ERROR("MaxInflight has no string.")
          return False
        tmp_maxif = int(str_maxif)
        if tmp_maxif < 0 or tmp_maxif > 65535:
          tmp_maxif = 20
        print("max_inflight: " + str(tmp_maxif))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if index8 < 0:
      print("Retained not found. Default retained '" + str(tmp_retain) + "' is used.")
    else:
      try:
        str_retain = any.from_any(properties[index8].value, keep_structs=True)
        if not str_retain:
          self._rtcout.RTC_ERROR("Retained has no string.")
          return False
        if str_retain == "True" or str_retain == "true" or str_retain == "TRUE" or str_retain == "t" or str_retain == "T" or str_retain == "1":
          tmp_retain = True
        print("Retained: " + str(tmp_retain))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if index9 < 0:
      print("Last will not found. Default last will '" + str(tmp_will) + "' is used.")
    else:
      try:
        str_will = any.from_any(properties[index9].value, keep_structs=True)
        if not str_will:
          self._rtcout.RTC_ERROR("Last will has no string.")
          return False
        if str_will == "True" or str_will == "true" or str_will == "TRUE" or str_will == "t" or str_will == "T" or str_will == "1":
          tmp_will = True
        print("Last will: " + str(tmp_will))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if indexA >= 0:
      try:
        str_clrrm = any.from_any(properties[indexA].value, keep_structs=True)
        if not str_clrrm:
          self._rtcout.RTC_ERROR("Clear_retained_message has no string.")
          return False
        if str_clrrm == "True" or str_clrrm == "true" or str_clrrm == "TRUE" or str_clrrm == "t" or str_clrrm == "T" or str_clrrm == "1":
          clear_retained_msg = True
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    self.generateDataTypeInfo(properties)

    if self.__datatype and self.__endian:
      self.__formatter = DataTypeFormat(self.__datatype, self.__endian)
    else:
      self._rtcout.RTC_ERROR("DataType or Endian is unknown.")
      return False
      
    if tmp_will == True:
      if self.__datatype and self.__endian:
        cdrdata = cdrMarshal(any.to_any(self.__datatype).typecode(), self.__datatype, self.__endian)
        tmp_willmsg = self.__formatter.reserializeFromCdrToJson(cdrdata)
      else:
        tmp_willmsg = None
        print("DataType or Endian is unknown, therefore 'Will' function does not work.")

    print("[connecting to MQTT broker start]")
    PahoPublisher.paho_initialize(self, tmp_id, tmp_cs, tmp_maxif, tmp_topic, tmp_qos, tmp_retain, tmp_willmsg)
    PahoPublisher.paho_connect(self, tmp_host, tmp_port, tmp_kpalv)
    print("[connecting to MQTT broker end]")

    if clear_retained_msg == True:
      PahoPublisher.paho_pub_nullmsg(self)
      print("* Cleared retained message from MQTT broker.")

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
  def __init__(self, OutPortPahoPubJson):
    self._OutPortPahoPubJson = OutPortPahoPubJson

  def preShutdown(self):
    pass

  ##
  # @brief Clean up mqtt communication module instance when RTC exit
  #
  def postShutdown(self):
    print("[disconnecting from MQTT broker start]")
    self._OutPortPahoPubJson.paho_disconnect()
    print("[disconnecting from MQTT broker end]")

  def preReinit(self):
    pass

  def postReinit(self):
    pass

##
# @brief Initialize OutPortPahoPubJson module
#
def OutPortPahoPubJsonInit(self):
  factory = OpenRTM_aist.InPortConsumerFactory.instance()
  factory.addFactory("mqtt_json",
                     OutPortPahoPubJson,
                     OpenRTM_aist.Delete)
##
# @brief Register OutPortPahoPubJson module
#
def registerModule():
  print("[Paho Publisher initialization start]")
  OutPortPahoPubJsonInit()
  print("[Paho Publisher initialization end]")
