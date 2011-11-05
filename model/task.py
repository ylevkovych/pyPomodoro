class Task:
	
	#Constractor

	def __init__(self, name, duration):
		self.set_name(name)
		self.set_duration(duration)
		self.set_task_type('')
		self.set_status('')

	# Methods
	
	def set_name(self, name):
		self._name = name

	def set_duration(self, duration):
		self._duration = duration

	def set_task_type(self, task_type):
		self._task_type = task_type

	def set_status(self, status):
		self._status = status
		
	def get_name(self):
		return self._name

	def get_duration(self):
		return self._duration

	def get_task_type(self):
		return self._task_type
		
	def get_status(self):
		status = self._status
		if status == None:
			status = ''
		return status
