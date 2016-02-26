#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file  OutPortSHMProvider.py
# @brief OutPortSHMProvider class
# @date  $Date: 2016-01-12 $
# @author Nobuhiko Miyamoto
#
#

import sys
from omniORB import any
import OpenRTM_aist
import OpenRTM
import OpenRTM__POA

import threading

##
# @if jp
# @class OutPortSHMConsumer
#
# @brief OutPortSHMConsumer ���饹
#
# �̿����ʤ� ��ͭ���� �����Ѥ������ϥݡ��ȥץ��Х������μ������饹��
#
#
# @else
# @class OutPortSHMConsumer
#
# @brief OutPortSHMConsumer class
#
#
# @endif
#
class OutPortSHMConsumer(OpenRTM_aist.OutPortCorbaCdrConsumer):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @else
  # @brief Constructor
  #
  # Constructor
  #
  # @endif
  #
  def __init__(self):
    OpenRTM_aist.OutPortCorbaCdrConsumer.__init__(self)
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("OutPortSHMConsumer")

    self._shmem = OpenRTM_aist.SharedMemory()
      
    self._mutex = threading.RLock()
    self._outportcdr = None

    return

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @else
  # @brief Destructor
  #
  # Destructor
  #
  # @endif
  #
  def __del__(self, CorbaConsumer=OpenRTM_aist.CorbaConsumer):
    self._rtcout.RTC_PARANOID("~OutPortSHMConsumer()")
    CorbaConsumer.__del__(self)
    self._outportcdr.close_memory(True)
    


  ##
  # @if jp
  # @brief ��������
  #
  # OutPortConsumer�γƼ������Ԥ�
  #
  # @param self
  # @param prop ���ͥ����ץ��ѥƥ�
  #
  # @else
  # @brief Initializing configuration
  #
  #
  # @endif
  #
  # virtual void init(coil::Properties& prop);
  def init(self, prop):
    self._rtcout.RTC_TRACE("init()")
    
    self._properties = prop
        
    return


  


  ##
  # @if jp
  # @brief �ǡ������ɤ߽Ф�
  #
  # ���ꤵ�줿�ǡ������ɤ߽Ф���
  #
  # �ǡ����Υ������϶�ͭ�������Ƭ8byte�����������
  # �ǡ����϶�ͭ���꤫���ɤ߹���
  #
  # @param data �ɤ߽Ф����ǡ����������륪�֥�������
  #
  # @return �꥿���󥳡���
  #
  # @else
  # @brief Read data
  #
  # Read set data
  #
  # @param data Object to receive the read data
  #
  # @return Return Code
  #
  # @endif
  #
  # virtual ReturnCode get(cdrMemoryStream& data);
  def get(self, data):
    self._rtcout.RTC_PARANOID("get()")
    
    try:
      outportcdr = self.getObject()._narrow(OpenRTM__POA.SharedMemory)
      
      if self._outportcdr is None:
        outportcdr.setInterface(self._shmem._this())
        self._outportcdr = outportcdr

      guard = OpenRTM_aist.ScopedLock(self._mutex)
      ret = outportcdr.get()
      
      if ret == OpenRTM.PORT_OK:
        self._rtcout.RTC_DEBUG("get() successful")

        
        
        shm_data = self._shmem.read()
        

        data[0] = shm_data
        self.onReceived(data[0])
        self.onBufferWrite(data[0])
        
        if self._buffer.full():
          self._rtcout.RTC_INFO("InPort buffer is full.")
          self.onBufferFull(data[0])
          self.onReceiverFull(data[0])
        
        self._buffer.put(data[0])
        self._buffer.advanceWptr()
        self._buffer.advanceRptr()

        return self.PORT_OK
      return self.convertReturn(ret,data[0])

    except:
      self._rtcout.RTC_WARN("Exception caught from OutPort.get().")
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return self.CONNECTION_LOST

    self._rtcout.RTC_ERROR("get(): Never comes here.")
    return self.UNKNOWN_ERROR


  


def OutPortSHMConsumerInit():
  factory = OpenRTM_aist.OutPortConsumerFactory.instance()
  factory.addFactory("shared_memory",
                     OpenRTM_aist.OutPortSHMConsumer,
                     OpenRTM_aist.Delete)
  return