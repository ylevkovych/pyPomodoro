import wx
import sys
import os


from model import activity as model 
from threads import main as threads

activity = model.Activity(0)

class App(wx.App):
	def OnInit(self):
		self.frame = MainFrame(None, size = (400, 360), title = "Pomodoro Technique Runner")
		self.frame.Show()
		return True
	
class MainFrame(wx.Frame):
	def __init__(self, *args, **kwargs):
		super(MainFrame, self).__init__(*args, **kwargs)
		
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		
		self.size = (40, 200)
				
		self.panel = MainPanel(self)
		
		refresh_thread = threads.RefreshThread(window = self, activity = activity)
		
		threads.thread_list.append(refresh_thread)
		
	def OnClose(self, event):
		dlg = wx.MessageDialog(self,
			"Do you really want to exit this application?",
			"Confirm exit", 
			wx.YES_NO|wx.ICON_QUESTION)
			
		result = dlg.ShowModal()
		dlg.Destroy()
				
		if result == wx.ID_YES:
			threads.stop_all_threads()
			self.Destroy()
		
		
class MainPanel(wx.Panel):
	def __init__(self, parent):

		super(MainPanel, self).__init__(parent)

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
				
		# events
		
		self.eventsHandler = EventsHandler(parent = self)

		self.Bind(wx.EVT_BUTTON, self.eventsHandler.btn_pomodos_count_on_click, self.btn_pomodos_count)
		self.Bind(wx.EVT_BUTTON, self.eventsHandler.btn_pomodo_play_on_click, self.btn_pomodoro_play)
		
	def refresh_pomodoro_activity(self):
		self.activity_list.DeleteAllItems()
		for task in activity.get_task_list():
			index = self.activity_list.InsertStringItem(sys.maxint , task.get_name())
			self.activity_list.SetStringItem(index, 0, task.get_name())
			self.activity_list.SetStringItem(index, 1, str(task.get_duration()) + ' min.')
			self.activity_list.SetStringItem(index, 2, task.get_status())
				

class EventsHandler():

	def __init__(self, parent):
		self.parent = parent

	def btn_pomodos_count_on_click(self, event):
		pomodoros_count = self.parent.txt_pomodoros_count.GetValue()
		
		try:
			pomodoros_count = int(pomodoros_count)
		except:
			pomodoros_count = 0
			
		if pomodoros_count != activity.get_task_count() and activity.get_in_progress_task() == None :
			global activity
			activity.set_task_count(pomodoros_count)
			activity.set_task_list()
			self.parent.refresh_pomodoro_activity()
			
	def btn_pomodo_play_on_click(self, event):
		run_thread = threads.RunThread(activity)

		# global threads
		threads.thread_list.append(run_thread)
						
