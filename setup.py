#!/usr/bin/env python3
#coding: utf8
"""
Setup script for python distutils package and mario
Ubuntu users: use easy_install (contained in  python-setuptools)
We need the following packages: python3-dev python3-setuptools
"""
import os, sys, platform, io, subprocess, pathlib, glob

OS          = platform.system()
NAME        = 'mario'
VERSION     = '0.0.0'
URL         = 'https://www.marxperts.com'
EMAIL       = 'claudio.klein@marxperts.com'
AUTHOR      = 'Claudio Klein, marXperts GmbH'
REQUIRES_PYTHON = '>=3.0'
DESCRIPTION = 'Python module for reading and writing mar images'
REQUIRED    = [ ]
EXTRAS      = { }

# Check setuptools
try:
    from setuptools import setup, find_packages
except ImportError:
    print("ERROR: missing setuptools, please install using\n    sudo apt install python3-setuptools")
    sys.exit(0)

# Local path = here
here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Build C library with CFFI ###################################################
if "Win" in OS:
    mylib = '_libmar345.pyd'
elif "Darwin" in OS:
    V = sys.version_info[:3]
    # mylib = '_libmar345.dylib'
    mylib = "_libmar345.cpython-{}{}-darwin.so".format( V[0], V[1])
else:
    mylib = '_libmar345.so'
sosrc = 'lib/_libmar345.{}.{}.so'.format(platform.system(),platform.machine())
sodst = 'mario/{}'.format( mylib )
#
if not os.path.exists( sosrc ) or not os.path.exists( sodst ):
    try:
        subprocess.call("cd lib;python buildlib.py", shell=True)
    except:
        print("ERROR: Cannot build C library" )

if os.path.exists( sosrc ):
    print("Copy {} to {}".format( sosrc, sodst ))
    import shutil
    if os.path.exists( sodst ): os.remove( sodst )
    shutil.copyfile( sosrc, sodst )

# Load the package's version.py module as a dictionary.
about={}
fn='{}{}{}{}version.py'.format(here,os.path.sep,NAME,os.path.sep)
if os.path.exists(fn):
    with open(os.path.join(here, os.path.sep, fn)) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

# On Windows ...
if OS == 'Windows':
    pass
# On Unix ...
else:
    # if not os.path.isfile( "/usr/bin/python3-config" ) :
    try:
        subprocess.call("which python3-config", shell=True)
    except:
        print("ERROR: missing requirement, please install using\n    sudo apt install python3-dev")
     #    sys.exit(0)

# Get all precompiled C-libs
clibs = []
for i in glob.glob( "lib{}_libmar345.*.*.*".format(os.path.sep) ):
    f = "lib{}{}".format( os.path.sep,os.path.basename(i))
    clibs.append( f )
for i in glob.glob( "lib{}marpck.*".format(os.path.sep) ):
    f = "lib{}{}".format( os.path.sep,os.path.basename(i))
    clibs.append( f )
for i in glob.glob( "lib{}build*.py".format(os.path.sep) ):
    f = "lib{}{}".format( os.path.sep,os.path.basename(i))
    clibs.append( f )

# Get all files in example
example = [ ]
for i in glob.glob( "example{}*".format(os.path.sep) ):
    f = "example{}{}".format( os.path.sep,os.path.basename(i))
    example.append( f )

print (60*'+')
print ("Master directory:  \t {}".format(here))
print ("Libraries:         \t {}".format( clibs ))
print ("My library:        \t {}".format( mylib  ))
print ("Examples:          \t {}".format( example ))
print (60*'+')

"""
"""

# Run setup
setup(
    name=NAME,
    version=about['__version__'],
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    install_requires=REQUIRED,
    python_requires=REQUIRES_PYTHON,
    extras_require=EXTRAS,
    url=URL,
    ext_package='',

    #packages=[NAME, ''],
    packages=[NAME, 'mario'],
    package_data={ NAME: [ mylib ] },

    # packages=find_packages(where=NAME),
    scripts=[ ],
    options = { },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python/C :: 3',
        'Environment :: Console',
        'License :: Freely Distributable',
        'Topic :: Software Development :: Debuggers',
        ],
    zip_safe=False  # For using C-libs: cannot do this from zipped egg
)
