#!/usr/bin/env python
"""
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Module:         w345
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Description:    Python code to write a mar345 image using random data
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Author:         Claudio Klein
                marXperts GmbH
                Werkstr.3
                22844 Norderstedt / Germany
                Claudio.Klein@marxperts.com
                www.marxperts.com
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
History:
Version         Date        Description
1.0             16/02/2021  Original version
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""
import os, sys, array, time, optparse, math, re
path = os.path.dirname(__file__)
sys.path.append(path)
import numpy as np
from mario import mar345

###########################################################################
## If this python file is called by itself, run the main program ...
###########################################################################
def start():
    p= optparse.OptionParser()
    p.add_option('-x', '--x',      default=1200, type="int",help="Number of pixels in x")
    p.add_option('-y', '--y',      default=1200, type="int",help="Number of pixels in y")
    p.add_option('-o', '--outfile', default=None, help="Name of output file")
    p.add_option('-v', '--verbose', default=0, action="count",help="Increase verbosity level")
    p.add_option('-d', '--debug',   default=0, type="int",help="Debug level")
    p.add_option('--prg',default="write345")
    o,r  = p.parse_args()

    # Arg without command line switch: probably a file name. Loop through r until valid file found
    if len(r)>0:
        for name in r:
            if o.outfile == None:
                o.outfile = name

    # Initialize Mar345 class
    img = mar345.Mar345(o.verbose)
    img.x = o.x
    img.y = o.x
    img.pixels = o.x*o.y
    # Create some random data with values between 0 and 512
    img.data = np.random.randint(0,high=512,size=(img.pixels,), dtype=np.uint32)
    # Circular image: set pixels outside radius to 0
    n = 0
    cx = o.x/2
    for y in range( o.y ):
        cy2 = math.pow(y-cx,2.)
        for x in range( o.x ):
            if math.sqrt( cy2 + math.pow(x-cx,2.) ) > cx: img.data[n] = 0
            n+=1
    # Update some important image header information
    img.header['x'] = img.x
    img.header['pixels'] = img.pixels
    # Update some optional image header information
    img.header['x'] = img.x
    img.header['valmax'] = int(img.data.max())
    img.header['valavg'] = img.data.mean()
    # Now, make the header and give it back to me as 4k byte string
    img.raw_header = img.makeheader()

    if o.debug>0:
        with open( 'header', 'wb') as fp: fp.write(img.raw_header)
        with open( 'data.raw32', 'wb') as fp: fp.write(img.data)

    # Write out mar345 image
    if o.outfile != None:
        img.write (o.outfile, img.data, img.raw_header)
        print ("{}: {} || {}x{} pixels || mean: {:6.1f} || max: {:6.0f}".format(o.prg, o.outfile, img.x, img.y, img.data.mean(),img.data.max()))

if __name__ == "__main__":
    start()
