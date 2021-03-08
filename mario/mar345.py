#!/usr/bin/env python3
"""
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Module:		    mar345
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Description:	Class definition for mar345 images
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Author:		    Claudio Klein
                marXperts GmbH
                Werkstr.3
                22844 Norderstedt / Germany
                Claudio.Klein@marxperts.com
                www.marxperts.com
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
History:
Version         Date        Description
1.0.1           08/03/2021  readheader: fix self.y = int(... )
1.0             23/01/2020  Original version
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""
import os, sys, array, time, datetime, re, math
import numpy as np
path = os.path.dirname(__file__)
sys.path.append(path)
from   mario._libmar345  import lib, ffi

# Dict for mar345 header
h345 = {
	# General
	'program'	:	'xxx',
	'version'	:	'x.x',
	'serial'	:	0,
	'date'		:	'',
	'extra'	    :	'',
	'swap'	    :	0,
	'remark'	:	[''],

	# Detector specific
	'detector'	:	'mar345',
	'x'		    :	0,
	'y'		    :	0,
	'pixels'	:	0,
	'high'		:	0,
	'adc'		:	[0,0],
	'adc_add'	:	[0,0],
	'gaps'		:	[0,0,0,0,0,0,0,0],
	'pixelsize'	:	[0.15, 0.15],
	'center'	:	[0.0, 0.0],
	'roff'		:	0.0,
	'toff'		:	0.0,
	'gain'		:	0.0,
	'multiplier':	0.0,

	# Experimental conditions
	'type'		:	'TIME',		# 0=dose, 1=time
	'time'		:	0.0,
	'dose_n'	:	0,
	'dosebeg'	:	0.0,
	'doseend'	:	0.0,
	'dosemin'	:	0.0,
	'dosemax'	:	0.0,
	'doseavg'	:	0.0,
	'dosesig'	:	0.0,
	'wavelength':	1.541789,
	'distance'	:	100.0,
	'resolution':	0.0,
	'phibeg'	:	0.0,
	'phiend'	:	0.0,
	'phiosc'	:	1,
	'omebeg'	:	0.0,
	'omeend'	:	0.0,
	'omeosc'	:	0,
	'theta'		:	0.0,
	'chi'		:	0.0,

	# Generator
	'source'	:	'Rotating_anode',
	'kV'		:	50.0,
	'mA'		:	40.0,

	# Monochromator
	'filter'	:	'Mirrors',
	'polarization':	0.0,
	'slits'		:	[0.0, 0.0],

	# Image stats
	'valmin'	:	0,
	'valmax'	:	0,
	'valavg'	:	0.0,
	'valsig'	:	0.0,
	'histbeg'	:	0,
	'histend'	:	0,
	'histmax'	:	0,
}

h345_keywords = ['PROGRAM', 'DATE', 'SCANNER', 'FORMAT', 'HIGH',
		 'PIXEL', 'OFFSET', 'GAPS', 'ADC', 'MULTIPLIER',
		 'GAIN', 'WAVELENGTH', 'DISTANCE', 'RESOLUTION',
		 'PHI', 'OMEGA', 'CHI', 'TWOTHETA', 'CENTER',
		 'MODE', 'TIME', 'COUNTS', 'INTENSITY', 'HISTOGRAM',
		 'GENERATOR', 'MONOCHROMATOR', 'COLLIMATOR',
		 'DETECTOR', 'REMARK' ]

h345_line  = {
	( 'PROGRAM', '' )	: '',
	( 'DATE', '' )		: '',
	( 'REMARK', '' )	: '',
	( 'DETECTOR', '' )	: '',
	( 'SCANNER', '')	: 0,
	( 'FORMAT', 'PCK')	: 0,
	( 'FORMAT', 'IMAGE')	: 0,
	( 'FORMAT', '')		: 0,
	( 'HIGH', '')		: 0,
	( 'DISTANCE', '')	: 0.0,
	( 'WAVELENGTH', '')	: 0.0,
	( 'RESOLUTION', '')	: 0.0,
	( 'CHI', '')		: 0.0,
	( 'TWOTHETA', '')	: 0.0,
	( 'TIME', '')		: 0.0,
	( 'GAIN', '')		: 0.0,
	( 'GAPS', '')		: 0.0,
	( 'ADC', 'ADD_A')	: 0,
	( 'ADC', 'ADD_B')	: 0,
	( 'ADC', 'A')		: 0,
	( 'ADC', 'B')		: 0,
	( 'MODE', 'TIME')	: 0,
	( 'MODE', 'DOSE')	: 0,
	( 'MULTIPLIER', '')	: 0.0,
	( 'INTENSITY', 'MIN' )	: 0.0,
	( 'INTENSITY', 'MAX' )	: 0.0,
	( 'INTENSITY', 'AVE' )	: 0.0,
	( 'INTENSITY', 'SIG' )	: 0.0,
	( 'HISTOGRAM', 'START')	: 0,
	( 'HISTOGRAM', 'END' )	: 0,
	( 'HISTOGRAM', 'MAX' )	: 0,
	( 'PIXEL','LENGTH' )	: 0.0,
	( 'PIXEL','HEIGHT')	: 0.0,
	( 'COLLIMATOR','WIDTH' ): 0.0,
	( 'COLLIMATOR','HEIGHT'): 0.0,
	( 'MONOCHROMATOR','POLAR'): 0.0,
	( 'MONOCHROMATOR','')	: 0.0,
	( 'GENERATOR','kV')	: 0.0,
	( 'GENERATOR','mA')	: 0.0,
	( 'GENERATOR','')	: 0.0,
	( 'OFFSET', 'ROFF' )	: 0.0,
	( 'OFFSET', 'TOFF' )	: 0.0,
	( 'CENTER', 'X' )	: 0.0,
	( 'CENTER', 'Y' )	: 0.0,
	( 'PHI', 'START' )	: 0.0,
	( 'PHI', 'END' )	: 0.0,
	( 'PHI', 'OSC' )	: 1,
	( 'OMEGA', 'START' )	: 0.0,
	( 'OMEGA', 'END' )	: 0.0,
	( 'OMEGA', 'OSC' )	: 1,
	( 'COUNTS', 'START' )	: 0.0,
	( 'COUNTS', 'END' )	: 0.0,
	( 'COUNTS', 'MIN' )	: 0.0,
	( 'COUNTS', 'MAX' )	: 0.0,
	( 'COUNTS', 'AVE' )	: 0.0,
	( 'COUNTS', 'SIG' )	: 0.0,
	( 'COUNTS', 'NMEAS' )	: 0
}

###########################################################################
## Class:       Mar345
## Arguments:   name:      filename
##              data:      image array for image output
##              header:    4k image header for image output
##              verbose:   default=0
###########################################################################
class Mar345( ):
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Function:         __init__
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, name=None, data=None, header=None, verbose=0):
        '''Mar345::__init__: initialize class'''
        self.__name__   = 'mar345'
        self.verbose    = verbose
        self.x		    = 1
        self.y		    = 1
        self.pixels	    = 0
        self.high	    = 0
        self.filename   = name
        self.success    = False
        self.data       = None
        self.header     = h345      # Fill header with defaults
        self.raw_header = None
        self.bpp        = 2
        if self.verbose > 1: print("Mar345::__init__: ")
        # Has a file name been given?
        if name != None:
            if isinstance(data, np.ndarray):    # Datar given: write image
                self.write( name, data, h345 if header == None else header)
            else:                               # No data given: read image
                self.read(name)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Function:         string64
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def string64(self,s):
        '''Mar345::string64: make a string 64 chars long, end with newline'''
        i = len(s)
        return ( s+(63-i)*' '+'\n')

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Function:         makeheader
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def makeheader(self, h=None):
        '''Mar345::_makeheader: returns a 4k header string'''
        # Optional argument is a h345 dictionary
        if h == None: h = h345

        # Check contents of dictionary, use defaults for missing stuff
        if not 'x' in h:                h['x'] = self.x
        if not 'pixels' in h:           h['pixels'] = self.x*self.y
        if not 'high' in h:             h['high'] = 0
        if not 'pixelsize' in h:        h['pixelsize'] = [ 0.15, 0.15 ]
        if not 'wavelength' in h:       h['wavelength'] = 1.5417890
        if not 'distance' in h:         h['distance'] = 100.
        if not 'phibeg' in h:           h['phibeg'] = 0.
        if not 'phiend' in h:           h['phibeg'] = 0.
        if not 'phiosc' in h:           h['phiosc'] = 0.
        if not 'omeosc' in h:           h['omeosc'] = 0.
        if not 'omebeg' in h:           h['omebeg'] = 0.
        if not 'omeend' in h:           h['omeend'] = 0.
        if not 'chi' in h:              h['chi'] = 0.
        if not 'theta' in h:            h['theta'] = 0.
        if not 'roff' in h:             h['roff'] = 0.
        if not 'toff' in h:             h['toff'] = 0.
        if not 'gaps' in h:             h['gaps'] = [0,0,0,0,0,0,0,0]
        if not 'adc'  in h:             h['adc' ] = [0,0]
        if not 'adc_add' in h:          h['adc_add' ] = [0,0]
        if not 'multipler' in h:        h['multiplier'] = 1.0
        if not 'resolution' in h:       h['resolution'] = 0.0
        if not 'gain' in h:             h['gain'] = 1.0
        if not 'kV' in h:               h['kV'] = 0.0
        if not 'mA' in h:               h['mA'] = 0.0
        if not 'polarization' in h:     h['polarization'] = 0.0
        if not 'source' in h:           h['source'] = "Synchrotron"
        if not 'remark' in h:           h['remark'] = ['']
        if not 'filter' in h:           h['filter'] = "Mirrors"
        if not 'center' in h:           h['center'] = [ self.x/2., self.y/2. ]
        if not 'slits' in h:            h['slits'] = [ 0.3, 0.3 ]
        if not 'dose_n' in h:
                h['dose_n' ] = 0
                h['dosebeg'] = 0
                h['doseend'] = 0
                h['dosemin'] = 0
                h['dosemax'] = 0
                h['doseavg'] = 0.
                h['dosesig'] = 0.
        if not 'valmin' in h:
                h['valsig']  = 0.
                h['valavg']  = 0.
                h['valmin']  = 0
                h['valmax']  = 0
        if not 'histmax' in h:
                h['histbeg']  = 0
                h['histend']  = 0
                h['histmax']  = 0

        self.header = h

        # First 32 integers contain:
        # byteorder[0], size_x[1], nhigh[2], format[3], timemode[4],
        # pixels[5], pixellength[6], pixelheight[7],
        # wavelength[8], distance[9], phibeg[10], phiend[11],
        # omebeg[12], omeend[13], chi[14], theta[15], [16-31]:ununsed
        h32 = np.zeros(32, dtype=np.int32)
        h32[0] = 1234
        h32[1] = h['x']
        h32[2] = h['high']
        h32[3] = 1
        h32[4] = 1
        h32[5] = h['pixels']
        h32[6] = int(h['pixelsize'][0]*1000)
        h32[7] = int(h['pixelsize'][1]*1000)
        h32[8] = int(h['wavelength']*1000000)
        h32[9] = int(h['distance']*1000)
        h32[10]= int(h['phibeg']*1000)
        h32[11]= int(h['phiend']*1000)
        h32[12]= int(h['omebeg']*1000)
        h32[13]= int(h['omeend']*1000)
        h32[14]= int(h['chi']*1000)
        h32[15]= int(h['theta']*1000)

        s = [ ]
        s.append(self.string64("mar research") )
        s.append(self.string64("PROGRAM        mario") )
        s.append(self.string64("DATE           {}".format( datetime.datetime.utcnow().ctime()) ))
        s.append(self.string64("FORMAT         {}  PCK {}".format(h['x'],h['pixels'])))
        s.append(self.string64("SCANNER        000") )
        s.append(self.string64("HIGH           {}".format(h['high']) ))
        s.append(self.string64('PIXEL          LENGTH {:.0f} HEIGHT {:.0f}'.format(h['pixelsize'][0]*1000.,h['pixelsize'][1]*1000.)))
        s.append(self.string64('OFFSET         ROFF {} TOFF {}'.format(h['roff'],h['toff'])))
        s.append(self.string64('GAPS           {}'.format(re.sub( '[,\[\]]','',str(h['gaps'])))))
        s.append(self.string64('ADC            A {} B {} ADD_A {} ADD_B {}'.format(h['adc'][0],h['adc'][1],h['adc_add'][0],h['adc_add'][1])))
        s.append(self.string64('MULTIPLIER     {:.3f}'.format(h['multiplier'])))

        s.append(self.string64('GAIN           {:.3f}'.format(h['gain'])))
        s.append(self.string64('WAVELENGTH     {:.6f}'.format(h['wavelength'])))
        s.append(self.string64('DISTANCE       {:.3f}'.format(h['distance'])))
        s.append(self.string64('RESOLUTION     {:.3f}'.format(h['resolution'])))
        s.append(self.string64('PHI            START {:.3f} END {:.3f}  OSC {}'.format(h['phibeg'],h['phiend'],h['phiosc'])))
        s.append(self.string64('OMEGA          START {:.3f} END {:.3f}  OSC {}'.format(h['omebeg'],h['omeend'],h['omeosc'])))
        s.append(self.string64('CHI            {:.3f}'.format(h['chi'])))
        s.append(self.string64('TWOTHETA       {:.3f}'.format(h['theta'])))
        s.append(self.string64('CENTER         X {:.3f} Y {:.3f}'.format(h['center'][0],h['center'][1])))
        s.append(self.string64('MODE           TIME'))
        s.append(self.string64('COUNTS         START {:.1f} END {:.1f} NMEAS {}'.format(h['dosebeg'],h['doseend'],h['dose_n'])))
        s.append(self.string64('COUNTS         MIN {} MAX {}'.format(h['dosemin'],h['dosemax'])))
        s.append(self.string64('COUNTS         AVE {:.1f} SIG {:.1f}'.format(h['doseavg'],h['dosesig'])))
        s.append(self.string64('INTENSITY      MIN {} MAX {} AVE {:.1f} SIG {:.1f}'.format(h['valmin'],h['valmax'],h['valavg'],h['valsig'])))
        s.append(self.string64('HISTOGRAM      START {} END {} MAX {}'.format(h['histbeg'],h['histend'],h['histmax'])))
        s.append(self.string64('GENERATOR      {} kV {:.1f} mA {:.1f}'.format(h['source'], h['kV'],h['mA'])))
        s.append(self.string64('MONOCHROMATOR  {} POLAR {:.1f}'.format(h['filter'],h['polarization'])))
        s.append(self.string64('COLLIMATOR     WIDTH {:.1f} HEIGHT {:.1f}'.format(h['slits'][0],h['slits'][1])))
        for r in h['remark']:
            s.append(self.string64('REMARK         {}'.format(r)))
        s.append(self.string64('END OF HEADER\n'))

        # Put all items in list into one string with lenght 4k
        s = ''.join(s)
        while len(s) < 4096-128: s=s+" "

        # s.append( bytes(h32) )  # First 128 bytes
        return ( bytes(h32)  + bytes(s.encode()) )

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Function:         write
    # Arguments:        name (mandatory), onlyheader (optional, False|True)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def write(self, name, data=None, header=None, onlyheader=False):
        '''Mar345::write: writes an image in mar345 format '''
        # Optional argument header can be a 4k string or a h345 dictionary
        self.filename   = name
        self.success    = False
        if isinstance( data, np.ndarray):
            self.pixels	    = data.shape[0]
            # Watch out: for mar345 images x may be != y (e.g.Dectris detectors)
            if self.x == 1:
                self.x		    = int(math.sqrt( self.pixels ))
                self.y		    = self.x
        if self.verbose > 1: print("Mar345::write: {} header={}".format(self.filename,onlyheader))
        fp = self.open( name=name, doread=False)
        if fp == None: return self

        # Open has been successful, so get image header
        if header == None:              # Makes image header out of thin air
            header = self.makeheader()
        elif isinstance(header, dict):  # Uses a given h345 dict
            header = self.makeheader(header)
        elif isinstance(header, str):   # Uses a full 4k header string
            print ("ERROR (Mar345::write:): header must be bytes not string")
            return self
        elif isinstance(header, bytes): # Uses a full 4k header string
            # Get byteorder, nx and pixels from header, don't rely on sqrt
            b = int.from_bytes( header[ 0: 4], 'little')
            if b == 1234:
                b = 'little'
            else:
                b = 'big'
            self.x = int.from_bytes( header[ 4: 8], b)
            self.pixels = int.from_bytes( header[20:24], b)
            self.y = int(self.pixels/self.x)
        ##################
        fp.write( header )
        ##################
        if onlyheader:
            fp.close()
            return self

        # Write high intensity records if some pixels are > 16 bits
        data = self.writehigh( fp, header, data.flatten() )

        # Close open file before going into library
        if fp != None: fp.close()

        # Write compressed data array
        self.writedata( data.flatten() )
        return self.success

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Function:     writehigh
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def writehigh(self,fp,header,data):
        '''Mar345::writehigh: writes mar345 high intensity pixels '''
        if data.max() < 65536 or fp == None: return data
        i = 0
        h = 0
        fp.seek( 4096 )
        h32=np.zeros(2, dtype=np.uint32)
        for n in data:
            if n > 65535:
                h32[0] = i
                h32[1] = np.uint32(n)
                fp.write( h32 )
                data[i] = 65535
                h+=1
                # print("qqq {:5d} @ {:-8d} {:6d} -> {}".format(h,i,int(n), int(data[i])))
            i+=1
        pos = fp.tell()

        if self.verbose > 1: print("Mar345::writehigh: {} > 16-bits".format(h))

        if self.header != None:
            if 'high' in self.header: self.header['high'] = h


        # Update the number of high intensity pixels in header:
        fp.seek( 8 )
        h32=np.zeros(1, dtype=np.uint32)
        h32[0] = h
        fp.write(h32)

        try:
            fp.seek( 448 )      # Entry "HIGH" starts at byte 448 of header
            s = 'HIGH           {:32s}'.format(str(h))
            fp.write(s.encode())
        except:
            pass
        fp.seek(pos)
        return data

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Function:     _writedata
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def writedata(self,data):
        '''Mar345::writedata: writes mar345 data array'''
        if self.verbose > 1: print("Mar345::writedata: ", self.x, self.y)
        if not data.dtype == np.int16: data = data.astype(np.int16)
        # Data I/O is via mario.c using CFFI
        # r should return the number of pixels read from file
        s = self.filename.encode('ascii', 'ignore') # self.filename is unicode!
        r = lib.Putmar345Data16(s,self.x,self.y,ffi.cast("short int *", ffi.from_buffer(data) ) )
        # r = mario.GetmarData32(s, 0, N, self.data )
        if r == self.x*self.y:  self.success = True

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Function:         open
    # Arguments:        filename (mandatory), onlyheader (optional, False|True)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def open(self, name=None, doread=True):
        if name == None: name=self.filename
        if name == None: return None
        try:
            fp = open(name, 'rb' if doread else 'wb')
            return fp
        except:
            print("ERROR (Mar345::open): Cannot open '{}' for {} ".format(name, "reading" if doread else "writing"))
            return None

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Function:         read
    # Arguments:        filename (mandatory), onlyheader (optional, False|True)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def read(self, name, onlyheader=False):
        """Mar345::read: reads an image in mar345 format """
        self.data       = None
        self.header     = None
        self.filename   = name
        self.success    = False
        if self.verbose > 1: print("Mar345::read: {} onlyheader={}".format(self.filename,onlyheader))

        fp = self.open(name)
        if fp == None: return self

        # Open has been successful, so get image header
        self.readheader( fp=fp )
        if self.success == False or ( onlyheader ):
            fp.close()
            return self

        # Open has been successful, so get image data
        self.readdata( )
        if self.success == False:
            self.x      = 1
            self.y      = 1
            self.data   = np.resize(np.array([0], np.int), [1,1] )
            fp.close()
            return self

        # Return
        fp.close()
        return self

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Function:     readdata
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def readdata(self):
        '''Mar345::readdata: reads mar345 image data'''
        if self.verbose > 1: print("Mar345::readdata: ", self.x, self.y)
        self.success = False
        N = self.x * self.y
        self.data = np.zeros( self.x * self.y, dtype=np.int32 )
        # Data I/O is via libmar345 using CFFI
        # r should return the number of pixels read from file
        s = self.filename.encode('ascii', 'ignore') # self.filename is unicode!
        r = lib.Getmar345DataFromName(s,N,ffi.cast("int *", ffi.from_buffer(self.data) ) )
        if r == N:  self.success = True
        return self

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Function:     readheader
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def readheader(self, name=None, fp=None):
        '''Mar345::readheader: reads mar345 image header'''
        if fp == None:
            fp = self.open( name if name != None else self.filename )

        n = 0
        h345_keys = list(h345_line.keys())

        # First 32 integers contain:
        # byteorder[0], size_x[1], nhigh[2], format[3], timemode[4],
        # pixels[5], pixellength[6], pixelheight[7],
        # wavelength[8], distance[9], phibeg[10], phiend[11],
        # omebeg[12], omeend[13], chi[14], theta[15], [16-31]:ununsed
        h32 = array.array('i')
        h32.fromfile(fp, 32)
        # First integer should be 1234, otherwise we need to swap bytes
        swap = False
        if h32[0] != 1234:
            h32.byteswap()
            h345['swap'] = 1
        if h32[0] != 1234:
            print("ERROR (Mar345::readheader): First integer in header should be 1234 but is %d.\nThis is NOT a mar345 image!" % h32[0])
            return None

        # Get first 16 integer values from file
        if self.verbose > 1: print(60*'+',"\nFirst 16 integers contain:\nItem Value\n",60*'+')
        while n < 16:
            i = h32[n]
            if h345['swap']: i.byteswap()
            if self.verbose > 1: print("%2d: %d" % ( n+1, i ))
            n += 1
        if self.verbose > 1: print(60*'+')

        # Dimensions
        self.x      = h32[1]
        self.y      = int(h32[5]/self.x)
        self.high   = h32[2]

        self.success = True

        # Byte 128: mar research
        fp.seek(128)
        line = fp.read(64)
        if line[:12] != b'mar research':
            print("WARNING (Mar345::readheader): byte 128 should start with string 'mar research' but starts with '%s'" % line[:12])
        else:
            if self.verbose > 1: print("Byte  128: %s" % line[:12], "\n", 60*'+')

        # Bytes 192-4096: 64-chars/line
        remarks = 0
        while fp.tell()  < 4096:
            barr = fp.read(64)
            # Last meaningful line in header is marked END OF HEADER
            if barr.startswith(b'END OF HEADER'): break
            try:
                line = barr.decode('ASCII')
            except:
                continue
            if self.verbose > 1: print(line[:-1].replace('\n','\0'))
            # Split each line in individual words starting with 'key'
            token = line.split()
            key = token[0]
            # Check key against h345_keys
            for x in h345_keys:
                keypair = list(x)
                mainkey = keypair[0]
                subkey 	= keypair[1]
                # Only 1 keyword in line
                if (len(subkey) == 0 ) and ( key == mainkey ):
                    if self.verbose > 2: print("No subkey for %s" % mainkey)
                    if key == 'HIGH':
                        h345['high'] = int(token[1])
                    elif key == 'FORMAT':
                        h345['x'] = int(token[1])
                        h345['y'] = int(token[1])
                    elif key == 'SCANNER':
                        h345['serial'] = int(token[1])
                    elif key == 'DISTANCE':
                        h345['distance'] = float(token[1])
                    elif key == 'WAVELENGTH':
                        h345['wavelength'] = float(token[1])
                    elif key == 'THETA':
                        h345['theta'] = float(token[1])
                    elif key == 'CHI':
                        h345['chi'] = float(token[1])
                    elif key == 'TIME':
                        h345['time'] = float(token[1])
                    elif key == 'GAIN':
                        h345['gain'] = float(token[1])
                    elif key == 'MULTIPLIER':
                        h345['multiplier'] = float(token[1])
                    elif key == 'REMARK':
                        h345['extra'] = " ".join(list(token[1:]))
                        h345['remark'].append( h345['extra']  )
                        remarks += 1
                    elif key == 'POLARIZATION':
                        h345['polarization'] = " ".join(list(token[1:]))
                    elif key == 'GENERATOR':
                        h345['source'] = " ".join(list(token[1:]))
                    elif key == 'DETECTOR':
                        h345['detector'] = " ".join(list(token[1:]))
                    elif key == 'PROGRAM':
                        h345['program'] = " ".join(list(token[1:]))
                    elif key == 'DATE':
                        h345['date'] = " ".join(list(token[1:]))

                # Line with keywords and subkeywords
                # print "keypair %s \t%s\t%s" % (keypair, mainkey, subkey)
                n = 1
                for y in token[1:]:
                    n += 1
                    if ( y == subkey ) and (key == mainkey):
                        if self.verbose > 2: print("Found key %s subkey %s" % ( key, subkey ))

                        if subkey == 'PCK' or subkey == 'IMGE':
                            h345['pixels'] = int(token[n])
                        elif subkey == 'ROFF':
                            h345['roff'] = float(token[n])
                        elif subkey == 'TOFF':
                            h345['toff'] = float(token[n])
                        elif subkey == 'TIME':
                            h345['type'] = 'TIME'
                        elif subkey == 'DOSE':
                            h345['type'] = 'DOSE'
                        elif subkey == 'ADD_A':
                            h345['adc_add'][0] = int(token[n])
                        elif subkey == 'ADD_B':
                            h345['adc_add'][1] = int(token[n])
                        elif subkey == 'A' and key == 'ADC':
                            h345['adc'][0] = int(token[n])
                        elif subkey == 'B' and key == 'ADC':
                            h345['adc'][1] = int(token[n])
                        elif subkey == 'X' and key == 'CENTER':
                            h345['center'][0] = float(token[n])
                        elif subkey == 'Y' and key == 'CENTER':
                            h345['center'][1] = float(token[n])
                        elif subkey == 'START' and key == 'PHI':
                            h345['phibeg'] = float(token[n])
                        elif subkey == 'END' and key == 'PHI':
                            h345['phiend'] = float(token[n])
                        elif subkey == 'OSC' and key == 'PHI':
                            h345['phiosc'] = int(token[n])
                        elif subkey == 'START' and key == 'OMEGA':
                            h345['omebeg'] = float(token[n])
                        elif subkey == 'END' and key == 'OMEGA':
                            h345['omeend'] = float(token[n])
                        elif subkey == 'OSC' and key == 'OMEGA':
                            h345['omeosc'] = int(token[n])
                        elif subkey == 'START' and key == 'HISTOGRAM':
                            h345['histbeg'] = int(token[n])
                        elif subkey == 'END' and key == 'HISTOGRAM':
                            h345['histend'] = int(token[n])
                        elif subkey == 'MAX' and key == 'HISTOGRAM':
                            h345['histmax'] = int(token[n])
                        elif subkey == 'MAX' and key == 'INTENSITY':
                            h345['valmax'] = int(token[n])
                        elif subkey == 'MIN' and key == 'INTENSITY':
                            h345['valmin'] = int(token[n])
                        elif subkey == 'AVE' and key == 'INTENSITY':
                            h345['valavg'] = float(token[n])
                        elif subkey == 'SIG' and key == 'INTENSITY':
                            h345['valsig'] = float(token[n])
                        elif subkey == 'SIG' and key == 'COUNTS':
                            h345['dosesig'] = float(token[n])
                        elif subkey == 'AVE' and key == 'COUNTS':
                            h345['doseavg'] = float(token[n])
                        elif subkey == 'MIN' and key == 'COUNTS':
                            h345['dosemin'] = float(token[n])
                        elif subkey == 'MAX' and key == 'COUNTS':
                            h345['dosemax'] = float(token[n])
                        elif subkey == 'START' and key == 'COUNTS':
                            h345['dosebeg'] = float(token[n])
                        elif subkey == 'END' and key == 'COUNTS':
                            h345['doseend'] = float(token[n])
                        elif subkey == 'NMEAS' and key == 'COUNTS':
                            h345['dose_n'] = int(token[n])
                        elif subkey == 'LENGTH' and key == 'PIXEL':
                            h345['pixelsize'][0] = int(token[n])
                        elif subkey == 'HEIGHT' and key == 'PIXEL':
                            h345['pixelsize'][1] = int(token[n])
            # End of:  for x in h345_keys:
        # End of: while fp.tell()  < 4096:
        # We come here if either END OF HEADER has been seen or if
        # 4096 bytes have been read
        if self.verbose > 1:
            print(60*'+', "\nByte %4d: END OF HEADER reached with %d remarks\n" % ( fp.tell(), remarks ), 60*'+')

        where   = h345['program'].find( "Version" )
        if ( where > 0 ): h345['version'] = h345['program'][ where+8: ]

        # Something wrong with x, y ?
        if h345['x'] == 0 and h345['y'] == 0 and h345['pixels'] > 0:
            h345['x'] = h345['y'] = int( math.sqrt( h345['pixels'] ) )

        # Non-square images:
        if h345['x'] * h345['y'] != h345['pixels'] and h345['pixels'] > 0:
            h345['y'] = int(h345['pixels'] / h345['x']) # Version 1.0.1 bug fix

        # Convert pixelsize into mm
        if h345['pixelsize'][0] <=0.0:
            if h345['x'] == 1200 or h345['x'] == 1600 or  h345['x'] == 2000 or  h345['x'] == 2300:
                h345['pixelsize'][0] = 150.
            else:
                h345['pixelsize'][0] = 100.
        if h345['pixelsize'][1] <=0.0:
            h345['pixelsize'][1] = h345['pixelsize'][0]
        if h345['pixelsize'][0] > 1.0: h345['pixelsize'][0] /= 1000.
        if h345['pixelsize'][1] > 1.0: h345['pixelsize'][1] /= 1000.

        # For debugging, print stuff
        if self.verbose > 2:
            K = list(h345.keys())
            V = list(h345.values())
            print(list(K))
            print(list(V))

        # For debugging, print stuff
        if self.verbose > 1:
            print("Program:                 \t %s" % h345['program'])
            print("Version:                 \t %s" % h345['version'])
            print("Date:                    \t %s" % h345['date'])
            print("Detector:                \t %s" % h345['detector'])
            print("Serial:                  \t %d" % h345['serial'])
            print("ADC A/B                  \t %d / %d " % (h345['adc'][0], h345['adc'][1]))
            print("ADC ADD_A/B              \t %d / %d " % (h345['adc_add'][0], h345['adc_add'][1]))
            print("Radial/tangential offset \t %d / %d " % (h345['roff'], h345['toff']))
            print("Gaps                     \t ", str(h345['gaps']).strip('[]'))
            print("Number of pixels in x,y: \t %d x %d = %d" % ( h345['x'], h345['y'], h345['pixels'] ))
            print("Number of 32-bit values: \t %d" % h345['high'])
            print("Pixelsize in x,y:        \t %1.3f %1.3f" % (h345['pixelsize'][0],h345['pixelsize'][1]))
            print("Center in x,y:           \t %1.3f %1.3f" % (h345['center'][0],h345['center'][1]))

            print("Exposure time:           \t %1.1f in %s mode" % (h345['time'],h345['type']))
            print("Phi:                     \t %-7.3f -> %1.3f\t x %d" % ( h345['phibeg'],h345['phiend'],h345['phiosc']))
            print("Omega:                   \t %-7.3f -> %1.3f\t x %d" % ( h345['omebeg'],h345['omeend'],h345['omeosc']))
            print("Distance:                \t %1.3f" % h345['distance'])
            print("Wavelength:              \t %1.5f" % h345['wavelength'])
            print("Chi:                     \t %1.3f" % h345['chi'])
            print("Two-theta:               \t %1.1f" % h345['theta'])
            print("Counts min/max:          \t %1.0f\t%1.0f" % ( h345['dosemin'], h345['dosemax'] ))
            print("Counts avg/sig:          \t %1.0f +/- %1.2f" % ( h345['doseavg'],h345['dosesig']))
            print("Counts start/end/N:      \t %1.0f\t%1.0f\t#=%d" % ( h345['dosebeg'], h345['doseend'],h345['dose_n']))
            print("Histogram start/end/max  \t %d\t%d\t%d" % ( h345['histbeg'], h345['histend'],h345['histmax']))
            print("Intensity min/max:       \t %d\t%d" % ( h345['valmin'], h345['valmax']))
            print("Intensity avg/sig:       \t %1.1f +/- %1.1f" % ( h345['valavg'], h345['valsig']))
            print("Generator:               \t %s" % h345['source'])
            print("Generator kV / mA        \t %1.1f \t %1.1f" % ( h345['kV'], h345['mA']))
            print("Monochromator:           \t %s" % h345['filter'])
            print("Polarization:            \t %s" % h345['polarization'])
            for x in h345['remark']:
                print("Remark:                  \t %s" % x)
            if self.verbose > 1: print(60*'+')

        # Put some important stuff into self
        self.x          = int(h345['x'])
        self.y          = int(h345['y'])
        self.pixels     = int(h345['pixels'])
        self.high       = int(h345['high'])

        # Put the mar345 header into self
        self.header     = h345

        # Go back to start of file and keep a copy of the raw header
        fp.seek( 0 )
        self.raw_header = fp.read(4096)
        del h32         # Version 2.1.0: free memory
        return self.raw_header

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Class/end:    Mar345
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

###########################################################################
## If this python file is called by itself, run the main program ...
###########################################################################
if __name__ == "__main__":
    print("mar345: Reading image")
    img = Mar345(name="../example/a.mar1200", verbose=2)
    print ("mar345: Shape of array is {}".format(  img.data.shape ))
    f = open( "x.raw32", "wb")
    f.write( img.data )
    f.close()
    print ("mar345: Wrote x.raw32")


