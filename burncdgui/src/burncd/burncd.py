#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Description:	Klassen zum Umgang mit burncd
Version:	0.1
Copyright:	2005 by Thomas Flaig t.gf@freenet.de
Created:	21.Feb.2005
Last modified:	21.Feb.2005
License:        BSD
Requirements:   burncd in /usr/sbin/burncd (as it is used to be for FreeBSD)
"""


from types import StringType
from os import system

__all__=["databurner","audioburner","dvdrwburner","vcdburner"]

class burner(object):
	device="/dev/acd1"
	mode="data"
	fixate=1
	speed="max"
	command="/usr/sbin/burncd"
	def __init__(self,data):
		self.data=data
		
	def change_cddevice(self, name):
		self.device=name
	def change_mode(self,mode):
		self.mode=mode
	def change_fixate(self, int):
		self.fixate=int
	def change_speed(self, speed):
		self.speed=speed
	def burn(self):
		if isinstance(self.data, StringType):
			commandline=self.command +" -f" + self.device 
			commandline+= " -s " +self.speed
			commandline+= " " + self.mode + " " + self.data
			if self.fixate:
				commandline+= " " + "fixate"
			value=system(commandline)
			if value:
				return "Error while burning"
			else:
				return "Burning done"
		else:
			return """
			Can't create Commandline:
			self.data must be a string. But it is not a string.
			"""

class databurner(burner):
	mode="data"

class audioburner(burner):
	mode="audio"

class dvdrwburner(burner):
	mode="dvdrw"

class vcdburner(burner):
	mode="vcd"
