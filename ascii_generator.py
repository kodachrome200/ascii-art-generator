### ASCII Art Generator GUI ###

# This file contains all of the GUI functions and objects for the ASCII
# art generator. It will use Tkinter throughout to generate GUI objects.
# The main window and its widgets are initialized in main(), the remainder
# of the GUI functionality is contained in functions below.

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox

from generator import AsciiGenerator

class GeneratorGUI():
	"""Class that contains all properties and functions of the ASCII 
	generator GUI."""

	def __init__(self):
		"""Initialize the root window and objects for the GUI."""

		### Create the root window and set up dimensions ###
		self.root = Tk()
		self.root.title("ASCII Art Generator")
		self.root.geometry('640x320')

		### Create objects for getting the input image file ###
		# Label for file input
		self.lblInput = Label(self.root,
				text=f"Select the image file to be converted to ASCII:")
		self.lblInput.grid(
				column=0, 
				row=0,
				padx=10,
				pady=10,
				sticky='W',
				)

		# Text box for file input path
		self.txtInput = Entry(self.root, width=102)
		self.txtInput.grid(
				column=0, 
				row=1,
				padx=10,
				pady=0,
				sticky='W',
				)

		# Button to open input file dialog
		self.btnInput = Button(self.root, text="Select", width=12,
				command=self._input_file_dialog)
		self.btnInput.grid(
				column=0, 
				row=2,
				padx=10,
				pady=10,
				sticky='E',
				)

		### Create objects for getting the output text file ###
		# Label for file output
		self.lblOutput = Label(self.root,
				text=f"Select the location to save the ASCII image:")
		self.lblOutput.grid(
				column=0, 
				row=3,
				padx=10,
				pady=10,
				sticky='W',
				)

		# Text box for file output path
		self.txtOutput = Entry(self.root, width=102)
		self.txtOutput.grid(
				column=0, 
				row=4,
				padx=10,
				pady=0,
				sticky='W',
				)

		# Button to open output file dialog
		self.btnOutput = Button(self.root, text="Select", width=12,
				command=self._output_file_dialog)
		self.btnOutput.grid(
				column=0, 
				row=5,
				padx=10,
				pady=10,
				sticky='E',
				)

		### Create objects for getting the scale of the ASCII output. ###
		# Label for scale entry textbox
		self.lblScale = Label(self.root,
				text=f"Specify a scale for the output of the ASCII image, "
						f"in horizontal pixels per ASCII character:")
		self.lblScale.grid(
				column=0,
				row=6,
				padx=10,
				pady=10,
				sticky='W',
				)

		# Text box for scale entry
		self.txtScale = Entry(self.root, width=8)
		self.txtScale.grid(
				column=0,
				row=7,
				padx=10,
				pady=0,
				sticky='W',
				)
		self.txtScale.insert(0,'10')

		### Create objects for converting the input image file to the output
		### ASCII text file.
		self.btnConvert = Button(self.root, text="Convert to ASCII", width=15,
			command=self._convert_image)
		self.btnConvert.grid(column=0,
				row=8,
				padx=10,
				pady=20,
				sticky='SE',
				)

		### Initialize lists of allowed input and output file types. ###
		self.inputTypes = self._initialize_input_file_types()
		self.outputTypes = self._initialize_output_file_types()


	def run(self):
		# Execute Tkinter
		self.root.mainloop()


	def _initialize_input_file_types(self):
		"""Creates a list of valid file types for askOpenFile dialogs."""
		
		inputTypes = [
				('All images', '*.bmp;*.jpg;*.jpeg;*.png;*.gif'),
				('Bitmap images', '*.bmp'),
				('JPEG images', '*.jpg;*.jpeg'),
				('PNG images', '*.png'),
				('GIF images', '*.gif'),
				]

		return inputTypes


	def _initialize_output_file_types(self):
		"""Creates a list of valid file types for askSaveAsFile dialogs."""

		outputTypes = [
				('Text files', '*.txt'),
				('All file types', '*.'),
				]

		return outputTypes


	def _input_file_dialog(self):
		"""Opens a tkinter file dialog box and fills the txtInput entry with
		the file path if a file is selected."""

		# Open file dialog
		inputFile = askopenfilename(filetypes=self.inputTypes)
		# If file selected, check if txtInput already has an entry and clear,
		# then insert path of selected file
		if inputFile:
			curTxt = self.txtInput.get()
			if curTxt:
				curTxtEnd = len(curTxt)
				self.txtInput.delete(0, curTxtEnd)
			self.txtInput.insert(0, inputFile)


	def _output_file_dialog(self):
		"""Opens a tkinter file dialog box and fills the txtOutput entry with
		the file path if a file is selected."""

		# Open file dialog
		outputFile = asksaveasfilename(filetypes=self.outputTypes,
				defaultextension=self.outputTypes[0])
		# If file selected, check if txtInput already has an entry and clear,
		# then insert path of selected file
		if outputFile:
			curTxt = self.txtOutput.get()
			if curTxt:
				curTxtEnd = len(curTxt)
				self.txtOutput.delete(0, curTxtEnd)
			self.txtOutput.insert(0, outputFile)


	def _convert_image(self):
		"""Checks to ensure that there is a valid path for both the input
		and output file, then calls the proper module to generate an ASCII
		image."""
		inputFile = self.txtInput.get()
		outputFile = self.txtOutput.get()
		scale = self.txtScale.get()
		ag = AsciiGenerator()
		ag.convert_to_ascii(inputFile, outputFile, scale)


if __name__ == '__main__':
	gen_gui = GeneratorGUI()
	gen_gui.run()