#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file CPUAffinity.py
# @brief 
# @date $Date$
# @author Nobuhiko Miyamoto
#

import sys
import os
import platform
import ctypes


##
# @if jp
# @brief CPU���ֹ�ꥹ�Ȥ��Ѵ�
#
# @param cpu_num_list CPU���ֹ�ꥹ��
# @return ����
#
# @else
# @brief 
#
# @param cpu_num_list
# @return 
#
# @endif
#
def listToCUPNUM(cpu_num_list):
  cpu_num = 0
  try:
    for num in cpu_num_list:
      p = 0x01 << (int(num))
      cpu_num += p
  except ValueError:
    pass
  return cpu_num
    
    
##
# @if jp
# @brief �ץ�������CPU���ե��˥ƥ�������
#
# @param cpu_num_list CPU���ֹ�ꥹ��
# @return ������True�����Ԥ�False
#
# @else
# @brief 
#
# @param cpu_num_list
# @return 
#
# @endif
#
def setProcessAffinity(cpu_num_list):
  cpu_num = listToCUPNUM(cpu_num_list)
  if cpu_num == 0:
    return False
  pid = os.getpid()
  
  if platform.system() == "Windows":
    
    PROCESS_QUERY_INFORMATION   = 0x0400
    PROCESS_SET_INFORMATION     = 0x0200


    
    flag = PROCESS_QUERY_INFORMATION | PROCESS_SET_INFORMATION
    h = ctypes.windll.kernel32.OpenProcess(flag, 0, pid)

    
    result = ctypes.windll.kernel32.SetProcessAffinityMask(ctypes.windll.kernel32.GetCurrentProcess(), cpu_num)
    processMask = ctypes.c_long()
    systemMask = ctypes.c_long()
    result = ctypes.windll.kernel32.GetProcessAffinityMask(ctypes.windll.kernel32.GetCurrentProcess(),ctypes.byref(processMask),ctypes.byref(systemMask))
    
    if processMask.value != cpu_num:
      return False
    else:
      return True
    
  else:
    from ctypes.util import find_library
    pthread = find_library("pthread")
    if pthread is None:
      return False
    pthread = ctypes.CDLL(pthread)
    
    mask = ctypes.c_long()
    mask.value = cpu_num
    result = pthread.sched_setaffinity(pid, ctypes.sizeof(mask), ctypes.byref(mask))
    if result != 0:
      return False
    mask = ctypes.c_long()
    result = pthread.sched_getaffinity(pid, ctypes.sizeof(mask), ctypes.byref(mask))
    if mask.value != cpu_num:
      return False
    else:
      return True


##
# @if jp
# @brief ����åɤ�CPU���ե��˥ƥ�������
#
# @param cpu_num_list CPU���ֹ�ꥹ��
# @return ������True�����Ԥ�False
#
# @else
# @brief 
#
# @param cpu_num_list
# @return 
#
# @endif
#
def setThreadAffinity(cpu_num_list):
  cpu_num = listToCUPNUM(cpu_num_list)
  if cpu_num == 0:
    return False
  
  
  if platform.system() == "Windows":
    PROCESS_QUERY_INFORMATION   = 0x0400
    PROCESS_SET_INFORMATION     = 0x0200



    h = ctypes.windll.kernel32.GetCurrentThread()
    
    result = ctypes.windll.kernel32.SetThreadAffinityMask(h, cpu_num)
    result = ctypes.windll.kernel32.SetThreadAffinityMask(h, cpu_num)
    
    if result != cpu_num:
      return False
    
    return True
    
  else:
    from ctypes.util import find_library
    pthread = find_library("pthread")
    if pthread is None:
      return False
    pthread = ctypes.CDLL(pthread)
    libc = find_library("libc")
    libc = ctypes.CDLL(libc)
    
    mask = ctypes.c_long()
    mask.value = cpu_num
    tid = libc.syscall(186)
    result = pthread.sched_setaffinity(tid, ctypes.sizeof(mask), ctypes.byref(mask))
    if result != 0:
      return False
    mask = ctypes.c_long()
    result = pthread.sched_getaffinity(tid, ctypes.sizeof(mask), ctypes.byref(mask))
    if mask.value != cpu_num:
      return False
    else:
      return True
