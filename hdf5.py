# -*- python -*-
#
# Copyright Christoph Lassner 2015.
#
# Distributed under the Boost Software License, Version 1.0.
#    (See http://www.boost.org/LICENSE_1_0.txt)

from __future__ import print_function
import sys
import os

from ._tools import _checkLibs, _setupPaths

from SCons.SConf import CheckContext
CheckContext.checkLibs = _checkLibs

_check_dict = {}
_hdf5_option_dict = {'--hdf5-dir':
                       {'dest':"hdf5_prefix",
                       'type':"string",
                       'nargs':1,
                       'action':"store",
                       'metavar':"DIR",
                       'default':os.environ.get("HDF5_ROOT"),
                       'help':"prefix for HDF5; should contain the 'bin', 'include', and 'lib' folders."},
                       '--hdf5-inc-dir':
                       {'dest':"hdf5_include",
                       'type':"string",
                       'nargs':1,
                       'action':"store",
                       'metavar':"DIR",
                       'help':"this folder should contain 'hdf5.h'.",
                       'default':os.environ.get("HDF5_INCLUDE_DIR")},
                       '--hdf5-lib-dir':
                       {'dest':"hdf5_lib",
                       'type':"string",
                       'nargs':1,
                       'action':"store",
                       'metavar':"DIR",
                       'help':"this folder should contain 'libhdf5'.",
                       'default':os.environ.get("HDF5_LIB_DIR")}}

def CheckHDF5(context):
    sample_source_file = r"""
#include <iostream>
#include <string>

#include <hdf5.h>
#include <H5Cpp.h>

int main (void) {
    hsize_t dims[2];
    dims[0] = 5;
    dims[1] = 5;
    H5::DataSpace dataspace(2, dims);
    return 0;
}
"""
    context.Message('Check building with HDF5... ')
    ex_prefix_dir = context.env.GetOption("hdf5_prefix")
    ex_lib_dir = context.env.GetOption("hdf5_lib")
    ex_include_dir = context.env.GetOption("hdf5_include")
    _setupPaths(context.env,
                prefix = ex_prefix_dir,
                include = ex_include_dir,
                lib = ex_lib_dir
                )
    result = (context.checkLibs(['hdf5', 'hdf5_cpp',
                                 'hdf5_hl', 'hdf5_hl_cpp'],
              sample_source_file))
    if not result:
        context.Result(0)
        print("Cannot build with HDF5.")
        return False
    result, output = context.TryRun(sample_source_file,'.cpp')
    if not result:
        context.Result(0)
        print("Cannot run program built with HDF5.")
        return False
    context.Result(1)
    return True
_check_dict['hdf5'] = {'options': _hdf5_option_dict,
                       'checks': [CheckHDF5]}