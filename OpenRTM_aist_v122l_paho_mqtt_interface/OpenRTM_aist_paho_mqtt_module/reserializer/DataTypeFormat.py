#!/usr/bin/env python3
# -*- coding: euc-jp -*-

##
# @file  DataTypeFormat.py
# @brief DataTypeFormat class
# @date   2020/12/07
# @author Daishi Yoshino
#
# Copyright (C) 2020
#     Daishi Yoshino
#     Revitalization Center
#     University of Aizu, Japan
#

from omniORB import *
import OpenRTM_aist
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
    self._TYPE_NAME = 'RTC.' + any.to_any(self._datatype).typecode().name()

  ##
  # @brief Convert DataType object to dict object
  #
  def convertDataTypeToDict(self, dataobj):
    dictobj = {}
    for key, val in vars(dataobj).items():
      if hasattr(val, '__dict__'):
        dictobj[key] = self.convertDataTypeToDict(val)
      else:
        dictobj[key] = val

    return dictobj

  ##
  # @brief Convert dict object to DataType object
  #
  def convertDictToDataType(self, dictobj, datatype):
    dataobj = OpenRTM_aist.instantiateDataType(datatype)
    for key, val in dictobj.items():
      item = dataobj.__dict__[key]
      if isinstance(val, dict):
        dataobj.__dict__[key] = self.convertDictToDataType(val, item)
      else:
        dataobj.__dict__[key] = val

    return dataobj

  ##
  # @brief Reserialize from CDR to JSON
  #
  # CDR data -> (unmarshal) -> DataType object -> convertDataTypeToDict() -> dict object-> (serialize) -> JSON text
  #
  def reserializeFromCdrToJson(self, cdrdata):
    dataobj = cdrUnmarshal(any.to_any(self._datatype).typecode(), cdrdata, self._endian)
    dictobj = {}
    dictobj[self._TYPE_NAME] = self.convertDataTypeToDict(dataobj)
    jsontext = json.dumps(dictobj)

    return jsontext

  ##
  # @brief Reserialize from JSON to CDR
  #
  # JSON text -> (deserialize) -> dict object -> convertDictToDataType() -> DataType object -> (marshal) -> CDR data
  #
  def reserializeFromJsonToCdr(self, jsontext):
    dictobj = json.loads(jsontext)
    dictobj = dictobj[self._TYPE_NAME]
    dataobj = self.convertDictToDataType(dictobj, eval(self._TYPE_NAME))
    cdrdata = cdrMarshal(any.to_any(self._datatype).typecode(), dataobj, self._endian)

    return cdrdata
