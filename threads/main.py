import time
import threading
import wx

thread_list = []

class RefreshThread(threading.Thread):
	def __init__(self, window, activity):
		threading.Thread.__init__(self)
		self.window = window
		self.activity = activity
		self.start()

	def run(self):
		current_task = None
		while True:
			in_progress_task = self.activity.get_in_progress_task()
			if in_progress_task != current_task:
				current_task = in_progress_task
				wx.CallAfter(self.window.panel.refresh_pomodoro_activity)
			time.sleep(0.5)

class RunThread(threading.Thread):
	def __init__(self, activity):
		threading.Thread.__init__(self)
		self.activity = activity
		self.start()

	def run(self):
		self.activity.run()

def stop_all_threads():
	for current_thread in thread_list:
		if current_thread.isAlive():
			current_thread._Thread__stop()

