#!/usr/bin/env python
"""
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Module:         rw345
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Description:    Python code to read and write mar345 images
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
1.1             10/11/2020  Some modifications in star
1.0             04/09/2019  Original version
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
    norm = (1.0, 1.0)
    p= optparse.OptionParser()
    p.add_option('-1','-i','--file1', default=None, help="Name of 1st input file")
    p.add_option('-2', '--file2',  default=None, help="Name of 2nd input file")
    p.add_option('-s','--scale',   default=None, help="Scale factor(s)")
    p.add_option('-b', '--bpp',    default=4, type="int",help="Bytes per pixel")
    p.add_option('-x', '--x',      default=0, type="int",help="Number of pixels in x")
    p.add_option('-y', '--y',      default=0, type="int",help="Number of pixels in y")
    p.add_option('-o', '--outfile', default=None, help="Name of output file")
    p.add_option('-v', '--verbose',default=0, action="count",help="Increase verbosity level")
    p.add_option('--prg',default="write345")
    o,r  = p.parse_args()

    # Arg without command line switch: probably a file name. Loop through r until valid file found
    if len(r)>0:
        for name in r:
            if o.file1 == None:
                o.file1 = name
            elif o.file2 == None:
                o.file2 = name
            elif o.outfile == None:
                o.outfile = name

    if o.scale != None:
        # Replace all occurences of (),{},[] and colon by blank
        s = re.sub(r'[\[\],(){}]',' ',o.scale).split()
        if len(s) == 1:
            try:    # try single scale factor first
                norm = ( float(s[0]), 1.0 )
            except:
                print("ERROR with scale: use -s 1.0 or alike")
                sys.exit(0)
        elif len(s) == 2:
            try:    # try single scale factor first
                norm = ( float(s[0]), float(s[1]) )
            except:
                print("ERROR with scale: use -s 1.0,2.0 or alike")
                sys.exit(0)


    mar345a = mar345.Mar345(o.verbose)
    img1 = mar345a.read(o.file1)
    print ("{}: {} || {}x{} pixels || mean: {:6.1f} || max: {:6.0f}".format(o.prg, o.file1, img1.x, img1.y, img1.data.mean(),img1.data.max()))
    if norm[0] != 1.0:
        print("Scale factor for img1: {:.3f}".format(norm[0]))
        img1.data = img1.data*norm[0]

    if o.file2 != None:
        # Create new instance of Mar345 class for 2nd file
        mar345b = mar345.Mar345(o.verbose)
        img2 = mar345b.read(o.file2)
        print ("{}: {} || {}x{} pixels || mean: {:6.1f} || max: {:6.0f}".format(o.prg, o.file2, img2.x, img2.y, img2.data.mean(),img2.data.max()))
        if len(norm) > 1:
            print("Scale factor for img2: {:.3f}".format(norm[1]))
            if norm[1] != 1.0:  img2.data = img2.data*norm[1]

        # Combine images 1 and 2
        img1.data = img1.data+img2.data

    # The data format is supposed to be a 32-bit binary array of x
    if o.outfile != None:
        mar345a.write (o.outfile, img1.data, img1.raw_header)
        print ("{}: {} || {}x{} pixels || mean: {:6.1f} || max: {:6.0f}".format(o.prg, o.outfile, img1.x, img1.y, img1.data.mean(),img1.data.max()))

if __name__ == "__main__":
    start()
