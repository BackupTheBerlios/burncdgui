#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Description:	GUI Elements
Version:	0.1
Copyright:	2005 by Thomas Flaig t.gf@freenet.de
Created:	06.Mar.2005
Last modified:	06.Mar.2005
License:        BSD
Requirements:   wxpython, wxIDs
"""
import wx
from wxIDs import *

class CreateConfirm(object):
	def __init__(self,sizer, frame,text="&ok"):
		self.ConfirmBox=wx.BoxSizer(wx.HORIZONTAL)
		
		self.BurnButton=wx.Button(frame, ID_BURNBUTTON, text)
		self.ExitButton=wx.Button(frame, ID_EXITBUTTON, "E&xit")
		
		self.ConfirmBox.Add(self.BurnButton,1,wx.EXPAND)
		self.ConfirmBox.Add(self.ExitButton,1,wx.EXPAND)
		
		sizer.Add(self.ConfirmBox,0,wx.EXPAND)
		
		wx.EVT_BUTTON(frame, ID_BURNBUTTON,frame.OnConfirm)
		wx.EVT_BUTTON(frame, ID_EXITBUTTON,frame.OnExit)

class TextSelector(object):
	def __init__(self, sizer, frame, EVENTID,EVENTHANDLER, var,
		text="Enter your choice"):
		self.Box=wx.BoxSizer(wx.HORIZONTAL)
		text=wx.StaticText(frame,-1,text)
		self.vartext=wx.TextCtrl(frame, EVENTID)
		self.Box.Add(text,1,wx.EXPAND)
		self.Box.Add(self.vartext,1,wx.EXPAND)
		sizer.Add(self.Box,0,wx.EXPAND)
		self.vartext.SetValue(var)
		wx.EVT_TEXT(frame, EVENTID,EVENTHANDLER)

class CreateSelector(object):
	def __init__(self, sizer, frame, EVENTID,EVENTHANDLER, 
		text="Make your choice", choices=["yes","no"]):
		self.select=wx.RadioBox(frame, EVENTID, text, wx.Point(-1,-1),
		wx.DefaultSize,	choices, 2, wx.RA_SPECIFY_COLS)
		sizer.Add(self.select,0,wx.EXPAND)
		
		wx.EVT_RADIOBOX(frame, EVENTID, EVENTHANDLER)
	
