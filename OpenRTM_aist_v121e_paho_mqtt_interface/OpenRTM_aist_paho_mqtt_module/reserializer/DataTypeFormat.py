#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  DataTypeFormat.py
# @brief DataTypeFormat class
# @date   2020/11/19
# @author Daishi Yoshino
#
# Copyright (C) 2020
#     Daishi Yoshino
#     Revitalization Center
#     University of Aizu, Japan
#

from omniORB import *
import RTC
import json

##
# @class DataTypeFormat
# @brief DataTypeFormat class
#
class DataTypeFormat:

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    self._datatype = datatype
    self._endian = endian
    self._TYPE_NAME = any.to_any(self._datatype).typecode().name()

  ##
  # @brief Reserialize from CDR to JSON
  #
  # CDR data -> (unmarshal) -> DataType object -> (serialize) -> JSON text
  #
  def reserializeFromCdrToJson(self, cdrdata):
    pass

  ##
  # @brief Reserialize from JSON to CDR
  #
  # JSON text -> (deserialize) -> Dictionary object -> (marshal) -> CDR data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    pass

##
# @class BasicDataTypeFormat
# @brief BasicDataTypeFormat class
#
class BasicDataTypeFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'
    self._FULL_DTNAME = "RTC." + any.to_any(self._datatype).typecode().name()

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:dtobj.data}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = eval(self._FULL_DTNAME)(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              dictobj[self._TYPE_NAME][self._DATA])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimeFormat
# @brief TimeFormat class
#
class TimeFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._SEC = 'sec'
    self._NSEC = 'nsec'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._SEC:dtobj.sec, \
                 self._NSEC:dtobj.nsec}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Time(\
              dictobj[self._TYPE_NAME][self._SEC], \
              dictobj[self._TYPE_NAME][self._NSEC])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class RGBColourFormat
# @brief RGBColourFormat class
#
class RGBColourFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._R = 'r'
    self._G = 'g'
    self._B = 'b'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._R:dtobj.r, \
                 self._G:dtobj.g, \
                 self._B:dtobj.b}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.RGBColour(\
              dictobj[self._TYPE_NAME][self._R], \
              dictobj[self._TYPE_NAME][self._G], \
              dictobj[self._TYPE_NAME][self._B])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class PointOrVector2DFormat
# @brief PointOrVector2DFormat class
#
class PointOrVector2DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._X = 'x'
    self._Y = 'y'
    self._FULL_DTNAME = "RTC." + any.to_any(self._datatype).typecode().name()

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._X:dtobj.x, \
                 self._Y:dtobj.y}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = eval(self._FULL_DTNAME)(\
              dictobj[self._TYPE_NAME][self._X], \
              dictobj[self._TYPE_NAME][self._Y])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Pose2DFormat
# @brief Pose2DFormat class
#
class Pose2DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._PT2D_NAME = 'position'
    self._X = 'x'
    self._Y = 'y'
    self._HEADING = 'heading'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._PT2D_NAME:\
                  {self._X:dtobj.position.x, \
                   self._Y:dtobj.position.y}, \
                 self._HEADING:dtobj.heading}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Pose2D(\
              RTC.Point2D(\
                dictobj[self._TYPE_NAME][self._PT2D_NAME][self._X], \
                dictobj[self._TYPE_NAME][self._PT2D_NAME][self._Y]), \
              dictobj[self._TYPE_NAME][self._HEADING])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Velocity2DFormat
# @brief Velocity2DFormat class
#
class Velocity2DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._VX = 'vx'
    self._VY = 'vy'
    self._VA = 'va'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._VX:dtobj.vx, \
                 self._VY:dtobj.vy, \
                 self._VA:dtobj.va}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Velocity2D(\
              dictobj[self._TYPE_NAME][self._VX], \
              dictobj[self._TYPE_NAME][self._VY], \
              dictobj[self._TYPE_NAME][self._VA])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Acceleration2DFormat
# @brief Acceleration2DFormat class
#
class Acceleration2DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._AX = 'ax'
    self._AY = 'ay'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._AX:dtobj.ax, \
                 self._AY:dtobj.ay}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Acceleration2D(\
              dictobj[self._TYPE_NAME][self._AX], \
              dictobj[self._TYPE_NAME][self._AY])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class PoseVel2DFormat
