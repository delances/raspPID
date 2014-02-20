#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 DeLance Schmidt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""PID Controller.

"""
import sys
import subprocess
import os
import fnmatch
import argparse
import re

class Error(Exception):
    pass

class PIDController( object ):
    """Main class"""
    def __init__(self, kp, ki, kd, sampleTime, setpoint,
                 outputMax, outputMin, inputFunction, directController = True):
        """Instantiates a PID Controller"""
        self.directController = directController
        self.sampleTime = sampleTime
        self.set_tunings(kp, ki, kd)
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.on = False
        
        self.setpoint = setpoint
        self.lastError = 0.0
        self.errorSum = 0.0
        self.lastInput = 0.0
        self.iTerm = 0.0
        self.output = 0.0
        self.outputMax = outputMax
        self.outputMin = outputMin
        if ( not ( outputMin < outputMax ) ) or ( (outputMax == 0) and (outputMin == 0)):
            raise Error( 'Invalid output minimum and maximum' )
        self.inputReading = inputFunction
        
    def set_tunings(self, kp, ki, kd):
        """Sets the tuning values for the PID """
        
        if ( kp < 0) or ( ki < 0 ) or ( kd < 0):
            raise Error( 'kp, ki, and kd cannot be less than zero.' )
        sampleTimeInSec = self.sampleTime / 1000
        self.kp = kp
        self.ki = ki * sampleTimeInSec
        self.kd = kd / sampleTimeInSec
        
        if not self.directController:
            self.kp = 0 - self.kp
            self.ki = 0 - self.ki
            self.kd = 0 - self.kd
        
        
        
    def set_sample_time(self, sampleTime):
        """Sets the sample time for the PID """
        if (sampleTime > 0):
            ratio = sampleTime / self.sampleTime
            self.ki = self.ki * ratio
            self.kd = self.kd * ratio
            self.sampleTime = sampleTime
            
        
        
    def compute(self ):
        """Compute the return value of the PID """
        if not self.on:
            return self.output
        
        inputReading = self.inputReading()
        error = self.setpoint - inputReading
        self.errorSum = self.errorSum + error
        self.iTerm = self.iTerm + ( self.ki * error)
        dInput = inputReading - self.lastInput
        
        self.output = self.kp * error + self.iTerm + self.kd * dInput
        
        if ( self.output > self.outputMax ):
            self.output = self.outputMax
        elif( self.output < self.outputMin ):
            self.output = self.outputMin

        
        self.lastError = error
        self.lastInput = inputReading
        
        return self.output
    
    def start(self):
        if not self.on:
            self._initialize()
            
        self.on = True
        
    def stop(self):
        self.on = False
        
    def _initialize(self):
        self.lastInput = self.inputReading()
        self.iTerm = self.output
        if ( self.iTerm > self.outputMax ):
            self.iTerm = self.outputMax
        elif( self.iTerm < self.outputMin ):
            self.iTerm = self.outputMin
            
            

def main():
    parser = argparse.ArgumentParser(description='Python PID controller.')
    parser.add_argument( 'kp', help='Proportional value.' )
    parser.add_argument( 'ki', help='Integral value.' )
    parser.add_argument( 'kd', help='Derivative value.' )
    parser.add_argument( 'SampleTime', help='Sample time in milliseconds.' )
    parser.add_argument( 'Setpoint', help='Setpoint for the controller.' )
    parser.add_argument( 'Output Min', help='Maximum output for PID.' )
    parser.add_argument( 'Output Max', help='Minimum output for PID.' )
    
    args = parser.parse_args()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
