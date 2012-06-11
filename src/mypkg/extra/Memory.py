'''
Created on 30 mai 2012

@author: jade
'''
import os

class Memory(object):
    '''
    classdocs
    '''


    def __init__(self, _proc_status):
        '''
        Constructor
        '''
        self._proc_status = _proc_status
        self._scale = {'kB': 1024.0, 'mB': 1024.0*1024.0,
          'KB': 1024.0, 'MB': 1024.0*1024.0}
    

    def _VmB(self, VmKey):
        '''Private.
        '''
        global _proc_status, _scale
        # get pseudo file  /proc/<pid>/status
        try:
            t = open(_proc_status)
            v = t.read()
            t.close()
        except:
            return 0.0  # non-Linux?
            # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
        i = v.index(VmKey)
        v = v[i:].split(None, 3)  # whitespace
        if len(v) < 3:
            return 0.0  # invalid format?
            # convert Vm value to bytes
        return float(v[1]) * _scale[v[2]]

    def memory(self, since=0.0):
        '''Return memory usage in bytes.
        '''
        return self._VmB('VmSize:') - since
    
    def resident(self, since=0.0):
        '''Return resident memory usage in bytes.
        '''
        return self._VmB('VmRSS:') - since
    
    def stacksize(self, since=0.0):
        '''Return stack size in bytes.
        '''
        return self._VmB('VmStk:') - since