# @brief PoseVel2DFormat class
#
class PoseVel2DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._PS2D_NAME = 'pose'
    self._PT2D_NAME = 'position'
    self._X = 'x'
    self._Y = 'y'
    self._HEADING = 'heading'
    self._VL2D_NAME = 'velocities'
    self._VX = 'vx'
    self._VY = 'vy'
    self._VA = 'va'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._PS2D_NAME:\
                  {self._PT2D_NAME:\
                    {self._X:dtobj.pose.position.x, \
                     self._Y:dtobj.pose.position.y}, \
                   self._HEADING:dtobj.pose.heading}, \
                 self._VL2D_NAME:\
                  {self._VX:dtobj.velocities.vx, \
                   self._VY:dtobj.velocities.vy, \
                   self._VA:dtobj.velocities.va}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.PoseVel2D(\
              RTC.Pose2D(\
                RTC.Point2D(\
                  dictobj[self._TYPE_NAME][self._PS2D_NAME][self._PT2D_NAME][self._X], \
                  dictobj[self._TYPE_NAME][self._PS2D_NAME][self._PT2D_NAME][self._Y]), \
                dictobj[self._TYPE_NAME][self._PS2D_NAME][self._HEADING]), \
              RTC.Velocity2D(\
                dictobj[self._TYPE_NAME][self._VL2D_NAME][self._VX], \
                dictobj[self._TYPE_NAME][self._VL2D_NAME][self._VY], \
                dictobj[self._TYPE_NAME][self._VL2D_NAME][self._VA]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Size2DFormat
# @brief Size2DFormat class
#
class Size2DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._L = 'l'
    self._W = 'w'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._L:dtobj.l, \
                 self._W:dtobj.w}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Size2D(\
              dictobj[self._TYPE_NAME][self._L], \
              dictobj[self._TYPE_NAME][self._W])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Geometry2DFormat
# @brief Geometry2DFormat class
#
class Geometry2DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._PS2D_NAME = 'pose'
    self._PT2D_NAME = 'position'
    self._X = 'x'
    self._Y = 'y'
    self._HEADING = 'heading'
    self._SZ2D_NAME = 'size'
    self._L = 'l'
    self._W = 'w'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._PS2D_NAME:\
                  {self._PT2D_NAME:\
                    {self._X:dtobj.pose.position.x, \
                     self._Y:dtobj.pose.position.y}, \
                   self._HEADING:dtobj.pose.heading}, \
                 self._SZ2D_NAME:\
                  {self._L:dtobj.size.l, \
                   self._W:dtobj.size.w}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Geometry2D(\
              RTC.Pose2D(\
                RTC.Point2D(\
                  dictobj[self._TYPE_NAME][self._PS2D_NAME][self._PT2D_NAME][self._X], \
                  dictobj[self._TYPE_NAME][self._PS2D_NAME][self._PT2D_NAME][self._Y]), \
                dictobj[self._TYPE_NAME][self._PS2D_NAME][self._HEADING]), \
              RTC.Size2D(\
                dictobj[self._TYPE_NAME][self._SZ2D_NAME][self._L], \
                dictobj[self._TYPE_NAME][self._SZ2D_NAME][self._W]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Covariance2DFormat
# @brief Covariance2DFormat class
#
class Covariance2DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._XX = 'xx'
    self._XY = 'xy'
    self._XT = 'xt'
    self._YY = 'yy'
    self._YT = 'yt'
    self._TT = 'tt'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._XX:dtobj.xx, \
                 self._XY:dtobj.xy, \
                 self._XT:dtobj.xt, \
                 self._YY:dtobj.yy, \
                 self._YT:dtobj.yt, \
                 self._TT:dtobj.tt}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Covariance2D(\
              dictobj[self._TYPE_NAME][self._XX], \
              dictobj[self._TYPE_NAME][self._XY], \
              dictobj[self._TYPE_NAME][self._XT], \
              dictobj[self._TYPE_NAME][self._YY], \
              dictobj[self._TYPE_NAME][self._YT], \
              dictobj[self._TYPE_NAME][self._TT])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class PointCovariance2DFormat
# @brief PointCovariance2DFormat class
#
class PointCovariance2DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._XX = 'xx'
    self._XY = 'xy'
    self._YY = 'yy'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._XX:dtobj.xx, \
                 self._XY:dtobj.xy, \
                 self._YY:dtobj.yy}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.PointCovariance2D(\
              dictobj[self._TYPE_NAME][self._XX], \
              dictobj[self._TYPE_NAME][self._XY], \
              dictobj[self._TYPE_NAME][self._YY])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class CarlikeFormat
# @brief CarlikeFormat class
#
class CarlikeFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._SPEED = 'speed'
    self._STEERINGANGLE = 'steeringAngle'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._SPEED:dtobj.speed, \
                 self._STEERINGANGLE:dtobj.steeringAngle}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Carlike(\
              dictobj[self._TYPE_NAME][self._SPEED], \
              dictobj[self._TYPE_NAME][self._STEERINGANGLE])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class SpeedHeading2DFormat
# @brief SpeedHeading2DFormat class
#
class SpeedHeading2DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._SPEED = 'speed'
    self._HEADING = 'heading'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._SPEED:dtobj.speed, \
                 self._HEADING:dtobj.heading}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.SpeedHeading2D(\
              dictobj[self._TYPE_NAME][self._SPEED], \
              dictobj[self._TYPE_NAME][self._HEADING])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class PointOrVector3DFormat
# @brief PointOrVector3DFormat class
#
class PointOrVector3DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._X = 'x'
    self._Y = 'y'
    self._Z = 'z'
    self._FULL_DTNAME = "RTC." + any.to_any(self._datatype).typecode().name()

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._X:dtobj.x, \
                 self._Y:dtobj.y, \
                 self._Z:dtobj.z}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = eval(self._FULL_DTNAME)(\
              dictobj[self._TYPE_NAME][self._X], \
              dictobj[self._TYPE_NAME][self._Y], \
              dictobj[self._TYPE_NAME][self._Z])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Orientation3DFormat
# @brief Orientation3DFormat class
#
class Orientation3DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._R = 'r'
    self._P = 'p'
    self._Y = 'y'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._R:dtobj.r, \
                 self._P:dtobj.p, \
                 self._Y:dtobj.y}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Orientation3D(\
              dictobj[self._TYPE_NAME][self._R], \
              dictobj[self._TYPE_NAME][self._P], \
              dictobj[self._TYPE_NAME][self._Y])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Pose3DFormat
# @brief Pose3DFormat class
#
class Pose3DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._PT3D_NAME = 'position'
    self._X = 'x'
    self._Y = 'y'
    self._Z = 'z'
    self._OR3D_NAME = 'orientation'
    self._R = 'r'
    self._P = 'p'
    #self._Y = 'y'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._PT3D_NAME:\
                  {self._X:dtobj.position.x, \
                   self._Y:dtobj.position.y, \
                   self._Z:dtobj.position.z}, \
                 self._OR3D_NAME:\
                  {self._R:dtobj.orientation.r, \
                   self._P:dtobj.orientation.p, \
                   self._Y:dtobj.orientation.y}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Pose3D(\
              RTC.Point3D(\
                dictobj[self._TYPE_NAME][self._PT3D_NAME][self._X], \
                dictobj[self._TYPE_NAME][self._PT3D_NAME][self._Y], \
                dictobj[self._TYPE_NAME][self._PT3D_NAME][self._Z]), \
              RTC.Orientation3D(\
                dictobj[self._TYPE_NAME][self._OR3D_NAME][self._R], \
                dictobj[self._TYPE_NAME][self._OR3D_NAME][self._P], \
                dictobj[self._TYPE_NAME][self._OR3D_NAME][self._Y]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Velocity3DFormat
# @brief Velocity3DFormat class
#
class Velocity3DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._VX = 'vx'
    self._VY = 'vy'
    self._VZ = 'vz'
    self._VR = 'vr'
    self._VP = 'vp'
    self._VA = 'va'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._VX:dtobj.vx, \
                 self._VY:dtobj.vy, \
                 self._VZ:dtobj.vz, \
                 self._VR:dtobj.vr, \
                 self._VP:dtobj.vp, \
                 self._VA:dtobj.va}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Velocity3D(\
              dictobj[self._TYPE_NAME][self._VX], \
              dictobj[self._TYPE_NAME][self._VY], \
              dictobj[self._TYPE_NAME][self._VZ], \
              dictobj[self._TYPE_NAME][self._VR], \
              dictobj[self._TYPE_NAME][self._VP], \
              dictobj[self._TYPE_NAME][self._VA])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class AngularVelocity3DFormat
# @brief AngularVelocity3DFormat class
#
class AngularVelocity3DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._AVX = 'avx'
    self._AVY = 'avy'
    self._AVZ = 'avz'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._AVX:dtobj.avx, \
                 self._AVY:dtobj.avy, \
                 self._AVZ:dtobj.avz}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.AngularVelocity3D(\
              dictobj[self._TYPE_NAME][self._AVX], \
              dictobj[self._TYPE_NAME][self._AVY], \
              dictobj[self._TYPE_NAME][self._AVZ])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Acceleration3DFormat
