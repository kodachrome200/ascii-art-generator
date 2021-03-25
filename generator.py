### ASCII Art Image Generator ###

# This module contains the class for the ASCII art generator proper. The class
# contains the functions to take an image at a specified path, convert it
# to an ASCII image, and save it as a text file at a specified path.
# The functions in this module can be called by an external file (such as the
# interface file, interface.py, or when run alone the user will receive a 
# prompt in the command shell for the input and output file paths.

from os import startfile

import numpy as np
import cv2

from tkinter import messagebox

class AsciiGenerator():
	"""Class that contains all of the properties and functions of the ASCII
	image generator."""

	def __init__(self, shell=False):
		"""Initialize the ASCII generator. If shell=True, running from
		a shell; display errors in shell and not as messageboxes."""

		self.shell = shell

	def convert_to_ascii(self, imageFile, textFile, scale=1):
		"""Given an image path inputFile and text file path outputFile,
		generates an ASCII image to outputFile at the provided scale."""

		### Begin process of converting the image to an ASCII text file. ###
		# While loop while break if an exception occurs.
		while True:
			# Convert scale from string and check if valid integer
			intScale = self._convert_scale(scale)
			if not intScale:
				self._show_scale_errorbox()
				break

			# Get import image
			img = self._get_image_array(imageFile)
			if img is None:
				self._show_input_error_messagebox()

			# Convert image to array of ascii characters and check if good
			asc = self._get_ascii_array(img, intScale)
			if asc is None:
				self._show_input_error_messagebox()
				break

			# Save ascii array as text file and check if save successful. Open
			# if successful.
			saved = self._save_ascii_file(asc, textFile)
			if saved:
				startfile(rf'{textFile}')
			else:
				self._show_output_error_messagebox()
				break

			break


	def _get_image_array(self, imageFile):
		"""Attempts to create a numpy array of shading data from imageFile.
		If unsuccessful, returns an empty object."""
		try:	
			img = cv2.imread(imageFile, 0)
		except:
			return None

		return img


	def _get_ascii_array(self, image, scale):
		"""Given a numpy array representing greyscale pixel values, returns an
		array of ascii characters to generate a corresponding ascii image.
		Scale determines how many linear pixels are represented by an 
		ascii character."""
		
		# Initialize dimensions for working with the image and ascii array,
		# and initialize an empty ascii array.
		img = image
		sc_x = scale
		sc_y = int(scale//1.3) # sc_y must be different - chars are not square
		img_x = len(img) - 1
		img_y = len(img[0]) - 1
		asc_x = img_x//sc_x
		asc_y = img_y//sc_y
		asc = np.empty(shape=(asc_x+1, asc_y+1), dtype='object')

		# Loop through the indices of the ascii array. For each index,
		# grab a sc_x*sc_y section of the image and get its average shade value. 
		# Use this value to determine the ascii character for that section.
		i = 0
		while i <= asc_x: #Loop through columns of image
			i_start = sc_x*i # Get column coordinates of image section
			i_end = sc_x*(i+1)
			j = 0
			while j <= asc_y: #Loop through rows of image
				j_start = sc_y*j # Get row coordinates of image section
				j_end = sc_y*(j+1)
				img_slice = img[i_start:i_end, j_start:j_end] # Get img seciton
				shading = self._get_average_shading(img_slice, sc_x*sc_y)
				char = self._get_ascii_character(shading)
				asc[i,j] = char
				j += 1
			i += 1

		return asc


	def _get_average_shading(self, array, scale):
		"""Given a 2D array of pixel greyscale values, returns the average 
		greyscale value for all pixels. Requires a scale (pixel count in the
		array) to determine average shading."""

		return(array.sum() // scale)


	def _get_ascii_character(self, value):
		"""Given an input greyscale value, returns a corresponding ascii
		character."""

		if value < 50:
			return "M"
		elif value < 75:
			return "N"
		elif value < 100:
			return "N"
		elif value < 125:
			return "?"
		elif value < 150:
			return "7"
		elif value < 175:
			return "+"
		elif value < 200:
			return "="
		elif value < 225:
			return ","
		elif value < 240:
			return "."
		else:
			return " "


	def _save_ascii_file(self, asciiArray, textFile):
		"""Outputs the array asciiArray to a text file at the path textFile."""

		# Initialize array variable and get size attributes
		asc = asciiArray
		asc_x, asc_y = asc.shape

		# Output to text file, display a messagebox if an exception occurs.
		try:
			outputFile = open(textFile, 'wt')
			i = 0
			while i < asc_x:
				j = 0
				while j < asc_y:
					outputFile.write(asc[i,j])
					j += 1
				outputFile.write('\n')
				i += 1
			outputFile.close
			return True
		except:
			return False


	def _convert_scale(self, inputScale):
		"""Verifies that the scale is a valid integer and returns the
		integer value."""
		try:
			scale = int(float(inputScale))
		except ValueError:
			return False
		else:
			if scale >= 1:
				return scale
			else:
				return False


	def _show_input_error_messagebox(self):
		"""Display a messagebox in the case of an error with the input
		file path."""

		if self.shell:
			print(
				f"\n"
				f"An error occurred while attempting to import the image file. "
				f"Please verify that the file selected is a valid image and "
				f"that it is not in use."
				)
		else:
			inputFileErrorMsg = messagebox.showerror("Image File Error",
				f"An error occurred while attempting to import the image file. "
				f"Please verify that the file selected is a valid image and "
				f"that it is not in use.")


	def _show_output_error_messagebox(self):
		"""Display a messagebox in the case of an error with the input
		file path."""

		if self.shell:
			print(
				f"\n"
				f"An error occurred while attempting to save the ASCII text "
				f"file. Please ensure that the file path specified is valid "
				f"and that there is not already an existing file with this "
				f"path that is in use."
				)
		else:
			outputFileErrorMsg = messagebox.showerror("Text File Error",
				f"An error occurred while attempting to save the ASCII text "
				f"file. Please ensure that the file path specified is valid "
				f"and that there is not already an existing file with this "
				f"path that is in use.")


	def _show_scale_errorbox(self):
		"""An error box to be displayed if the scale is not a valid integer."""

		if self.shell:
			print(
				f"\n"
				f"Please enter a valid scale greater than or equal to 1 "
				f"before proceeding."
				)
		else:
			scaleErrorMsg = messagebox.showerror("Invalid Scale",
				f"Please enter a valid scale greater than or equal to 1 "
				f"before proceeding.")


def run_shell_generator():
	"""If this module is run on its own, provide a shell interface to convert
	images."""

	print(f"\n~ASCII Art Generator~\n\n"
			f"This program will convert a given image file to ASCII art.\n"
			f"Enter 'q' at any time to quit.")
			
	while True:
		# Get image file path from user
		print("\nPlease start by providing an image file path:")
		imageFile = input()
		if imageFile == 'q':
			break

		# Get text file path from user
		print("\nProvide a path for the text file to be generated:")
		textFile = input()
		if textFile == 'q':
			break

		# Get the scale from user
		print(f"\nFinally, provide a scale for generating the ASCII image. "
				f"A scale of 1/10 denotes that one ASCII character will "
				f"represent 10 pixels:")
		scale = input('1/')
		if scale == 'q':
			break

		# If the user hasn't given up by now, create an AsciiGenerator object
		# and convert:
		ag = AsciiGenerator(shell=True)
		ag.convert_to_ascii(imageFile, textFile, scale)


if __name__ == '__main__':

	run_shell_generator()