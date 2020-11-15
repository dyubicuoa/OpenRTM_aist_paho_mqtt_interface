#!/usr/bin/env python3
# -*- coding: euc-jp -*-

##
# @file  OutPortPahoPubSecure.py
# @brief OutPortPahoPubSecure class
# @date   2020/11/15
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
import signal
import os
import time
import threading
import sys
from OpenRTM_aist_paho_mqtt_module.paho_client.PahoPubSecure import PahoPubSecure

# There was a Ctrl+C interruption or not
stop = False
# Constructor was called already or not
called = False

##
# @class OutPortPahoPubSecure
# @brief OutPortPahoPubSecure class
#
class OutPortPahoPubSecure(OpenRTM_aist.InPortConsumer, PahoPubSecure):
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
    PahoPubSecure.__init__(self)
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("OutPortPahoPubSecure")
    self._properties = None
    thread = threading.Thread(target=self.catch_signal)
    thread.daemon = True
    thread.start()
    called = True

    return

  ##
  # @brief Destructor
  #
  def __del__(self, CorbaConsumer=PahoPubSecure):
    self._rtcout.RTC_PARANOID("~OutPortPahoPubSecure()")
    print("[disconnecting from MQTT broker start]")
    PahoPubSecure.paho_disconnect(self)
    print("[disconnecting from MQTT broker end]")
    PahoPubSecure.__del__(self)
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
      PahoPubSecure.paho_pub(self, data)
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

    if self.subscribePahoPubSecure(properties):
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
  def subscribePahoPubSecure(self, properties):
    self._rtcout.RTC_TRACE("subscribePahoPubSecure()")
    
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
    index7 = self.findProp(properties, PN_CACERT)
    index8 = self.findProp(properties, PN_CLTCERT)
    index9 = self.findProp(properties, PN_CLTKEY)
    indexA = self.findProp(properties, PN_MAXIF)
    indexB = self.findProp(properties, PN_RETAIN)
    indexC = self.findProp(properties, PN_WILL)
    indexD = self.findProp(properties, PN_CLRRM)

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

    if indexA < 0:
      print("MaxInflight not found. Default max_inflight '" + str(tmp_maxif) + "' is used.")
    else:
      try:
        str_maxif = any.from_any(properties[indexA].value, keep_structs=True)
        if not str_maxif:
          self._rtcout.RTC_ERROR("MaxInflight has no string.")
          return False
        tmp_maxif = int(str_maxif)
        if tmp_maxif < 0 or tmp_maxif > 65535:
          tmp_maxif = 20
        print("max_inflight: " + str(tmp_maxif))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if indexB < 0:
      print("Retained not found. Default retained '" + str(tmp_retain) + "' is used.")
    else:
      try:
        str_retain = any.from_any(properties[indexB].value, keep_structs=True)
        if not str_retain:
          self._rtcout.RTC_ERROR("Retained has no string.")
          return False
        if str_retain == "True" or str_retain == "true" or str_retain == "TRUE" or str_retain == "t" or str_retain == "T" or str_retain == "1":
          tmp_retain = True
        print("Retained: " + str(tmp_retain))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if indexC < 0:
      print("Last will not found. Default last will '" + str(tmp_will) + "' is used.")
    else:
      try:
        str_will = any.from_any(properties[indexC].value, keep_structs=True)
        if not str_will:
          self._rtcout.RTC_ERROR("Last will has no string.")
          return False
        if str_will == "True" or str_will == "true" or str_will == "TRUE" or str_will == "t" or str_will == "T" or str_will == "1":
          tmp_will = True
        print("Last will: " + str(tmp_will))
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if indexD >= 0:
      try:
        str_clrrm = any.from_any(properties[indexD].value, keep_structs=True)
        if not str_clrrm:
          self._rtcout.RTC_ERROR("Clear_retained_message has no string.")
          return False
        if str_clrrm == "True" or str_clrrm == "true" or str_clrrm == "TRUE" or str_clrrm == "t" or str_clrrm == "T" or str_clrrm == "1":
          clear_retained_msg = True
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if tmp_will == True:
      self.generateDataTypeInfo(properties)
      if self.__datatype and self.__endian:
        tmp_willmsg = cdrMarshal(any.to_any(self.__datatype).typecode(), self.__datatype, self.__endian)
      else:
        tmp_willmsg = None
        print("DataType or Endian is unknown, therefore 'Will' function does not work.")

    print("[connecting to MQTT broker start]")
    PahoPubSecure.paho_initialize(self, tmp_id, tmp_cs, tmp_maxif, tmp_topic, tmp_qos, tmp_retain, tmp_willmsg)
    PahoPubSecure.paho_secure_set(self, tmp_cacert, tmp_cltcert, tmp_cltkey)
    PahoPubSecure.paho_connect(self, tmp_host, tmp_port, tmp_kpalv)
    print("[connecting to MQTT broker end]")

    if clear_retained_msg == True:
      PahoPubSecure.paho_pub_nullmsg(self)
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

    if "Timed" in tmp_datatype and "Seq" in tmp_datatype:
      if any.to_any(RTC.TimedShortSeq).typecode().name() in tmp_datatype:
        dataBuff = []
        dataBuff.append(0)
        self.__datatype = RTC.TimedShortSeq(RTC.Time(0, 0), dataBuff)
      elif any.to_any(RTC.TimedLongSeq).typecode().name() in tmp_datatype:
        dataBuff = []
        dataBuff.append(0)
        self.__datatype = RTC.TimedLongSeq(RTC.Time(0, 0), dataBuff)
      elif any.to_any(RTC.TimedUShortSeq).typecode().name() in tmp_datatype:
        dataBuff = []
        dataBuff.append(0)
        self.__datatype = RTC.TimedUShortSeq(RTC.Time(0, 0), dataBuff)
      elif any.to_any(RTC.TimedULongSeq).typecode().name() in tmp_datatype:
        dataBuff = []
        dataBuff.append(0)
        self.__datatype = RTC.TimedULongSeq(RTC.Time(0, 0), dataBuff)
      elif any.to_any(RTC.TimedFloatSeq).typecode().name() in tmp_datatype:
        dataBuff = []
        dataBuff.append(0)
        self.__datatype = RTC.TimedFloatSeq(RTC.Time(0, 0), dataBuff)
      elif any.to_any(RTC.TimedDoubleSeq).typecode().name() in tmp_datatype:
        dataBuff = []
        dataBuff.append(0)
        self.__datatype = RTC.TimedDoubleSeq(RTC.Time(0, 0), dataBuff)
      elif any.to_any(RTC.TimedCharSeq).typecode().name() in tmp_datatype:
        dataBuff = []
        dataBuff.append('0')
        self.__datatype = RTC.TimedCharSeq(RTC.Time(0, 0), dataBuff)
      elif any.to_any(RTC.TimedWCharSeq).typecode().name() in tmp_datatype:
        dataBuff = []
        dataBuff.append('0')
        self.__datatype = RTC.TimedWCharSeq(RTC.Time(0, 0), dataBuff)
      elif any.to_any(RTC.TimedBooleanSeq).typecode().name() in tmp_datatype:
        dataBuff = []
        dataBuff.append(False)
        self.__datatype = RTC.TimedBooleanSeq(RTC.Time(0, 0), dataBuff)
      elif any.to_any(RTC.TimedOctetSeq).typecode().name() in tmp_datatype:
        dataBuff = []
        dataBuff.append('0')
        self.__datatype = RTC.TimedOctetSeq(RTC.Time(0, 0), dataBuff)
      elif any.to_any(RTC.TimedStringSeq).typecode().name() in tmp_datatype:
        dataBuff = []
        dataBuff.append("0")
        self.__datatype = RTC.TimedStringSeq(RTC.Time(0, 0), dataBuff)
      elif any.to_any(RTC.TimedWStringSeq).typecode().name() in tmp_datatype:
        dataBuff = []
        dataBuff.append("0")
        self.__datatype = RTC.TimedWStringSeq(RTC.Time(0, 0), dataBuff)
    elif "Timed" in tmp_datatype:
      if any.to_any(RTC.TimedState).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedState(RTC.Time(0, 0), 0)
      elif any.to_any(RTC.TimedShort).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedShort(RTC.Time(0, 0), 0)
      elif any.to_any(RTC.TimedLong).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedLong(RTC.Time(0, 0), 0)
      elif any.to_any(RTC.TimedUShort).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedUShort(RTC.Time(0, 0), 0)
      elif any.to_any(RTC.TimedULong).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedULong(RTC.Time(0, 0), 0)
      elif any.to_any(RTC.TimedFloat).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedFloat(RTC.Time(0, 0), 0)
      elif any.to_any(RTC.TimedDouble).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedDouble(RTC.Time(0, 0), 0)
      elif any.to_any(RTC.TimedChar).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedChar(RTC.Time(0, 0), '0')
      elif any.to_any(RTC.TimedWChar).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedWChar(RTC.Time(0, 0), '0')
      elif any.to_any(RTC.TimedBoolean).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedBoolean(RTC.Time(0, 0), False)
      elif any.to_any(RTC.TimedOctet).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedOctet(RTC.Time(0, 0), '0')
      elif any.to_any(RTC.TimedString).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedString(RTC.Time(0, 0), "0")
      elif any.to_any(RTC.TimedWString).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedWString(RTC.Time(0, 0), "0")
      elif any.to_any(RTC.TimedRGBColour).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedRGBColour(RTC.Time(0, 0), RTC.RGBColour(0, 0, 0))
      elif any.to_any(RTC.TimedPoint2D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedPoint2D(RTC.Time(0, 0), RTC.Point2D(0, 0))
      elif any.to_any(RTC.TimedVector2D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedVector2D(RTC.Time(0, 0), RTC.Vector2D(0, 0))
      elif any.to_any(RTC.TimedPose2D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedPose2D(RTC.Time(0, 0), RTC.Pose2D(RTC.Point2D(0, 0), 0))
      elif any.to_any(RTC.TimedVelocity2D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedVelocity2D(RTC.Time(0, 0), RTC.Velocity2D(0, 0, 0))
      elif any.to_any(RTC.TimedAcceleration2D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedAcceleration2D(RTC.Time(0, 0), RTC.Acceleration2D(0, 0))
      elif any.to_any(RTC.TimedPoseVel2D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedPoseVel2D(RTC.Time(0, 0), RTC.PoseVel2D(RTC.Pose2D(RTC.Point2D(0, 0), 0), RTC.Velocity2D(0, 0, 0)))
      elif any.to_any(RTC.TimedSize2D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedSize2D(RTC.Time(0, 0), RTC.Size2D(0, 0))
      elif any.to_any(RTC.TimedGeometry2D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedGeometry2D(RTC.Time(0, 0), RTC.Geometry2D(RTC.Pose2D(RTC.Point2D(0, 0), 0), RTC.Size2D(0, 0)))
      elif any.to_any(RTC.TimedCovariance2D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedCovariance2D(RTC.Time(0, 0), RTC.Covariance2D(0, 0, 0, 0, 0, 0))
      elif any.to_any(RTC.TimedPointCovariance2D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedPointCovariance2D(RTC.Time(0, 0), RTC.PointCovariance2D(0, 0, 0))
      elif any.to_any(RTC.TimedCarlike).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedCarlike(RTC.Time(0, 0), RTC.Carlike(0, 0))
      elif any.to_any(RTC.TimedSpeedHeading2D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedSpeedHeading2D(RTC.Time(0, 0), RTC.SpeedHeading2D(0, 0))
      elif any.to_any(RTC.TimedPoint3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedPoint3D(RTC.Time(0, 0), RTC.Point3D(0, 0, 0))
      elif any.to_any(RTC.TimedVector3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedVector3D(RTC.Time(0, 0), RTC.Vector3D(0, 0, 0))
      elif any.to_any(RTC.TimedOrientation3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedOrientation3D(RTC.Time(0, 0), RTC.Orientation3D(0, 0, 0))
      elif any.to_any(RTC.TimedPose3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedPose3D(RTC.Time(0, 0), RTC.Pose3D(RTC.Point3D(0, 0, 0), RTC.Orientation3D(0, 0, 0)))
      elif any.to_any(RTC.TimedVelocity3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedVelocity3D(RTC.Time(0, 0), RTC.Velocity3D(0, 0, 0, 0, 0, 0))
      elif any.to_any(RTC.TimedAngularVelocity3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedAngularVelocity3D(RTC.Time(0, 0), RTC.AngularVelocity3D(0, 0, 0))
      elif any.to_any(RTC.TimedAcceleration3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedAcceleration3D(RTC.Time(0, 0), RTC.Acceleration3D(0, 0, 0))
      elif any.to_any(RTC.TimedAngularAcceleration3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedAngularAcceleration3D(RTC.Time(0, 0), RTC.AngularAcceleration3D(0, 0, 0))
      elif any.to_any(RTC.TimedPoseVel3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedPoseVel3D(RTC.Time(0, 0), RTC.PoseVel3D(RTC.Pose3D(RTC.Point3D(0, 0, 0), RTC.Orientation3D(0, 0, 0)), RTC.Velocity3D(0, 0, 0, 0, 0, 0)))
      elif any.to_any(RTC.TimedSize3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedSize3D(RTC.Time(0, 0), RTC.Size3D(0, 0, 0))
      elif any.to_any(RTC.TimedGeometry3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedGeometry3D(RTC.Time(0, 0), RTC.Geometry3D(RTC.Pose3D(RTC.Point3D(0, 0, 0), RTC.Orientation3D(0, 0, 0)), RTC.Size3D(0, 0, 0)))
      elif any.to_any(RTC.TimedCovariance3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedCovariance3D(RTC.Time(0, 0), RTC.Covariance3D(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
      elif any.to_any(RTC.TimedSpeedHeading3D).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedSpeedHeading3D(RTC.Time(0, 0), RTC.SpeedHeading3D(0, RTC.Orientation3D(0, 0, 0)))
      elif any.to_any(RTC.TimedOAP).typecode().name() in tmp_datatype:
        self.__datatype = RTC.TimedOAP(RTC.Time(0, 0), RTC.OAP(RTC.Velocity3D(0, 0, 0, 0, 0, 0), RTC.Velocity3D(0, 0, 0, 0, 0, 0), RTC.Velocity3D(0, 0, 0, 0, 0, 0)))
    elif any.to_any(RTC.Time).typecode().name() in tmp_datatype:
      self.__datatype = RTC.Time(0, 0)
    else:
      if "Angular" in tmp_datatype:
        if any.to_any(RTC.AngularVelocity3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.AngularVelocity3D(0, 0, 0)
        elif any.to_any(RTC.AngularAcceleration3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.AngularAcceleration3D(0, 0, 0)
      else:
        if any.to_any(RTC.RGBColour).typecode().name() in tmp_datatype:
          self.__datatype = RTC.RGBColour(0, 0, 0)
        elif any.to_any(RTC.Point2D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Point2D(0, 0)
        elif any.to_any(RTC.Vector2D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Vector2D(0, 0)
        elif any.to_any(RTC.Pose2D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Pose2D(RTC.Point2D(0, 0), 0)
        elif any.to_any(RTC.Velocity2D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Velocity2D(0, 0, 0)
        elif any.to_any(RTC.Acceleration2D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Acceleration2D(0, 0)
        elif any.to_any(RTC.PoseVel2D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.PoseVel2D(RTC.Pose2D(RTC.Point2D(0, 0), 0), RTC.Velocity2D(0, 0, 0))
        elif any.to_any(RTC.Size2D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Size2D(0, 0)
        elif any.to_any(RTC.Geometry2D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Geometry2D(RTC.Pose2D(RTC.Point2D(0, 0), 0), RTC.Size2D(0, 0))
        elif any.to_any(RTC.Covariance2D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Covariance2D(0, 0, 0, 0, 0, 0)
        elif any.to_any(RTC.PointCovariance2D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.PointCovariance2D(0, 0, 0)
        elif any.to_any(RTC.Carlike).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Carlike(0, 0)
        elif any.to_any(RTC.SpeedHeading2D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.SpeedHeading2D(0, 0)
        elif any.to_any(RTC.Point3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Point3D(0, 0, 0)
        elif any.to_any(RTC.Vector3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Vector3D(0, 0, 0)
        elif any.to_any(RTC.Orientation3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Orientation3D(0, 0, 0)
        elif any.to_any(RTC.Pose3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Pose3D(RTC.Point3D(0, 0, 0), RTC.Orientation3D(0, 0, 0))
        elif any.to_any(RTC.Velocity3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Velocity3D(0, 0, 0, 0, 0, 0)
        elif any.to_any(RTC.Acceleration3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Acceleration3D(0, 0, 0)
        elif any.to_any(RTC.PoseVel3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.PoseVel3D(RTC.Pose3D(RTC.Point3D(0, 0, 0), RTC.Orientation3D(0, 0, 0)), RTC.Velocity3D(0, 0, 0, 0, 0, 0))
        elif any.to_any(RTC.Size3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Size3D(0, 0, 0)
        elif any.to_any(RTC.Geometry3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Geometry3D(RTC.Pose3D(RTC.Point3D(0, 0, 0), RTC.Orientation3D(0, 0, 0)), RTC.Size3D(0, 0, 0))
        elif any.to_any(RTC.Covariance3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.Covariance3D(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        elif any.to_any(RTC.SpeedHeading3D).typecode().name() in tmp_datatype:
          self.__datatype = RTC.SpeedHeading3D(0, RTC.Orientation3D(0, 0, 0))
        elif any.to_any(RTC.OAP).typecode().name() in tmp_datatype:
          self.__datatype = RTC.OAP(RTC.Velocity3D(0, 0, 0, 0, 0, 0), RTC.Velocity3D(0, 0, 0, 0, 0, 0), RTC.Velocity3D(0, 0, 0, 0, 0, 0))
        else:
          self.__datatype = None
          print("  The datatype does not support 'Will' function.")

##
# @brief Catch ctrl+c interruption
#
signal.signal(signal.SIGINT, OutPortPahoPubSecure.signal_handler)

##
# @brief Initialize OutPortPahoPubSecure module
#
def OutPortPahoPubSecureInit(self):
  factory = OpenRTM_aist.InPortConsumerFactory.instance()
  factory.addFactory("paho_mqtts",
                     OutPortPahoPubSecure,
                     OpenRTM_aist.Delete)

##
# @brief Register OutPortPahoPubSecure module
#
def registerModule():
  print("[Secure Paho Publisher initialization start]")
  OutPortPahoPubSecureInit()
  print("[Secure Paho Publisher initialization end]")
