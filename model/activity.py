
import time
import os

from task import *

class Activity:
	# constructor
	
	def __init__(self, task_count = 0, serial_id = 1):
		self._task_list = list()
		self.set_serial_id(serial_id)
		self.set_task_count(task_count)
		self.set_task_list()
		self.set_in_progress_task(None)
				
	# methods
	def set_task_count(self, task_count):
		self._task_count = task_count
	
	def set_task_list(self):
		self._task_list = []
		if self._task_count != 0:
			i = 1
			count = self.get_task_count()
			while i <= count:
				# add 25 min. work task
				work_task = Task("You have 25 min to work", 25)
				work_task.set_task_type('work')
				self.add_task(work_task)
				# add break
				if i < count:
					if i % 4 == 0:
						break_task = Task("Take a 30 min break", 30)
						work_task.set_task_type('break')
						self.add_task(break_task)
					else:
						break_task = Task("Take a 5 min break", 5)
						work_task.set_task_type('break')
						self.add_task(break_task)
				i = i + 1

	def set_in_progress_task(self, task):
		self._in_progress_task = task

	def set_serial_id(self, serial_id):
		self._serial_id = serial_id

	def get_serial_id(self):
		return self._serial_id


	def get_task_count(self):
		return self._task_count

	def get_task_list(self):
		return self._task_list

	def get_in_progress_task(self):
		return self._in_progress_task

	def add_task(self, task):
		self._task_list.append(task)

	def clear_task_list(self):
		self.task_list

	def clear_task_status(self):
		for task in self.get_task_list():
			task.set_status('')

	def run(self):
		if self.get_in_progress_task() == None:

			app_dir = str(os.path.abspath("."))
			self.clear_task_status()
			
			for task in self.get_task_list():
				self.set_in_progress_task(task)
				task.set_status("In progress") 

				cmd_str = 'notify-send -t 1000 -i ' + app_dir  + '/appereance/pomodoro.png "New Pomodoro starts" "'+ task.get_name() + '"'
								
				if task.get_task_type == 'break':
					os.system('aplay ' + app_dir  + '/appereance/notify.wav')
				else:
					os.system('aplay ' + app_dir  + '/appereance/notify.wav')
					os.system(cmd_str)
				
				time.sleep(task.get_duration()) # sleep
				task.set_status("Done")
				
			self.set_in_progress_task(None)
			cmd_str = 'notify-send -t 1000 -i ' + app_dir  + '/appereance/pomodoro.png "Congratulation" "Your work finished." '
			os.system('aplay ' + app_dir  + '/appereance/notify.wav')
			os.system(cmd_str)

		else:
			cmd_str = 'notify-send -t 1000 -i ' + app_dir  + '/appereance/pomodoro.png "Sorry" "Your pomodoro is in progress." '
			os.system('aplay ' + app_dir  + '/appereance/notify.wav')
			os.system(cmd_str)
			