# @brief Acceleration3DFormat class
#
class Acceleration3DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._AX = 'ax'
    self._AY = 'ay'
    self._AZ = 'az'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._AX:dtobj.ax, \
                 self._AY:dtobj.ay, \
                 self._AZ:dtobj.az}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Acceleration3D(\
              dictobj[self._TYPE_NAME][self._AX], \
              dictobj[self._TYPE_NAME][self._AY], \
              dictobj[self._TYPE_NAME][self._AZ])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class AngularAcceleration3DFormat
# @brief AngularAcceleration3DFormat class
#
class AngularAcceleration3DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._AAX = 'aax'
    self._AAY = 'aay'
    self._AAZ = 'aaz'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._AAX:dtobj.aax, \
                 self._AAY:dtobj.aay, \
                 self._AAZ:dtobj.aaz}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.AngularAcceleration3D(\
              dictobj[self._TYPE_NAME][self._AAX], \
              dictobj[self._TYPE_NAME][self._AAY], \
              dictobj[self._TYPE_NAME][self._AAZ])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class PoseVel3DFormat
# @brief PoseVel3DFormat class
#
class PoseVel3DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._PS3D_NAME = 'pose'
    self._PT3D_NAME = 'position'
    self._X = 'x'
    self._Y = 'y'
    self._Z = 'z'
    self._OR3D_NAME = 'orientation'
    self._R = 'r'
    self._P = 'p'
    #self._Y = 'y'
    self._VL3D_NAME = 'velocities'
    self._VX = 'vx'
    self._VY = 'vy'
    self._VZ = 'vz'
    self._VR = 'vr'
    self._VP = 'vp'
    self._VA = 'va'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._PS3D_NAME:\
                  {self._PT3D_NAME:\
                    {self._X:dtobj.pose.position.x, \
                     self._Y:dtobj.pose.position.y, \
                     self._Z:dtobj.pose.position.z}, \
                   self._OR3D_NAME:\
                    {self._R:dtobj.pose.orientation.r, \
                     self._P:dtobj.pose.orientation.p, \
                     self._Y:dtobj.pose.orientation.y}}, \
                 self._VL3D_NAME:\
                  {self._VX:dtobj.velocities.vx, \
                   self._VY:dtobj.velocities.vy, \
                   self._VZ:dtobj.velocities.vz, \
                   self._VR:dtobj.velocities.vr, \
                   self._VP:dtobj.velocities.vp, \
                   self._VA:dtobj.velocities.va}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.PoseVel3D(\
              RTC.Pose3D(\
                RTC.Point3D(\
                  dictobj[self._TYPE_NAME][self._PS3D_NAME][self._PT3D_NAME][self._X], \
                  dictobj[self._TYPE_NAME][self._PS3D_NAME][self._PT3D_NAME][self._Y], \
                  dictobj[self._TYPE_NAME][self._PS3D_NAME][self._PT3D_NAME][self._Z]), \
                RTC.Orientation3D(\
                  dictobj[self._TYPE_NAME][self._PS3D_NAME][self._OR3D_NAME][self._R], \
                  dictobj[self._TYPE_NAME][self._PS3D_NAME][self._OR3D_NAME][self._P], \
                  dictobj[self._TYPE_NAME][self._PS3D_NAME][self._OR3D_NAME][self._Y])), \
              RTC.Velocity3D(\
                dictobj[self._TYPE_NAME][self._VL3D_NAME][self._VX], \
                dictobj[self._TYPE_NAME][self._VL3D_NAME][self._VY], \
                dictobj[self._TYPE_NAME][self._VL3D_NAME][self._VZ], \
                dictobj[self._TYPE_NAME][self._VL3D_NAME][self._VR], \
                dictobj[self._TYPE_NAME][self._VL3D_NAME][self._VP], \
                dictobj[self._TYPE_NAME][self._VL3D_NAME][self._VA]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Size3DFormat
# @brief Size3DFormat class
#
class Size3DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._L = 'l'
    self._W = 'w'
    self._H = 'h'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._L:dtobj.l, \
                 self._W:dtobj.w, \
                 self._H:dtobj.h}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Size3D(\
              dictobj[self._TYPE_NAME][self._L], \
              dictobj[self._TYPE_NAME][self._W], \
              dictobj[self._TYPE_NAME][self._H])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Geometry3DFormat
# @brief Geometry3DFormat class
#
class Geometry3DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._PS3D_NAME = 'pose'
    self._PT3D_NAME = 'position'
    self._X = 'x'
    self._Y = 'y'
    self._Z = 'z'
    self._OR3D_NAME = 'orientation'
    self._R = 'r'
    self._P = 'p'
    #self._Y = 'y'
    self._SZ3D_NAME = 'size'
    self._L = 'l'
    self._W = 'w'
    self._H = 'h'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._PS3D_NAME:\
                  {self._PT3D_NAME:\
                    {self._X:dtobj.pose.position.x, \
                     self._Y:dtobj.pose.position.y, \
                     self._Z:dtobj.pose.position.z}, \
                   self._OR3D_NAME:\
                    {self._R:dtobj.pose.orientation.r, \
                     self._P:dtobj.pose.orientation.p, \
                     self._Y:dtobj.pose.orientation.y}}, \
                 self._SZ3D_NAME:\
                  {self._L:dtobj.size.l, \
                   self._W:dtobj.size.w, \
                   self._H:dtobj.size.h}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Geometry3D(\
              RTC.Pose3D(\
                RTC.Point3D(\
                  dictobj[self._TYPE_NAME][self._PS3D_NAME][self._PT3D_NAME][self._X], \
                  dictobj[self._TYPE_NAME][self._PS3D_NAME][self._PT3D_NAME][self._Y], \
                  dictobj[self._TYPE_NAME][self._PS3D_NAME][self._PT3D_NAME][self._Z]), \
                RTC.Orientation3D(\
                  dictobj[self._TYPE_NAME][self._PS3D_NAME][self._OR3D_NAME][self._R], \
                  dictobj[self._TYPE_NAME][self._PS3D_NAME][self._OR3D_NAME][self._P], \
                  dictobj[self._TYPE_NAME][self._PS3D_NAME][self._OR3D_NAME][self._Y])), \
              RTC.Size3D(\
                dictobj[self._TYPE_NAME][self._SZ3D_NAME][self._L], \
                dictobj[self._TYPE_NAME][self._SZ3D_NAME][self._W], \
                dictobj[self._TYPE_NAME][self._SZ3D_NAME][self._H]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class Covariance3DFormat
# @brief Covariance3DFormat class
#
class Covariance3DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._XX = 'xx'
    self._XY = 'xy'
    self._XZ = 'xz'
    self._XR = 'xr'
    self._XP = 'xp'
    self._XA = 'xa'
    self._YY = 'yy'
    self._YZ = 'yz'
    self._YR = 'yr'
    self._YP = 'yp'
    self._YA = 'ya'
    self._ZZ = 'zz'
    self._ZR = 'zr'
    self._ZP = 'zp'
    self._ZA = 'za'
    self._RR = 'rr'
    self._RP = 'rp'
    self._RA = 'ra'
    self._PP = 'pp'
    self._PA = 'pa'
    self._AA = 'aa'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._XX:dtobj.xx, \
                 self._XY:dtobj.xy, \
                 self._XZ:dtobj.xz, \
                 self._XR:dtobj.xr, \
                 self._XP:dtobj.xp, \
                 self._XA:dtobj.xa, \
                 self._YY:dtobj.yy, \
                 self._YZ:dtobj.yz, \
                 self._YR:dtobj.yr, \
                 self._YP:dtobj.yp, \
                 self._YA:dtobj.ya, \
                 self._ZZ:dtobj.zz, \
                 self._ZR:dtobj.zr, \
                 self._ZP:dtobj.zp, \
                 self._ZA:dtobj.za, \
                 self._RR:dtobj.rr, \
                 self._RP:dtobj.rp, \
                 self._RA:dtobj.ra, \
                 self._PP:dtobj.pp, \
                 self._PA:dtobj.pa, \
                 self._AA:dtobj.aa}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.Covariance3D(\
              dictobj[self._TYPE_NAME][self._XX], \
              dictobj[self._TYPE_NAME][self._XY], \
              dictobj[self._TYPE_NAME][self._XZ], \
              dictobj[self._TYPE_NAME][self._XR], \
              dictobj[self._TYPE_NAME][self._XP], \
              dictobj[self._TYPE_NAME][self._XA], \
              dictobj[self._TYPE_NAME][self._YY], \
              dictobj[self._TYPE_NAME][self._YZ], \
              dictobj[self._TYPE_NAME][self._YR], \
              dictobj[self._TYPE_NAME][self._YP], \
              dictobj[self._TYPE_NAME][self._YA], \
              dictobj[self._TYPE_NAME][self._ZZ], \
              dictobj[self._TYPE_NAME][self._ZR], \
              dictobj[self._TYPE_NAME][self._ZP], \
              dictobj[self._TYPE_NAME][self._ZA], \
              dictobj[self._TYPE_NAME][self._RR], \
              dictobj[self._TYPE_NAME][self._RP], \
              dictobj[self._TYPE_NAME][self._RA], \
              dictobj[self._TYPE_NAME][self._PP], \
              dictobj[self._TYPE_NAME][self._PA], \
              dictobj[self._TYPE_NAME][self._AA])
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class SpeedHeading3DFormat
# @brief SpeedHeading3DFormat class
#
class SpeedHeading3DFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._SPEED = 'speed'
    self._OR3D_NAME = 'direction'
    self._R = 'r'
    self._P = 'p'
    self._Y = 'y'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._SPEED:dtobj.speed, \
                 self._OR3D_NAME:\
                  {dtobj.direction.r, \
                   dtobj.direction.p, \
                   dtobj.direction.y}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.SpeedHeading3D(\
              dictobj[self._TYPE_NAME][self._SPEED], \
              RTC.Orientation3D(\
                dictobj[self._TYPE_NAME][self._OR3D_NAME][self._R], \
                dictobj[self._TYPE_NAME][self._OR3D_NAME][self._P], \
                dictobj[self._TYPE_NAME][self._OR3D_NAME][self._Y]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class OAPFormat
# @brief OAPFormat class
#
class OAPFormat(DataTypeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    DataTypeFormat.__init__(self, datatype, endian)
    self._VC3D1_NAME = 'orientation'
    self._VC3D2_NAME = 'approach'
    self._VC3D3_NAME = 'position'
    self._X = 'x'
    self._Y = 'y'
    self._Z = 'z'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._VC3D1_NAME:\
                  {self._X:dtobj.orientation.x, \
                   self._Y:dtobj.orientation.y, \
                   self._Z:dtobj.orientation.z}, \
                 self._VC3D2_NAME:\
                  {self._X:dtobj.approach.x, \
                   self._Y:dtobj.approach.y, \
                   self._Z:dtobj.approach.z}, \
                 self._VC3D3_NAME:\
                  {self._X:dtobj.position.x, \
                   self._Y:dtobj.position.y, \
                   self._Z:dtobj.position.z}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.OAP(\
              RTC.Vector3D(\
                dictobj[self._TYPE_NAME][self._VC3D1_NAME][self._X], \
                dictobj[self._TYPE_NAME][self._VC3D1_NAME][self._Y], \
                dictobj[self._TYPE_NAME][self._VC3D1_NAME][self._Z]), \
              RTC.Vector3D(\
                dictobj[self._TYPE_NAME][self._VC3D2_NAME][self._X], \
                dictobj[self._TYPE_NAME][self._VC3D2_NAME][self._Y], \
                dictobj[self._TYPE_NAME][self._VC3D2_NAME][self._Z]), \
              RTC.Vector3D(\
                dictobj[self._TYPE_NAME][self._VC3D3_NAME][self._X], \
                dictobj[self._TYPE_NAME][self._VC3D3_NAME][self._Y], \
                dictobj[self._TYPE_NAME][self._VC3D3_NAME][self._Z]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedRGBColourFormat
# @brief TimedRGBColourFormat class
#
class TimedRGBColourFormat(RGBColourFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    RGBColourFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._R:dtobj.data.r, \
                   self._G:dtobj.data.g, \
                   self._B:dtobj.data.b}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedRGBColour(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.RGBColour(\
                dictobj[self._TYPE_NAME][self._DATA][self._R], \
                dictobj[self._TYPE_NAME][self._DATA][self._G], \
                dictobj[self._TYPE_NAME][self._DATA][self._B]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedPointOrVector2DFormat
# @brief TimedPointOrVector2DFormat class
#
class TimedPointOrVector2DFormat(PointOrVector2DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    PointOrVector2DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'
    self._SUB_DTNAME = "RTC." + any.to_any(self._datatype.data).typecode().name()

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._X:dtobj.data.x, \
                   self._Y:dtobj.data.y}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = eval(self._FULL_DTNAME)(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              eval(self._SUB_DTNAME)(\
                dictobj[self._TYPE_NAME][self._DATA][self._X], \
                dictobj[self._TYPE_NAME][self._DATA][self._Y]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedPose2DFormat
# @brief TimedPose2DFormat class
#
class TimedPose2DFormat(Pose2DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Pose2DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._PT2D_NAME:\
                    {self._X:dtobj.data.position.x, \
                     self._Y:dtobj.data.position.y}, \
                   self._HEADING:dtobj.data.heading}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedPose2D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Pose2D(\
                RTC.Point2D(\
                  dictobj[self._TYPE_NAME][self._DATA][self._PT2D_NAME][self._X], \
                  dictobj[self._TYPE_NAME][self._DATA][self._PT2D_NAME][self._Y]), \
                dictobj[self._TYPE_NAME][self._DATA][self._HEADING]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedVelocity2DFormat
# @brief TimedVelocity2DFormat class
#
class TimedVelocity2DFormat(Velocity2DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Velocity2DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._VX:dtobj.data.vx, \
                   self._VY:dtobj.data.vy, \
                   self._VA:dtobj.data.va}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedVelocity2D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Velocity2D(\
                dictobj[self._TYPE_NAME][self._DATA][self._VX], \
                dictobj[self._TYPE_NAME][self._DATA][self._VY], \
                dictobj[self._TYPE_NAME][self._DATA][self._VA]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedAcceleration2DFormat
# @brief TimedAcceleration2DFormat class
#
class TimedAcceleration2DFormat(Acceleration2DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Acceleration2DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._AX:dtobj.data.ax, \
                   self._AY:dtobj.data.ay}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedAcceleration2D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Acceleration2D(\
                dictobj[self._TYPE_NAME][self._DATA][self._AX], \
                dictobj[self._TYPE_NAME][self._DATA][self._AY]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedPoseVel2DFormat
# @brief TimedPoseVel2DFormat class
#
class TimedPoseVel2DFormat(PoseVel2DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    PoseVel2DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._PS2D_NAME:\
                    {self._PT2D_NAME:\
                      {self._X:dtobj.data.pose.position.x, \
                       self._Y:dtobj.data.pose.position.y}, \
                     self._HEADING:dtobj.data.pose.heading}, \
                   self._VL2D_NAME:\
                    {self._VX:dtobj.data.velocities.vx, \
                     self._VY:dtobj.data.velocities.vy, \
                     self._VA:dtobj.data.velocities.va}}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedPoseVel2D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.PoseVel2D(\
                RTC.Pose2D(\
                  RTC.Point2D(\
                    dictobj[self._TYPE_NAME][self._DATA][self._PS2D_NAME][self._PT2D_NAME][self._X], \
                    dictobj[self._TYPE_NAME][self._DATA][self._PS2D_NAME][self._PT2D_NAME][self._Y]), \
                  dictobj[self._TYPE_NAME][self._DATA][self._PS2D_NAME][self._HEADING]), \
                RTC.Velocity2D(\
                  dictobj[self._TYPE_NAME][self._DATA][self._VL2D_NAME][self._VX], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VL2D_NAME][self._VY], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VL2D_NAME][self._VA])))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedSize2DFormat
# @brief TimedSize2DFormat class
#
class TimedSize2DFormat(Size2DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Size2DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._L:dtobj.data.l, \
                   self._W:dtobj.data.w}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedSize2D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Size2D(\
                dictobj[self._TYPE_NAME][self._DATA][self._L], \
                dictobj[self._TYPE_NAME][self._DATA][self._W]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedGeometry2DFormat
# @brief TimedGeometry2DFormat class
#
class TimedGeometry2DFormat(Geometry2DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Geometry2DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._PS2D_NAME:\
                    {self._PT2D_NAME:\
                      {self._X:dtobj.data.pose.position.x, \
                       self._Y:dtobj.data.pose.position.y}, \
                     self._HEADING:dtobj.data.pose.heading}, \
                   self._SZ2D_NAME:\
                    {self._L:dtobj.data.size.l, \
                     self._W:dtobj.data.size.w}}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedGeometry2D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Geometry2D(\
                RTC.Pose2D(\
                  RTC.Point2D(\
                    dictobj[self._TYPE_NAME][self._DATA][self._PS2D_NAME][self._PT2D_NAME][self._X], \
                    dictobj[self._TYPE_NAME][self._DATA][self._PS2D_NAME][self._PT2D_NAME][self._Y]), \
                  dictobj[self._TYPE_NAME][self._DATA][self._PS2D_NAME][self._HEADING]), \
                RTC.Size2D(\
                  dictobj[self._TYPE_NAME][self._DATA][self._SZ2D_NAME][self._L], \
                  dictobj[self._TYPE_NAME][self._DATA][self._SZ2D_NAME][self._W])))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedCovariance2DFormat
# @brief TimedCovariance2DFormat class
#
class TimedCovariance2DFormat(Covariance2DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Covariance2DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._XX:dtobj.data.xx, \
                   self._XY:dtobj.data.xy, \
                   self._XT:dtobj.data.xt, \
                   self._YY:dtobj.data.yy, \
                   self._YT:dtobj.data.yt, \
                   self._TT:dtobj.data.tt}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedCovariance2D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Covariance2D(\
                dictobj[self._TYPE_NAME][self._DATA][self._XX], \
                dictobj[self._TYPE_NAME][self._DATA][self._XY], \
                dictobj[self._TYPE_NAME][self._DATA][self._XT], \
                dictobj[self._TYPE_NAME][self._DATA][self._YY], \
                dictobj[self._TYPE_NAME][self._DATA][self._YT], \
                dictobj[self._TYPE_NAME][self._DATA][self._TT]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedPointCovariance2DFormat
# @brief TimedPointCovariance2DFormat class
#
class TimedPointCovariance2DFormat(PointCovariance2DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    PointCovariance2DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._XX:dtobj.data.xx, \
                   self._XY:dtobj.data.xy, \
                   self._YY:dtobj.data.yy}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedPointCovariance2D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.PointCovariance2D(\
                dictobj[self._TYPE_NAME][self._DATA][self._XX], \
                dictobj[self._TYPE_NAME][self._DATA][self._XY], \
                dictobj[self._TYPE_NAME][self._DATA][self._YY]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedCarlikeFormat
# @brief TimedCarlikeFormat class
#
class TimedCarlikeFormat(CarlikeFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    CarlikeFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._SPEED:dtobj.data.speed, \
                   self._STEERINGANGLE:dtobj.data.steeringAngle}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedCarlike(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Carlike(\
                dictobj[self._TYPE_NAME][self._DATA][self._SPEED], \
                dictobj[self._TYPE_NAME][self._DATA][self._STEERINGANGLE]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedSpeedHeading2DFormat
# @brief TimedSpeedHeading2DFormat class
#
class TimedSpeedHeading2DFormat(SpeedHeading2DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    SpeedHeading2DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._SPEED:dtobj.data.speed, \
                   self._HEADING:dtobj.data.heading}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedSpeedHeading2D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.SpeedHeading2D(\
                dictobj[self._TYPE_NAME][self._DATA][self._SPEED], \
                dictobj[self._TYPE_NAME][self._DATA][self._HEADING]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedPointOrVector3DFormat
# @brief TimedPointOrVector3DFormat class
#
class TimedPointOrVector3DFormat(PointOrVector3DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    PointOrVector3DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'
    self._SUB_DTNAME = "RTC." + any.to_any(self._datatype.data).typecode().name()

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._X:dtobj.data.x, \
                   self._Y:dtobj.data.y, \
                   self._Z:dtobj.data.z}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = eval(self._FULL_DTNAME)(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              eval(self._SUB_DTNAME)(\
                dictobj[self._TYPE_NAME][self._DATA][self._X], \
                dictobj[self._TYPE_NAME][self._DATA][self._Y], \
                dictobj[self._TYPE_NAME][self._DATA][self._Z]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedOrientation3DFormat
# @brief TimedOrientation3DFormat class
#
class TimedOrientation3DFormat(Orientation3DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Orientation3DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._R:dtobj.data.r, \
                   self._P:dtobj.data.p, \
                   self._Y:dtobj.data.y}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedOrientation3D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Orientation3D(\
                dictobj[self._TYPE_NAME][self._DATA][self._R], \
                dictobj[self._TYPE_NAME][self._DATA][self._P], \
                dictobj[self._TYPE_NAME][self._DATA][self._Y]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedPose3DFormat
# @brief TimedPose3DFormat class
#
class TimedPose3DFormat(Pose3DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Pose3DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._PT3D_NAME:\
                    {self._X:dtobj.data.position.x, \
                     self._Y:dtobj.data.position.y, \
                     self._Z:dtobj.data.position.z}, \
                   self._OR3D_NAME:\
                    {self._R:dtobj.data.orientation.r, \
                     self._P:dtobj.data.orientation.p, \
                     self._Y:dtobj.data.orientation.y}}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedPose3D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Pose3D(\
                RTC.Point3D(\
                  dictobj[self._TYPE_NAME][self._DATA][self._PT3D_NAME][self._X], \
                  dictobj[self._TYPE_NAME][self._DATA][self._PT3D_NAME][self._Y], \
                  dictobj[self._TYPE_NAME][self._DATA][self._PT3D_NAME][self._Z]), \
                RTC.Orientation3D(\
                  dictobj[self._TYPE_NAME][self._DATA][self._OR3D_NAME][self._R], \
                  dictobj[self._TYPE_NAME][self._DATA][self._OR3D_NAME][self._P], \
                  dictobj[self._TYPE_NAME][self._DATA][self._OR3D_NAME][self._Y])))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedVelocity3DFormat
# @brief TimedVelocity3DFormat class
#
class TimedVelocity3DFormat(Velocity3DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Velocity3DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._VX:dtobj.data.vx, \
                   self._VY:dtobj.data.vy, \
                   self._VZ:dtobj.data.vz, \
                   self._VR:dtobj.data.vr, \
                   self._VP:dtobj.data.vp, \
                   self._VA:dtobj.data.va}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedVelocity3D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Velocity3D(\
                dictobj[self._TYPE_NAME][self._DATA][self._VX], \
                dictobj[self._TYPE_NAME][self._DATA][self._VY], \
                dictobj[self._TYPE_NAME][self._DATA][self._VZ], \
                dictobj[self._TYPE_NAME][self._DATA][self._VR], \
                dictobj[self._TYPE_NAME][self._DATA][self._VP], \
                dictobj[self._TYPE_NAME][self._DATA][self._VA]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedAngularVelocity3DFormat
# @brief TimedAngularVelocity3DFormat class
#
class TimedAngularVelocity3DFormat(AngularVelocity3DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    AngularVelocity3DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._AVX:dtobj.data.avx, \
                   self._AVY:dtobj.data.avy, \
                   self._AVZ:dtobj.data.avz}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedAngularVelocity3D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.AngularVelocity3D(\
                dictobj[self._TYPE_NAME][self._DATA][self._AVX], \
                dictobj[self._TYPE_NAME][self._DATA][self._AVY], \
                dictobj[self._TYPE_NAME][self._DATA][self._AVZ]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedAcceleration3DFormat
# @brief TimedAcceleration3DFormat class
#
class TimedAcceleration3DFormat(Acceleration3DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Acceleration3DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._AX:dtobj.data.ax, \
                   self._AY:dtobj.data.ay, \
                   self._AZ:dtobj.data.az}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedAcceleration3D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Acceleration3D(\
                dictobj[self._TYPE_NAME][self._DATA][self._AX], \
                dictobj[self._TYPE_NAME][self._DATA][self._AY], \
                dictobj[self._TYPE_NAME][self._DATA][self._AZ]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedAngularAcceleration3DFormat
# @brief TimedAngularAcceleration3DFormat class
#
class TimedAngularAcceleration3DFormat(AngularAcceleration3DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    AngularAcceleration3DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._AAX:dtobj.data.aax, \
                   self._AAY:dtobj.data.aay, \
                   self._AAZ:dtobj.data.aaz}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedAngularAcceleration3D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.AngularAcceleration3D(\
                dictobj[self._TYPE_NAME][self._DATA][self._AAX], \
                dictobj[self._TYPE_NAME][self._DATA][self._AAY], \
                dictobj[self._TYPE_NAME][self._DATA][self._AAZ]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedPoseVel3DFormat
# @brief TimedPoseVel3DFormat class
#
class TimedPoseVel3DFormat(PoseVel3DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    PoseVel3DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._PS3D_NAME:\
                    {self._PT3D_NAME:\
                      {self._X:dtobj.data.pose.position.x, \
                       self._Y:dtobj.data.pose.position.y, \
                       self._Z:dtobj.data.pose.position.z}, \
                     self._OR3D_NAME:\
                      {self._R:dtobj.data.pose.orientation.r, \
                       self._P:dtobj.data.pose.orientation.p, \
                       self._Y:dtobj.data.pose.orientation.y}}, \
                   self._VL3D_NAME:\
                    {self._VX:dtobj.data.velocities.vx, \
                     self._VY:dtobj.data.velocities.vy, \
                     self._VZ:dtobj.data.velocities.vz, \
                     self._VR:dtobj.data.velocities.vr, \
                     self._VP:dtobj.data.velocities.vp, \
                     self._VA:dtobj.data.velocities.va}}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedPoseVel3D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.PoseVel3D(\
                RTC.Pose3D(\
                  RTC.Point3D(\
                    dictobj[self._TYPE_NAME][self._DATA][self._PS3D_NAME][self._PT3D_NAME][self._X], \
                    dictobj[self._TYPE_NAME][self._DATA][self._PS3D_NAME][self._PT3D_NAME][self._Y], \
                    dictobj[self._TYPE_NAME][self._DATA][self._PS3D_NAME][self._PT3D_NAME][self._Z]), \
                  RTC.Orientation3D(\
                    dictobj[self._TYPE_NAME][self._DATA][self._PS3D_NAME][self._OR3D_NAME][self._R], \
                    dictobj[self._TYPE_NAME][self._DATA][self._PS3D_NAME][self._OR3D_NAME][self._P], \
                    dictobj[self._TYPE_NAME][self._DATA][self._PS3D_NAME][self._OR3D_NAME][self._Y])), \
                RTC.Velocity3D(\
                  dictobj[self._TYPE_NAME][self._DATA][self._VL3D_NAME][self._VX], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VL3D_NAME][self._VY], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VL3D_NAME][self._VZ], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VL3D_NAME][self._VR], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VL3D_NAME][self._VP], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VL3D_NAME][self._VA])))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedSize3DFormat
# @brief TimedSize3DFormat class
#
class TimedSize3DFormat(Size3DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Size3DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._L:dtobj.data.l, \
                   self._W:dtobj.data.w, \
                   self._H:dtobj.data.h}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedSize3D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Size3D(\
                dictobj[self._TYPE_NAME][self._DATA][self._L], \
                dictobj[self._TYPE_NAME][self._DATA][self._W], \
                dictobj[self._TYPE_NAME][self._DATA][self._H]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedGeometry3DFormat
# @brief TimedGeometry3DFormat class
#
class TimedGeometry3DFormat(Geometry3DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Geometry3DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._PS3D_NAME:\
                    {self._PT3D_NAME:\
                      {self._X:dtobj.data.pose.position.x, \
                       self._Y:dtobj.data.pose.position.y, \
                       self._Z:dtobj.data.pose.position.z}, \
                     self._OR3D_NAME:\
                      {self._R:dtobj.data.pose.orientation.r, \
                       self._P:dtobj.data.pose.orientation.p, \
                       self._Y:dtobj.data.pose.orientation.y}}, \
                   self._SZ3D_NAME:\
                    {self._L:dtobj.data.size.l, \
                     self._W:dtobj.data.size.w, \
                     self._H:dtobj.data.size.h}}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedGeometry3D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Geometry3D(\
                RTC.Pose3D(\
                  RTC.Point3D(\
                    dictobj[self._TYPE_NAME][self._DATA][self._PS3D_NAME][self._PT3D_NAME][self._X], \
                    dictobj[self._TYPE_NAME][self._DATA][self._PS3D_NAME][self._PT3D_NAME][self._Y], \
                    dictobj[self._TYPE_NAME][self._DATA][self._PS3D_NAME][self._PT3D_NAME][self._Z]), \
                  RTC.Orientation3D(\
                    dictobj[self._TYPE_NAME][self._DATA][self._PS3D_NAME][self._OR3D_NAME][self._R], \
                    dictobj[self._TYPE_NAME][self._DATA][self._PS3D_NAME][self._OR3D_NAME][self._P], \
                    dictobj[self._TYPE_NAME][self._DATA][self._PS3D_NAME][self._OR3D_NAME][self._Y])), \
                RTC.Size3D(\
                  dictobj[self._TYPE_NAME][self._DATA][self._SZ3D_NAME][self._L], \
                  dictobj[self._TYPE_NAME][self._DATA][self._SZ3D_NAME][self._W], \
                  dictobj[self._TYPE_NAME][self._DATA][self._SZ3D_NAME][self._H])))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedCovariance3DFormat
# @brief TimedCovariance3DFormat class
#
class TimedCovariance3DFormat(Covariance3DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    Covariance3DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._XX:dtobj.data.xx, \
                   self._XY:dtobj.data.xy, \
                   self._XZ:dtobj.data.xz, \
                   self._XR:dtobj.data.xr, \
                   self._XP:dtobj.data.xp, \
                   self._XA:dtobj.data.xa, \
                   self._YY:dtobj.data.yy, \
                   self._YZ:dtobj.data.yz, \
                   self._YR:dtobj.data.yr, \
                   self._YP:dtobj.data.yp, \
                   self._YA:dtobj.data.ya, \
                   self._ZZ:dtobj.data.zz, \
                   self._ZR:dtobj.data.zr, \
                   self._ZP:dtobj.data.zp, \
                   self._ZA:dtobj.data.za, \
                   self._RR:dtobj.data.rr, \
                   self._RP:dtobj.data.rp, \
                   self._RA:dtobj.data.ra, \
                   self._PP:dtobj.data.pp, \
                   self._PA:dtobj.data.pa, \
                   self._AA:dtobj.data.aa}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedCovariance3D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.Covariance3D(\
                dictobj[self._TYPE_NAME][self._DATA][self._XX], \
                dictobj[self._TYPE_NAME][self._DATA][self._XY], \
                dictobj[self._TYPE_NAME][self._DATA][self._XZ], \
                dictobj[self._TYPE_NAME][self._DATA][self._XR], \
                dictobj[self._TYPE_NAME][self._DATA][self._XP], \
                dictobj[self._TYPE_NAME][self._DATA][self._XA], \
                dictobj[self._TYPE_NAME][self._DATA][self._YY], \
                dictobj[self._TYPE_NAME][self._DATA][self._YZ], \
                dictobj[self._TYPE_NAME][self._DATA][self._YR], \
                dictobj[self._TYPE_NAME][self._DATA][self._YP], \
                dictobj[self._TYPE_NAME][self._DATA][self._YA], \
                dictobj[self._TYPE_NAME][self._DATA][self._ZZ], \
                dictobj[self._TYPE_NAME][self._DATA][self._ZR], \
                dictobj[self._TYPE_NAME][self._DATA][self._ZP], \
                dictobj[self._TYPE_NAME][self._DATA][self._ZA], \
                dictobj[self._TYPE_NAME][self._DATA][self._RR], \
                dictobj[self._TYPE_NAME][self._DATA][self._RP], \
                dictobj[self._TYPE_NAME][self._DATA][self._RA], \
                dictobj[self._TYPE_NAME][self._DATA][self._PP], \
                dictobj[self._TYPE_NAME][self._DATA][self._PA], \
                dictobj[self._TYPE_NAME][self._DATA][self._AA]))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedSpeedHeading3DFormat
# @brief TimedSpeedHeading3DFormat class
#
class TimedSpeedHeading3DFormat(SpeedHeading3DFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    SpeedHeading3DFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._SPEED:dtobj.data.speed, \
                   self._OR3D_NAME:\
                    {dtobj.data.direction.r, \
                     dtobj.data.direction.p, \
                     dtobj.data.direction.y}}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedSpeedHeading3D(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.SpeedHeading3D(\
                dictobj[self._TYPE_NAME][self._DATA][self._SPEED], \
                RTC.Orientation3D(\
                  dictobj[self._TYPE_NAME][self._DATA][self._OR3D_NAME][self._R], \
                  dictobj[self._TYPE_NAME][self._DATA][self._OR3D_NAME][self._P], \
                  dictobj[self._TYPE_NAME][self._DATA][self._OR3D_NAME][self._Y])))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata

##
# @class TimedOAPFormat
# @brief TimedOAPFormat class
#
class TimedOAPFormat(OAPFormat):

  ##
  # @brief Constructor
  #
  def __init__(self, datatype, endian):
    OAPFormat.__init__(self, datatype, endian)
    self._TM_NAME = 'tm'
    self._SEC = 'sec'
    self._NSEC = 'nsec'
    self._DATA = 'data'

  ##
  # @brief Reserialize from CDR to JSON
  # @param cdrdata CDR marshaled data
  # @return jsontext JSON serialized data
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dtobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {self._TYPE_NAME:\
                {self._TM_NAME:\
                  {self._SEC:dtobj.tm.sec, \
                   self._NSEC:dtobj.tm.nsec}, \
                 self._DATA:\
                  {self._VC3D1_NAME:\
                    {self._X:dtobj.data.orientation.x, \
                     self._Y:dtobj.data.orientation.y, \
                     self._Z:dtobj.data.orientation.z}, \
                   self._VC3D2_NAME:\
                    {self._X:dtobj.data.approach.x, \
                     self._Y:dtobj.data.approach.y, \
                     self._Z:dtobj.data.approach.z}, \
                   self._VC3D3_NAME:\
                    {self._X:dtobj.data.position.x, \
                     self._Y:dtobj.data.position.y, \
                     self._Z:dtobj.data.position.z}}}}
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  # @param jsontext JSON serialized data
  # @return cdrdata CDR marshaled data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dtobj = RTC.TimedOAP(\
              RTC.Time(\
                dictobj[self._TYPE_NAME][self._TM_NAME][self._SEC], \
                dictobj[self._TYPE_NAME][self._TM_NAME][self._NSEC]), \
              RTC.OAP(\
                RTC.Vector3D(\
                  dictobj[self._TYPE_NAME][self._DATA][self._VC3D1_NAME][self._X], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VC3D1_NAME][self._Y], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VC3D1_NAME][self._Z]), \
                RTC.Vector3D(\
                  dictobj[self._TYPE_NAME][self._DATA][self._VC3D2_NAME][self._X], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VC3D2_NAME][self._Y], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VC3D2_NAME][self._Z]), \
                RTC.Vector3D(\
                  dictobj[self._TYPE_NAME][self._DATA][self._VC3D3_NAME][self._X], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VC3D3_NAME][self._Y], \
                  dictobj[self._TYPE_NAME][self._DATA][self._VC3D3_NAME][self._Z])))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dtobj, self._endian)

    return cdrdata
