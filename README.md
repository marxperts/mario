
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
mario can be downloaded as distribution file from the https://marxperts.com/pub/mario-1.0.0.tgz

To install, unpack the compressed distribution file first, e.g. 
	tar xvzf mario-1.0.0.tgz

All files are unpacked into the directory mario-1.0.0. To install these do:

	cd mario-1.0.0

and install mario with:

	python3 setup.py install

Most likely you will need to do this with root privileges (e.g. put sudo in front of the command).
If you are using MS Windows you also download a binary version packaged as executable installation files. 
Depending on your python version open either

	mario-1.0.0.win64-py3.7.exe

Dependencies
============
Python 3.5 or later. 
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

2) For each file to be read, initialize Mar345 class and read data in:

	mar345a = mar345.Mar345()
	img = mar345a.read(filename)

   "img" contains the following elements:
	img.x & img.y:	x,y dimensions of the data array
	img.data:	32-bit integer numpy array  with x*y pixels (1D)
	img.header:	dictionary with header information
    	img.raw_header:	first 4k bytes of image with all header information

   Note, that the mar345 image stores the image data in a 16-bit array. Pixels
   exceeding 16-bits are stored with their address and intensity in between
   the header (4k) and the start of the 16-bit  array. When using the module,
   you will get the data back as full 32-bit array, so you don't have to care.

3) To write out the image, use:
	img.write( filename, img.data, img.raw_header )

For more details, see rw345.py and w345.py in the examples directory.

