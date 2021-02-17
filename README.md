
mario 
=====
mario is a Python package for reading and writing mar345 images
The program is written in python (>=3). For file I/O, C-routines are used.
	
Changelog
=========

Version	Date		Changes
1.0	15/02/2021	Original version


Installation
============
mario can be obtained from github as:
	git clone https://github.com/marxperts/mario

After cloning, install it:

	cd mario

	python setup.py install

Most likely you will need to do this with root privileges (e.g. put sudo in front of the command).
If you are using MS Windows you also download a binary version packaged as executable installation files. 
Depending on your python version open either

	mario-1.0.0.win64-py3.7.exe

Dependencies
============
Python 3.0 or later. 
The program also makes use of:

* numpy
* cffi

Ubuntu and Debian Like linux distributions:
-------------------------------------------
To use mario on Ubuntu (a linux distribution based on Debian) the needed python modules can be installed either through the Synaptic Package Manager (found in System -> Administration) or using apt-get on from the command line in a terminal.
The extra ubuntu packages needed are:

* python3-numpy
* python3-cffi

using apt-get these can be installed as:

sudo apt-get install python3-numpy  python3-cffi

Usage:
------

1) Import the mar345 module from the mario package:

	from mario import mar345

   Module mar345 features a single class "Mar345" that can be used for both
   reading and writing mar345 formatted images, depending on class arguments.

2) For each file to be read, use a filename (name=...) with class Mar345 

	img = mar345.Mar345(name=input_file)

   "img" contains the following elements:
	img.x & img.y:	x,y dimensions of the data array
	img.name:	filename
	img.data:	32-bit integer numpy array  with x*y pixels (1D)
	img.header:	dictionary with header information
    	img.raw_header:	first 4k bytes of image with all header information

   Note, that the mar345 image format uses a 16-bit data array. Pixels
   exceeding 16-bits are stored with their address and intensity in between
   the header (4k) and the start of the 16-bit  array. When using the module,
   you will get the data back as full 32-bit array, so you don't have to care.

   See example/rw345.py for a more sophisticated test case that reads in 2 
   images, adds them up, applies a scale factor and writes out a combined image.

3) To write out the image, pass filename (name=...), 
   data array (data=...) and 4k raw image header (header=)  to  the class
   constructor. 

	mar345.Mar345( name=outputfile, data=img.data, header=img.raw_header )

   For writing, it is also possible to initialize the class stand-alone without
   filename and fill in the required information for headers and data step by
   step. See example/w345.py for more details.


