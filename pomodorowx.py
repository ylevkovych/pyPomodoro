#!/usr/bin/python

import wx
import sys
import threading
import time
from activity import *

activity = Activity(0)
threads = []

"""
Threads
"""
class RefreshThread(threading.Thread):
	def __init__(self, window):
		threading.Thread.__init__(self)
		self.window = window
		self.start()

	def run(self):
		current_task = None
		while True:
			in_progress_task = activity.get_in_progress_task()
			if in_progress_task != current_task:
				current_task = in_progress_task
				wx.CallAfter(self.window.panel.refresh_pomodoro_activity)
			time.sleep(0.5)

class RunThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.start()

	def run(self):
		wx.CallAfter(activity.run())


"""
UI's

Application UI's: 
    App     - application
    Frame   - main frame
    Panel   - main panel
"""

class App(wx.App):
	def OnInit(self):
		self.frame = mainFrame(None, size = (400, 360), title = "Pomodoro Technique Runner")
		self.frame.Show()
		return True

class mainFrame(wx.Frame):
	def __init__(self, *args, **kwargs):
		super(mainFrame, self).__init__(*args, **kwargs)

		self.size = (40, 200)
		self.title = "Pomodoro Technique"
		
		self.panel = mainPanel(self)
		
		refresh_thread = RefreshThread(window = self)
		
		global threads
		threads.append(refresh_thread)

class mainPanel(wx.Panel):
	def __init__(self, parent):

		super(mainPanel, self).__init__(parent)

		# UI components
		
		self.lbl_pomodoros_count = wx.StaticText(self, -1,"Pomodoros Count: ", pos=(10,14))
		self.txt_pomodoros_count = wx.TextCtrl(self, -1,"", (150,10))
		self.btn_pomodos_count = wx.Button(self, -1,"Count", (250,10))
		self.lbl_summary = wx.StaticText(self, -1,"", (10,30))
		self.lbl_pomodoros_count1 = wx.StaticText(self, -1,"Pomodoro activity: ", (10,60))
		self.activity_list = wx.ListCtrl(self, -1, style=wx.LC_REPORT, pos=(10,90), size=(380, 220))
		self.activity_list.InsertColumn(0, 'Description', width=200)
		self.activity_list.InsertColumn(1, 'Duration', width=80)
		self.activity_list.InsertColumn(2, 'Status', width=100)
		self.btn_pomodoro_play = wx.Button(self, -1,"Play", (10,317))
		self.btn_pomodoro_pause = wx.Button(self, -1,"Pause", (100,317))
		self.btn_pomodoro_stop = wx.Button(self, -1,"Stop", (200,317))
		
		# events
		
		self.Bind(wx.EVT_BUTTON, self.btn_pomodos_count_on_click, self.btn_pomodos_count)
		self.Bind(wx.EVT_BUTTON, self.btn_pomodo_play_on_click, self.btn_pomodoro_play)
		self.Bind(wx.EVT_BUTTON, self.btn_pomodoro_stop_on_click, self.btn_pomodoro_stop)

	def btn_pomodos_count_on_click(self, event):
		pomodoros_count = self.txt_pomodoros_count.GetValue()
		
		try:
			pomodoros_count = int(pomodoros_count)
		except:
			pomodoros_count = 0
			
		if pomodoros_count != activity.get_task_count() and activity.get_in_progress_task() == None :
			global activity
			activity.set_task_count(pomodoros_count)
			activity.set_task_list()
			self.refresh_pomodoro_activity()
			
	def btn_pomodo_play_on_click(self, event):
		run_thread = RunThread()

		global threads
		threads.append(run_thread)
				
	def btn_pomodoro_stop_on_click(self, event):
		global threads
		for thr in threads:
			thr._Thread__stop()


	def run_activity(self):
		activity.run()

	def refresh_pomodoro_activity(self):
		if self.check_difference():
			self.activity_list.DeleteAllItems()
			for task in activity.get_task_list():
				index = self.activity_list.InsertStringItem(sys.maxint , task.get_name())
				self.activity_list.SetStringItem(index, 0, task.get_name())
				self.activity_list.SetStringItem(index, 1, str(task.get_duration()) + ' min.')
				self.activity_list.SetStringItem(index, 2, task.get_status())

	def check_difference(self):
		return True		
					
if __name__ != '__main__':
	print("Can't use from another module.")
else:
	app = App()
	app.MainLoop()

	# global threads
	for current_thread in threads:
		if current_thread.isAlive():
			current_thread._Thread__stop()
		else:
			print('Thread %s is stopped.' % current_thread)


