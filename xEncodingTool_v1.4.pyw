#!/usr/bin/python
# -*- coding: utf8 -*-
'''
contact:
bluphy@qq.com
@author: bluphy
Updated on 2017-11-07 v1.4 optimize layout control when resizing window
Updated on 2017-09-06 v1.3 add feature to remember the last used task decode/encode
Updated on 2017-09-02 v1.2 based on Python 3.6
	1.Update the strategy to refresh the output box immediately 
	after the input or change the task encode/decode.
	2.Reorgnized the release infomation part (this section) by latest info on the top
	3.Remove the extra '0A' at the tail when encodeing
Updated on 2013-06-18 v1.1 based on Python 3.3
	1.make output can be selected and copied
	2.when decoding, ignore space characters
	3.multi-line display
Updated on 2012-09-26 v1.0 based on Python 3.2.2 
Created on 2012-09-17

'''

from tkinter import *
from binascii import hexlify
import ctypes,sys,os
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def hex2str(hexbytes):
	tmp=str(hexlify(hexbytes)).upper()
	print(tmp)
	return tmp[2:-1]

def formatHEXstr(hexstr):
	#print(len(hexstr))
	tmp=''
	for i in range(len(hexstr)//2):
		tmp=tmp + ' ' + hexstr[2*i:2*i+2]
	return tmp

def getPath():
	return sys.argv[0]
	
def loadCfg(key):
	path = getPath()
	with open(path,'r') as cfg:
		for line in cfg:
			if '[CONFIG]' in line and key in line:
				value = line.split('=')[1].strip()
#				print('value='+value)
				break
	return value

def saveCfg(key,value):
	'''
	save cfg to current script file, use file.seek method to modify the file by seeking from file end.
	The config item is stored in the end of file. 
	The offset value is counted manually. And if the end of file has changed, the value need to modify.
	'''
	path = getPath()
	with open(path, 'r+b' ) as cfg:
		cfg.seek(-13,os.SEEK_END)
		cfg.write(bytes(value, 'ascii'))
		
	
	
class xEncodingTool(Frame):
	def __init__(self, master=NONE):
		Frame.__init__(self, master)
		#self.rowconfigure(index=0,weight=1)
		self.rowconfigure(index=1,weight=1)
		self.rowconfigure(index=2,weight=1)
		self.columnconfigure(index=3,weight=1)
		self.grid(sticky=N+S+E+W)
		
		self.task=StringVar()
		
		try:
			self.task.set(loadCfg('task'))
			print('task='+self.task.get())
		except:
			self.task.set('decode')
			print('ERROR: set to default')
			
		self.buttonEncode=Radiobutton(self, text='ENCODE',width=9,indicatoron=FALSE,value='encode',variable=self.task,relief=RAISED)
		self.buttonEncode.grid(row=0,rowspan=1,column=0,columnspan=1,sticky=S+E+W)
		self.buttonEncode.bind('<Button-1>',self.encodeHdl)
		
		self.buttonDecode=Radiobutton(self, text='DECODE',width=9,indicatoron=FALSE,value='decode',variable=self.task)
		self.buttonDecode.grid(row=0,rowspan=1,column=1,columnspan=1,sticky=N+E+W)
		self.buttonDecode.bind('<Button-1>',self.decodeHdl)
		
		self.encodingString=StringVar()
		self.encodingString.set('gb18030')
		self.encodingInputLabel=Label(self,text='ENCODING=',anchor=E)
		self.encodingInputLabel.grid(row=0,column=2,sticky=E)
		self.encodingInput=Entry(self,textvariable=self.encodingString)
		self.encodingInput.grid(row=0,column=3,sticky=W+E)
		
		self.inputBox=Text(self)
		#self.inputString=StringVar()
		#self.inputBox=Entry(self,textvariable=self.inputString)
		self.inputBox.bind('<KeyRelease>',self.updateOutputBox)
		self.inputBox.grid(row=1,rowspan=1,column=0,columnspan=4,sticky=N+S+E+W)
			 
		self.outputBox=Text(self,bg='grey')
		#self.output=StringVar()
		#self.outputBox=Label(self, textvariable=self.output, anchor=W, wraplength=330)
		self.outputBox.grid(row=2,rowspan=1,column=0,columnspan=4,sticky=N+S+E+W)
		
		self.encodingInput.bind('<KeyPress-Return>',self.updateOutputBox)
	
	def encodeHdl(self,event):
		self.task.set('encode')
		self.updateOutputBox(event)
		saveCfg('task','encode')
		
	def decodeHdl(self,event):
		self.task.set('decode')
		self.updateOutputBox(event)
		saveCfg('task','decode')
	
	def updateOutputBox(self,event):

		try:
			self.outputBox.delete("1.0",END)
			#if self.master.task.get()=='encode':
			#self.output.set(formatHEXstr(hex2str(self.inputBox.get("1.0",END).encode(self.encodingString.get()))))
			if self.task.get()=='encode':
				print('encode')
				#self.output.set(formatHEXstr(hex2str(self.inputString.get().encode(self.encodingString.get()))))
				self.outputBox.insert("1.0",formatHEXstr(hex2str(self.inputBox.get("1.0",END).encode(self.encodingString.get()))[:-2]))

			else:
				print('decode')
				#self.output.set(bytearray.fromhex(''.join(self.inputString.get().split())).decode(self.encodingString.get()))
				
				temp=''.join(self.inputBox.get("1.0",END).split())
				temp=''.join(temp.split(sep=' '))
				self.outputBox.insert("1.0",bytearray.fromhex(temp).decode(self.encodingString.get()))
		except ValueError:
			self.outputBox.insert(END,"Error!")
	  
		
if __name__ == '__main__':
	root=Tk()
	root.columnconfigure(0, weight=1)
	root.rowconfigure(0, weight=1)
	root.geometry('+'+str(screensize[0]//2-165)+'+'+str(screensize[1]//2-300))
	#root.geometry('400x600+700+400')
	app=xEncodingTool(master=root)
	app.master.title("xEncodingTool")
	app.mainloop()
	
	
'''
DO NOT EDIT THIS PART MANUALLY!!
DO NOT ADD ANY CHARACTER INCLUDING WHITESPACE IN THE END!!
[CONFIG]task=decode
'''
