#!/bin/python3.2

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
#import pygtk2
from gi.repository import Gtk

class Gui:

	def delete(self, widget, event=None):
		Gtk.main_quit()
		return False			

	def __init__(self, source):
		window = Gtk.Window()
		window.connect("delete_event", self.delete)
		#window.set_border_width(10)

		table = Gtk.Table(3, 6, False)
		window.add(table)

		window.set_title("GemRB Config")
		window.set_border_width(0)
		window.set_size_request(300, 300)

		# Create a new notebook, place the tabs
		notebook = Gtk.Notebook()
		notebook.set_tab_pos(Gtk.PositionType.LEFT)
		table.attach(notebook, 0, 6, 0, 1)
		notebook.show()

		self.show_tabs = True
		self.show_border = True	
	
		for i in source.sections:		
			vbox = Gtk.VBox()
			vbox.set_border_width(0)
			vbox.set_size_request(100, 100)
			vbox.show()    

			scrolled_window = Gtk.ScrolledWindow()
			scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.ALWAYS)

			scrolled_window.show()
			vbox.pack_start(scrolled_window, True, True, padding = 0)

			table1 = Gtk.Table(i.options.__len__(), 1, False)
			scrolled_window.add_with_viewport(table1)
			table1.show()
			
			for j, k in enumerate(i.options):
				button = Gtk.ToggleButton(k.name)
				table1.attach(button, 1, 2, j, j+1)
				button.show()

			label = Gtk.Label(i.name)
			notebook.append_page(vbox, label)


		notebook.set_current_page(0)

		table.show()
		window.show()

class Source:

	def __init__(self, fname):
		self.section_start = []
		self.sections = []

		if not os.path.exists(fname):
			print('Invalid Source File.')
			os._exit(1)

		self.filename = fname
		self.buff  = [line.strip() for line in open(fname, 'r')]

		for i, string in enumerate(self.buff):
			if string.find('#@') == 0:
				self.section_start.append(i)
		
		for i, item in enumerate(self.section_start):
			if item == self.section_start[-1]:
				self.sections.append(Section(self.buff[item:self.buff.__len__()]))
			else:
				self.sections.append(Section(self.buff[item:self.section_start[i+1] - 1]))

class Section:

	def __init__(self, buff):	
		self.description = []
		self.option_start = []
		self.options = []

		self.name = buff[0].lstrip('#@ ')
		
		if buff.__len__() == 1: return

		for i, string in enumerate(buff):
			
			if string.find('#+') == 0:
				self.option_start.append(i)
		
		for i, string in enumerate(buff[1:self.option_start[0]]):
			if not string: continue
			if string[0] == '#': self.description.append(string.lstrip('# '))
		
		for i, item in enumerate(self.option_start):
			if item == self.option_start[-1]:
				self.options.append(Option(buff[item:buff.__len__()]))
			else:
				self.options.append(Option(buff[item:self.option_start[i+1] - 1]))
	
	def print(self):
		print('\n' + self.name)
		print('\n'.join(self.description))
		print(self.option_start)
		for i in self.options:
			i.print()			

class Option:

	def __init__(self, buff):
		self.description = []
		self.choices = []

		self.name = buff[0].lstrip('#+ ')

		self.words = buff[1].split()
		
		self.option_string = self.words[1]
		self.type = self.words[2]

		if self.type == 'Boolean':
			self.choices = [0, 1]
		else:
			if self.type == 'Radiobutton':
				self.choices = self.words[3:self.words.__len__()]

		for i, string in enumerate(buff[2:(buff.__len__()-1)]):
			if not string: continue
			if string[0] == '#': self.description.append(string.lstrip('# '))

		self.default_value = buff[-1].split('=',1)[-1]

	def print(self):
		print('\n' + self.name)
		print('\n'.join(self.description))
		print(self.type)
		print(self.choices)
		print(self.default_value)

def main():
	Gtk.main()
	return 0

a = Source('./GemRB.cfg.skel')

for i in a.sections:
	i.print()

if __name__ == "__main__":
	Gui(a)
	main()
