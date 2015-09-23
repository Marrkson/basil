#
# ------------------------------------------------------------
# Copyright (c) All rights reserved
# SiLab, Institute of Physics, University of Bonn
# ------------------------------------------------------------
#
# An interface to HDL simulator thatnks to cocotb [http://cocotb.readthedocs.org/]
#

import socket
import array
import time
import logging

from basil.TL.SiTransferLayer import SiTransferLayer
from basil.utils.sim.Protocol import WriteRequest, ReadRequest, ReadResponse, PickleInterface


class SiSim (SiTransferLayer):

    def __init__(self, conf):
        super(SiSim, self).__init__(conf)
        self._sock = None

    def init(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = self._init.pop('host', 'localhost')
        port = self._init.pop('port', 12345)
        try_cnt = self._init.pop('timeout', 60)

        # try few times for simulator to setup
        while(self._sock.connect_ex((host, port)) != 0):
            logging.debug("Trying to connect to simulator.")
            time.sleep(1)
            try_cnt -= 1
            if(try_cnt < 1):
                raise IOError("No connection to simulation server.")

        self._iface = PickleInterface(self._sock)  # exeption?

    def write(self, addr, data):
        ad = array.array('B', data)
        req = WriteRequest(addr, ad)
        self._iface.send(req)

    def read(self, addr, size):
        req = ReadRequest(addr, size)
        self._iface.send(req)
        resp = self._iface.recv()
        if not isinstance(resp, ReadResponse):
            raise ValueError("Communication error with Simulation: got %s" % repr(resp))
        return array.array('B', resp.data)

    def close(self):
        self._sock.close()
