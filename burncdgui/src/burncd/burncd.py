#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Description:	Klassen zum Umgang mit burncd
Copyright:	2005 by Thomas Flaig t.gf@freenet.de
Created:	21.Feb.2005
Last modified:	21.Feb.2005
License:        BSD
Requirements:   burncd in /usr/sbin/burncd (as it is used to be for FreeBSD)
"""

from types import StringType
from os import system
from os import popen4

from os.path import isfile

__all__=["databurner","audioburner","dvdrwburner","vcdburner","NoSuchFileException","CharNotAllowedInFilename"]

class burner(object):
	"""
	Masterclass for all CD-Burning stuff
	"""
	device="/dev/acd1"
	mode="data"
	fixate=1
	speed="max"
	command="/usr/sbin/burncd"
	Burn="system"
	test=0
	def __init__(self,data):
		"""
		Raises NoSuchFileException if Files in data don't exist
		"""
		if not(isfiles(data)):
			raise NoSuchFileException
		self.data=data
		
	def change_cddevice(self, name):
		self.device=name
	def change_mode(self,mode):
		self.mode=mode
	def change_fixate(self, int):
		self.fixate=int
	def change_speed(self, speed):
		self.speed=speed
	def change_test(self,int):
		self.test=int
	
	def makeCommandline(self):
		if isinstance(self.data, StringType):
			self.commandline=self.command 
			if self.test:
				self.commandline+=" -t "
			self.commandline+=" -f " + self.device 
			self.commandline+= " -s " +self.speed
			self.commandline+= " " + self.mode + " " + self.data
			if self.fixate:
				self.commandline+= " " + " fixate "
		else:
			self.commandline="/bin/echo 'No commandline' "
			
	def burn(self):
		self.makeCommandline()
		return popen4(self.commandline)

class databurner(burner):
	"""
	Class for burning data CDs
	"""
	mode="data"

class audioburner(burner):
	"""
	Class for burning audio CDs
	"""
	mode="audio"

class dvdrwburner(burner):
	"""
	Class for burning DVD+
	"""
	mode="dvdrw"

class vcdburner(burner):
	"""
	Class for burning VCDs
	"""
	mode="vcd"

def isfiles(strng):
	for i in strng.split():
		if not(isfile(i)):
			return False
	return True

class NoSuchFileException(Exception): 
	pass

class CharNotAllowedInFilename(Exception):
	pass

if __name__=="__main__":
	try:
		burner("/etc/fstab")
	except NoSuchFileException:
		print "Has your *nix no /etc/fstab?"
	else:
		print "You have a /etc/fstab"
	try:
		burner("/")
	except NoSuchFileException:
		print "All right, / is not a file"
	else:
		print "Why is / a file?"
