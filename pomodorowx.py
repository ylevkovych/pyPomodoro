#!/usr/bin/python

import threads.main as threads
import ui.main as main_frame

if __name__ != '__main__':
	print("Can't use from another module.")
else:
	app = main_frame.App()
	app.MainLoop()

	threads.stop_all_threads()
	
	


