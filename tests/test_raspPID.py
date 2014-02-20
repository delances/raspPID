#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_raspPID
----------------------------------

Tests for `raspPID` module.
"""

import unittest

from raspPID import raspPID

class IdealHeatingProcess(object):
    def __init__(self, current, heatingMax, cooling):
        self.current = current
        self.heatingMax = heatingMax
        self.cooling = cooling
        self.currentHeating = 0
        
    def currentTemp(self):
        self.current = self.current + self.currentHeating - self.cooling
        return self.current

class TestRasppid(unittest.TestCase):

    def setUp(self):
        self.process = IdealHeatingProcess(100.0, 10.0, 1.0)
        self.PID = raspPID.PIDController( 0.5, 0.05, 0.00001, 1.0, 200.0, 10.0, 0.0, self.process.currentTemp )

    def test_basic_pid(self):
        self.PID.start()
        for x in range(0, 1000):
            setting = self.PID.compute()
            self.process.currentHeating = setting
            #print( "{0},{1}".format( self.process.current, setting ) )
           
        self.assertTrue( self.process.current > 198 and self.process.current < 201  )
        self.PID.stop()

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()