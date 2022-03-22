#-*- coding:utf-8 -*-

"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
import numpy as np

class RSVP_plugin(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'Add an RSVP to your experiment'

	def reset(self):

		"""
		desc:
			Resets plug-in to initial values.
		"""

		# targets and distractors are read from the text file that needs to be inside the file pool before the plugin is used in OS, plugin reads both lists of targets and distractors separated by space and uses them to correctly assign images from the file pool, it also keeps count of number of targets/distractors and shows it
		self.var._ntargets = 0
		self.var._ndistractors = 0
		with open(self.experiment.pool[u'targets.txt']) as f:
    			target_list = f.read()
		target_split = target_list.split('\n')
		for i in target_split:
			if i:
				self.var._ntargets += 1
				
		self.var._targets = target_list
		
		with open(self.experiment.pool[u'distractors.txt']) as f:
    			distractor_list = f.read()
		distractor_split = distractor_list.split('\n')
		for i in distractor_split:
			if i:
				self.var._ndistractors += 1
		
		self.var._distractors = distractor_list
		self.var._target_positions = u'1;3'
		self.var._stimdur = 300
		self.var._fixdur = 1000
		self.var._tar_option = u''
		self.var._dis_option = u''
		# self.var._event_handler = u'print(10)'

	def prepare(self):

		# Call the parent constructor.
		item.prepare(self)

		self.cnvs_stream = {} # creates the stream of canvases as a dictionary
		
		if u'Images' in self.var._tar_option and u'Images' in self.var._dis_option:
			target_positions = [int(x) - 1 for x in self.var._target_positions.split(';')]
			targets = self.var._targets.split('\n')
			distractors = self.var._distractors.split('\n')
			for i in range(self.var._ndistractors + self.var._ntargets):
				if i in target_positions:
					t = targets.pop(0)
					self.cnvs_stream[str(i)] = canvas(self.experiment) 
					self.cnvs_stream[str(i)].image(self.experiment.pool[t]) 
					self.var.set('stim_%d' % i, t)
				else:
					d = distractors.pop(0)
					self.cnvs_stream[str(i)] = canvas(self.experiment)
					self.cnvs_stream[str(i)].image(self.experiment.pool[d])
					self.var.set('stim_%d' % i, d)
	
		else:
			target_positions = [int(x) - 1 for x in self.var._target_positions.split(';')]
			targets = self.var._targets.split(';')
			distractors = self.var._distractors.split(';')
			for i in range(self.var._ndistractors + self.var._ntargets):
				if i in target_positions:
					t = targets.pop(0)
					self.cnvs_stream[str(i)] = canvas(self.experiment)
					self.cnvs_stream[str(i)].text(
					"<span style='color:rgba(0,0,0,.01)'>gb</span>{}<span style='color:rgba(0,0,0,.01)'>gb</span>".format(t),font_size=48,color=u'rgb(190,190,190)',x=0,y=0)
					self.var.set('stim_%d' % i, t)
				else:
					d = distractors.pop(0)
					self.cnvs_stream[str(i)] = canvas(self.experiment)
					self.cnvs_stream[str(i)].text(
					"<span style='color:rgba(0,0,0,.01)'>gb</span>{}<span style='color:rgba(0,0,0,.01)'>gb</span>".format(d),font_size=48,color=u'rgb(190,190,190)',x=0,y=0)
					self.var.set('stim_%d' % i, d)
					
	
		# create fixation canvas	
		self.cnvs_fix = canvas(self.experiment)
		self.cnvs_fix.fixdot()

		# # Byte-compile the event handling code (if any)
		# event_handler = self.var.get('_event_handler', _eval=False)
		# if event_handler:
		# 	custom_event_handler = self.python_workspace._compile(
		# 		event_handler
		# 	)
		# else:
		# 	custom_event_handler = None

	def run(self):

		#fixation dot
		self.set_item_onset(self.cnvs_fix.show())
		# self.var.fix_onset = clock.time()
		self.sleep(self.var._fixdur)
		# prev = 0

		for i in range(self.var._ndistractors + self.var._ntargets):
			t = self.cnvs_stream[str(i)].show()
			# print(t - prev)
			# prev = t

			self.sleep(self.var._stimdur)


class qtRSVP_plugin(RSVP_plugin, qtautoplugin):

	"""
	This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
	usually need to do hardly anything, because the GUI is defined in info.json.
	"""

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.

		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.

		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		# We don't need to do anything here, except call the parent
		# constructors.
		RSVP_plugin.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)
