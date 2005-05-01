#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Description:	GUI for CD Burning
Version:	0.1
Copyright:	2005 by Thomas Flaig t.gf@freenet.de
Created:	24.Feb.2005
Last modified:	06.Mar.2005
License:        BSD
Requirements:   burncd, wxpython, wxIDs, wxguiParts, wxburnwidow
"""
import wx
import os
from burncd.burncd import *
from wxIDs import *
from wxguiParts import *


__all__=["burngui"]

class MainFrame(wx.Frame):
	"""
	The main frame of the application ;)
	"""
	mode=0
	fixStatus=0
	speedmode=0
	file=""
	device="/dev/acd0"
	teststatus=0
	typelist=["data", "audio", "dvdrw", "vcd"]
	fix=["fixate","don't fixate"]
	test=["burn","only test burning"]
	
	def __init__(self, parent, ID, title):
		wx.Frame.__init__(self, parent, ID, title,
				wx.DefaultPosition, wx.Size(200, 150))
		self.CreateStatusBar()
		self.SetStatusText(" ")
		
		self.CreateMenuBar()
		
		self.sizer=wx.BoxSizer(wx.VERTICAL)
		
		self.IsoSelector=TextSelector(self.sizer, self,ID_ISOINPUT,self.SetISO,"",
		text="Please enter the path to your ISO-file")
		
		"CD Type selector"
		CreateSelector(self.sizer, self,ID_SELECT_TYPE,self.SetType,
		text="Please select CD-type", choices=self.typelist)
		
		"Fixating Selector:"	
		CreateSelector(self.sizer, self,ID_SELECT_FIX,self.SetFix,
		text="Fixate CD after burning?", choices=self.fix)
		
		"Testselector"
		CreateSelector(self.sizer, self, ID_SELECT_TEST,self.SetTest,
		text="Just testing?",choices=self.test)
		
		#SelectSpeed(self.sizer) to be done
		
		"DeviceSelector"
		TextSelector(self.sizer,self,ID_DEVICECH,self.SetDevice,self.device,text="Please enter CD-Device to use")
		
		
		CreateConfirm(self.sizer, self, text="&Burn")
		
		self.SetSizer(self.sizer)
		self.SetAutoLayout(1)
		self.sizer.Fit(self)
		self.Show(1)
	
	def CreateMenuBar(self):
		"""
		Seperate this ?!
		"""
		filemenu = wx.Menu()
		filemenu.Append(ID_OPEN,"&Load file","Load file to burn")
		filemenu.Append(ID_ADD,"&Add file","Add file to selection")
		filemenu.AppendSeparator()
		filemenu.Append(ID_EXIT, "E&xit", "Terminate the program")
		
		helpmenu=wx.Menu()
		helpmenu.Append(ID_HELP, "&Help","Help for this Programm")
		
		helpmenu.AppendSeparator()
		helpmenu.Append(ID_ABOUT, "&About","About this Programm")
		
		
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		menuBar.Append(helpmenu,"&Help")
		self.SetMenuBar(menuBar)
		
		wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)
		wx.EVT_MENU(self, ID_EXIT,  self.OnExit)
		wx.EVT_MENU(self, ID_OPEN, self.OnLoad)
		wx.EVT_MENU(self,ID_ADD, self.OnAdd)
		wx.EVT_MENU(self, ID_HELP, self.OnHelp)
	
	def OnAbout(self, event):
		diag = wx.MessageDialog(self, """
				This program was written by
				Thomas Flaig, t.gf@freenet.de
				and is licensed under the BSD-License.
				""",
				"About burncdGUI", wx.OK | wx.ICON_INFORMATION)
		diag.ShowModal()
		diag.Destroy()
	
	def OnHelp(self, event):
		diag = wx.MessageDialog(self, """
				Select file to burn, burn mode, if we fixate and at last the device
				""",
				"Help?", wx.OK | wx.ICON_INFORMATION)
		diag.ShowModal()
		diag.Destroy()
	
	
	def OnExit(self, event):
		self.Close(wx.true)
		
	def OnLoad(self,event):
		diag = wx.FileDialog(self, "Choose a file", "", "", "", wx.OPEN)
		if diag.ShowModal() == wx.ID_OK:
			filename=diag.GetFilename()
			dirname=diag.GetDirectory()
			self.file=os.path.join(dirname,filename)
			self.SetStatusText(self.file)
			self.IsoSelector.vartext.SetValue(self.file)
		
		diag.Destroy()
		
	def OnAdd(self,event):
		diag = wx.FileDialog(self, "Choose a file", "", "", "", wx.OPEN)
		if diag.ShowModal() == wx.ID_OK:
			filename=diag.GetFilename()
			dirname=diag.GetDirectory()
			self.file+=" "+os.path.join(dirname,filename)
			self.SetStatusText(self.file)
			self.IsoSelector.vartext.SetValue(self.file)
		
		diag.Destroy()
	
	def SetISO(self,event):
		self.file=event.GetString()
		self.SetStatusText(self.file)
	
	def SetTest(self,event):
		self.teststatus=event.GetInt()
	
	def SetType(self,event):
		self.mode=event.GetInt()
		
	def SetFix(self,event):
		self.fixStatus=event.GetInt()
	
	def SetSpeedmode(self,event):
		self.speedmode=event.GetInt()
	
	def SetDevice(self,event):
		self.device=event.GetString()

	def OnConfirm(self,event):
		if self.preptoburn() :
			self.burn()
		
	def preptoburn(self):
		diag = wx.MessageDialog(self,
			"Settings: "
			+"\n Image: " + self.file
			+"\n CD-Type "+self.typelist[self.mode]
			+"\n Fix: "+self.fix[self.fixStatus]
			+"\n Test:"+self.test[self.teststatus]
			+"\n Device: "+self.device
			#+"\n speedmode "+self.speedmodes[self.speedmode]
			,"Confirm",
			 wx.OK| wx.CANCEL| wx.ICON_INFORMATION)
		if diag.ShowModal()==wx.ID_OK:
			diag.Destroy()
			type=self.typelist[self.mode]
			path=self.file
			fix=self.fix[self.fixStatus]
			test=self.test[self.teststatus]
			try:
				if type == "data":
					self.burnobj=databurner(path)
				elif type=="audio":
					self.burnobj=audioburner(path)
				elif type=="dvdrw":
					self.burnobj=dvdrwburner(path)
				elif type=="vcd":
					self.burnobj=vcdburner(path)
				else:
					print "Type unknown"
					print type
			except NoSuchFileException:
				diag2 = wx.MessageDialog(self,
				"""
				A file you like to burn does not exist
				"""
				,"Error",wx.OK | wx.ICON_INFORMATION)
				diag2.ShowModal()
				diag2.Destroy()
				diag.Destroy()
				return False
			if fix=="fixate":
				self.burnobj.change_fixate(1)
			elif fix=="don't fixate":
				self.burnobj.change_fixate(0)
			else:
				print "Unkown command for fixate:"
				print fix
				diag.Destroy()
				return False
			if test !="burn":
				self.burnobj.change_test(1)
			self.burnobj.change_cddevice(self.device)
			diag.Destroy()
			return True
		diag.Destroy()
		return False
		
	def burn(self):
		"""
		result=self.burnobj.burn()
		
		ProgressWindow(self,result[1])
		result[0].close()
		result[1].close()
		"""
		command=self.burnobj.getCommandline()
		progwin=ProgressWindow2(self,command)
		progwin.run()

class burngui(wx.App):
	def OnInit(self):
		frame = MainFrame(wx.NULL, -1, "BurncdGUI")
		frame.Show(wx.true)
		self.SetTopWindow(frame)
		self.MainLoop()
		return wx.true	

if __name__=="__main__":
	burngui()
