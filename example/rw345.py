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
    norm = (1.0, 1.0)
    p= optparse.OptionParser()
    p.add_option('-1','-i','--file1', default=None, help="Name of 1st input file")
    p.add_option('-2', '--file2',  default=None, help="Name of 2nd input file")
    p.add_option('-s', '--scale',   default=None, help="Scale factor(s)")
    p.add_option('-x', '--x',      default=0, type="int",help="Number of pixels in x")
    p.add_option('-y', '--y',      default=0, type="int",help="Number of pixels in y")
    p.add_option('-o', '--outfile', default=None, help="Name of output file")
    p.add_option('-v', '--verbose',default=0, action="count",help="Increase verbosity level")
    p.add_option('--prg',default="rw345")
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


    # Read 1st image: give filename
    img1 = mar345.Mar345(name=o.file1, verbose=o.verbose)
    print ("{}: {} || {}x{} pixels || mean: {:6.1f} || max: {:6.0f}".format(o.prg, o.file1, img1.x, img1.y, img1.data.mean(),img1.data.max()))
    if norm[0] != 1.0:
        print("Scale factor for img1: {:.3f}".format(norm[0]))
        img1.data = img1.data*norm[0]

    if o.file2 != None:
        # Read 2nd image: give filename
        img2 = mar345.Mar345(name=o.file2, verbose=o.verbose)
        print ("{}: {} || {}x{} pixels || mean: {:6.1f} || max: {:6.0f}".format(o.prg, o.file2, img2.x, img2.y, img2.data.mean(),img2.data.max()))
        if len(norm) > 1:
            print("Scale factor for img2: {:.3f}".format(norm[1]))
            if norm[1] != 1.0:  img2.data = img2.data*norm[1]
        # Combine data from images 1 and 2
        img1.data = img1.data+img2.data

    if o.outfile != None:
        # For image output, also give data array and 4k image header from file1
        # The no. of pixels > 16bit will be updated automatically
        s = mar345.Mar345(name=o.outfile,data=img1.data,header=img1.raw_header)
        print ("{}: {} || {}x{} pixels || mean: {:6.1f} || max: {:6.0f}".format(o.prg, o.outfile, img1.x, img1.y, img1.data.mean(),img1.data.max()))

if __name__ == "__main__":
    start()
