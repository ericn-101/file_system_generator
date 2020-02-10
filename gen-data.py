#!/usr/bin/env python

"""
# FILE:     gen-data.py
# 
# PURPOSE:  This script generates a tree of directories and files under a top
#           dataroot directory. It is used when testing file systems or data
#           integrity across operations
#
# IC:       This script may be called any time.
#
# CALL:     This script is called as follows.
#           =  ./gen-data.py --dirDepth 5 --dirWidth 3
#           =  ./gen-data.py -m 5 -c 3
#
# INPUT:    <max dir depth>    = max_dir_depth    ==> must be >= 3
#           <dir entry count>  = dir_entry_count  ==> must be >= 2
#           <data root dir>    = dataroot_dir    e.g. "datagenA/datarootA"
# 
# OUTPUT:   hierarchical tree of directories and files each created 
#           using a random name.
# TO DO:
# 1. Make timestamp an optional param
# 2. Add NFS mount controls
#
# VERSION AND CHANGE HISTORY
#   V1.04 - 2014-02-19 - EN
#           Added inputs and parsing for user-defined dataroot
#   V1.03 - 2013-10-06 - EN
#           Changed option tags
#   V1.02 - 2013-09-19 - EN
#           Added timestamp option to file name
#           Improved dup dir name handling
#   V1.01 - 2013-05-17 - EN
#           Added argparse 
#   V1.00 - 2013-01-23 - EN
#       1)  Created Script
"""

import argparse
import datetime
import os
import random
import shutil
import string
import sys
import time
random.seed()


def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
  """ 
  # NAME:        timeStamped
  # DESCRIPTION: Inserts a time stamp into the filename
  # USAGE:       
  # INPUTS:      fname = file name we instead to create
  # OUTPUTS:     Updated file name with date-time stamp prepended to fname
  """
  return datetime.datetime.now().strftime(fmt).format(fname=fname)


def randChars(x):
  """
  # NAME:        randChars
  # DESCRIPTION: Generates a string of random ascii letters
  # USAGE:       
  # INPUTS:      x = Integer number of random characters to generate
  # OUTPUTS:     random character string of length x 
  """
  return ''.join(random.choice(string.ascii_letters) for y in range(x))
  # return ''.join(random.choice(string.printable) for y in range(x))


def randLine(x):
  """
  # NAME:        randLine
  # DESCRIPTION: Generates a line of random ascii letters
  # USAGE:       
  # INPUTS:      x = Integer number of characters in string
  # OUTPUTS:     random character string of approximate length x 
  """
  str_list = []
  while x > 0:
    offset = random.randint(1, x) 
    # print 'offset =', offset
    str_list.append(randChars(offset))
    str_list.append(' ')
    x = x - offset - 1
    # print 'result so far = ', str_list
  else:
    str_list.append('\n')
    return ''.join(str_list)


def parse_filespec(file_spec):
  """
  # NAME:        parse_filespec
  # DESCRIPTION: Splits input file spec into list.
  #              Should be used for filespecs to a file
  # USAGE:       
  # INPUTS:      file_spec = full or partial path specification
  #                        = /home/Eric Nelson,gen-data/datagenA/datarootA'
  # OUTPUTS:     return = [[pathlist], filename, ext] as a list
  #              rv =  (['/', 'home', 'Eric Nelson', 'gen-data', 'datagenA'], 'datarootA', '')
  """
  (root, ext) = os.path.splitext(file_spec)
  (x, name) = os.path.split(root)
  # dummy value
  y = '-'		
  parts = []
  while y <> '':
    (x, y) = os.path.split(x)
    parts.append(y)
  parts = parts[:-1]
  if x:
    parts.append(x)
  parts.reverse()
  return (parts, name, ext)


def split_fspec(path):
  """
  # NAME:        split_fspec
  # DESCRIPTION: Splits input file spec into list.
  #              Should be used for any filespecs
  # USAGE:       
  # INPUTS:      file_spec = full or partial path specification
  #                        = /home/Eric Nelson/gen-data/datagenA/datarootA
  #                        = /root/datagenA/datarootA/fdsdg.444
  # OUTPUTS:     return = [[pathlist], filename, ext] as a list
  #              rv =  ['/', 'home', 'Eric Nelson', 'gen-data', 'datagenA', 'datarootA']
  #              rv =  ['/', 'root', 'datagen-A', 'datarootA', 'fdsdg.444']
  """
  allparts = []
  while 1:
    parts = os.path.split(path)
    if parts[0] == path:  # sentinel for absolute paths
      allparts.insert(0, parts[0])
      break
    elif parts[1] == path: # sentinel for relative paths
      allparts.insert(0, parts[1])
      break
    else:
      path = parts[0]
      allparts.insert(0, parts[1])
  return allparts
  

def create_dirs(n_digits, n_dirs, target_dir):
  """
  # NAME:        create_dirs
  # DESCRIPTION: Generates a number directories in target_dir
  # USAGE:       
  # INPUTS:      n_digits = Integer number of characters in string
  #              n_dirs = Integer number of directories to create
  #              target_dir = root directory path
  # OUTPUTS:     directories created in target_dir
  #              return = dir_list 
  """
  os.chdir(target_dir)
  result_list = []
  for i in range(n_dirs):
    dir_name = randChars(random.randint(1, n_digits))
    done = 0
    while done == 0:
      if os.path.isdir(os.path.join(target_dir, dir_name)):
        dir_name = dir_name + '-1'
        print 'WARN: Found duplicate dir name and modified new dir name to be different'
        if debugswitch > 0:
          time.sleep(2)
      elif os.path.isfile(os.path.join(target_dir, dir_name)):
        dir_name = dir_name + '-1'
        print 'WARN: Found dir name used as a file name and modified new dir name to be different'
        if debugswitch > 0:
          time.sleep(2)
      else:
        done = 1
        if debugswitch > 0:
          print 'DEBUG: Found unique dir name = ', dir_name
          time.sleep(0.25)

    # os.mkdir(os.path.join(target_dir, dir_name))
    os.mkdir(dir_name)
    if debugswitch > 0:
      print 'DEBUG: Added dir name = ', dir_name
      time.sleep(0.25)
    result_list.append(os.path.join(target_dir, dir_name))
  return result_list


def file_accessible(file_path, mode):
  """ 
  # NAME:        file_accessible
  # DESCRIPTION: Absolutely guarantee that the file not only exists, but is 
  #              accessible at the current time
  # USAGE:       Say the file "foo.txt" exists and is readable,
  #              whereas the file "bar.txt" doesn't exist.
  #              >>> foo_accessible = file_accessible("foo.txt", "r")
  #              True
  #              >>> bar_accessible = file_accessible("bar.txt", "r")
  #              False
  # INPUTS:      file_path = file spec
  #              mode = file mode
  # OUTPUTS:     True = accessible
  #              False = not accessible 
  """
  try:
    fileD = open(file_path, mode)
  except IOError as errorD:
    return False
  return True


def file_create_rand(n_digits, line_len, max_lines, target_dir):
  """
  # NAME:        file_create_rand
  # DESCRIPTION: Generates a randonly populated file in target_dir
  # USAGE:       
  # INPUTS:      n_digits = Integer number of characters in name
  #              line_len = target line length for data
  #              max_lines = max number of lines to write to file
  #              target_dir = directory path
  # OUTPUTS:     files created in target_dir
  #              return = file_name 
  """
  # Verify directory exists
  if os.path.isdir(target_dir):
    os.chdir(target_dir)
  else:
    print 'Directory path', target_dir, 'is not a valid directory - check code'
    return False
  # Open File
  f_name = randChars(random.randint(1, n_digits))
  file_path = os.path.join(target_dir, f_name)
  if os.path.isdir(file_path):
    # Error indication
    print 'File spec', file_path, 'is existing directory - try again'
    return False
  elif file_accessible(f_name, "r"):
    # Error indication
    print 'File spec', file_path, 'already exists - try again'
    return False
  else:
    # OK to create it since it's not a dir or a file
    # f_handle = open(f_name, "w")
    with open(timeStamped(f_name),"w") as f_handle:
      num_lines = random.randint(5, max_lines)
      for i in range(num_lines):
        f_handle.write(randLine(line_len))
    f_handle.close
  return f_name



# #############################################################################
#  MAIN
# #############################################################################
"""
DESCRIPTION:    A Python script, gen-data.py, is for generating test
                data. The data produced is mostly random, but with a few
                constraints. Starts from a single top-level directory called 
                'dataroot'. Within this directory we have regular files and 
                sub-directories. The regular files contain lines of randomly 
                generated text. The lines are approximately 60 characters long. 
                The number of lines is between 5 and 15, chosen at random for 
                each file.

                The dataroot directory should have a random mix of files and
                sub-directories. The sub-directories should also be populated in 
                a similar manner, with the maximum depth of nesting determined by 
                the first parameter given to the script on the command line. The 
                number of entries in each directory is given by a second command 
                line argument.

                For example,

                $ python2.7 gen-data.py 6 2
                $ tree dataroot

                dataroot
                |
                +-- ckk
                |   +-- bfkv
                |   |   +-- dzlgm
                |   |   |   +-- jsvm
                |   |   |   |   +-- ghxf
                |   |   |   |   +-- thl
                |   |   |   +-- jzhxs
                |   |   |       +-- dvjn
                |   |   |       +-- dvjn
                |   |   +-- jkgwz
                |   |       +-- mrlwkr
                |   |       +-- nszgprj
                |   |           +-- vtl
                |   |           +-- xxmqxb
                |   +-- plv
                |       +-- lvrvgzk
                |       +-- snsq
                +-- rxhnj

                12 directories, 6 files
                $

                This script should run on any linux distro and has been tested 
                on:
                Ubuntu Linux distro.
                Centos Linux distro
                Fedora Linux distro
                Cygwin linux distro

CALL:           =  ./gen-data.py --dirDepth 5 --dirWidth 3 --rootDir "datagen-A/datarootA"
                =  ./gen-data.py -d 5 -w 3 -r "datagen-A/datarootA"
"""

# Process User Inputs and Check Usage
if len(sys.argv) < 5 or len(sys.argv) > 9:
  print 'arg count = ',len(sys.argv)
  print 'USAGE: gen-data.py -d <max dir depth> -w <dir entry count> [-r <dataroot>]'
  sys.exit()

mParser = argparse.ArgumentParser()
mParser.add_argument("-d", "--dirDepth", help="maximum directory depth to create", type=int)
mParser.add_argument("-w", "--dirWidth", help="maximum number of entries per directory to create", type=int)
mParser.add_argument("-r", "--rootDir",  help="data root path from current location", type=str)
mParser.add_argument("-x", "--debug",    help="Debug on|off switch", type=int)

args = mParser.parse_args()
if args.dirDepth:
  max_dir_depth = args.dirDepth
  print 'max_dir_depth = ',max_dir_depth

if args.dirWidth:
  dir_entry_count = args.dirWidth
  print 'dir_entry_count = ',dir_entry_count

if args.rootDir:
  dataroot = args.rootDir
  print 'dataroot = ',dataroot
else:
  dataroot = 'dataroot'
src_dir = os.getcwd()
root_dir = os.path.join(src_dir, dataroot)
if os.path.isdir(root_dir):
    print 'STATUS: Clearing dest dir: ', root_dir
    try:
        shutil.rmtree(root_dir)
    except OSError as e:
        print ("ERROR: %s - %s." % (e.filename, e.strerror))

if args.debug:
  debugswitch = args.debug
  print 'debugswitch = ',debugswitch
else:
  debugswitch = 0

if max_dir_depth < 3:
  print 'USAGE: <max dir depth> must be >= 3'
  if dir_entry_count < 2:
    print 'USAGE: <dir entry count> must be >= 2'
  sys.exit() 
elif dir_entry_count < 2:
  print 'USAGE: <dir entry count> must be >= 2'
  sys.exit()


# Proceed To Make Directories and Files
src_dir = os.getcwd()
print 'script source dir =', src_dir
# root_dir = os.path.join(src_dir, 'dataroot')
root_dir = os.path.join(src_dir, dataroot)

print 'root dir =', root_dir
if os.path.exists(root_dir):
  os.chdir(root_dir)
else:
  check_path_list = split_fspec(dataroot)
  print 'checking data path = ', check_path_list
  start_dir = src_dir
  for path_frag in check_path_list:
    print 'checking for ', path_frag, ' in current dir ', start_dir
    if not os.path.exists(os.path.join(start_dir, path_frag)):
      os.mkdir(os.path.join(start_dir, path_frag))
      start_dir = os.path.join(start_dir, path_frag)
      os.chdir(start_dir)
    else:
      print 'found ', path_frag, ' in current dir ', start_dir
      start_dir = os.path.join(start_dir, path_frag)
      os.chdir(start_dir)

      
current_dir = os.getcwd()
start_level = current_dir.count(os.sep)
print 'script working dir = ', current_dir

dir_list = []
dir_list.append(root_dir)

dir_depth = 1
dir_idx = 0
max_file_name_len = 10
line_len = 60
max_lines = 15
done = 'false'

while done == 'false':
  print 'processing dir_list', dir_list, 'index', dir_idx
  node_dir = dir_list[dir_idx]
  os.chdir(node_dir)

  if dir_depth < max_dir_depth:
    dir_count = random.randint(1, dir_entry_count)
    file_count = dir_entry_count - dir_count
    print 'node dir', node_dir, 'has', dir_count, 'directories and', file_count, 'files\n'

    # process any subdirectories for this level
    if dir_count > 0:
      return_list = create_dirs(max_file_name_len, dir_count, node_dir)
      for i in return_list:
        dir_list.append(i)
      print 'dir_list =', dir_list, 'dir_idx =', dir_idx
      dir_idx += 1
    else:
      print 'node_dir =', node_dir, 'has no sub-directories'

    # Process any files for this level
    if file_count > 0:
      for j in range(file_count):
        file_name = file_create_rand(max_file_name_len, line_len, max_lines, node_dir)
        print 'file created =', file_name
    else:
      print 'node_dir =', node_dir, 'has no files'
  else:
    file_count = dir_entry_count
    for j in range(file_count):
      file_name = file_create_rand(max_file_name_len, line_len, max_lines, node_dir)
      print 'file created =', file_name
    dir_idx += 1

  # Check for max dir depth
  current_level = node_dir.count(os.sep)
  dir_depth = current_level - start_level
  print 'On loop', dir_idx, 'directory depth =', dir_depth, 'breaking out of loop'
  if dir_idx >= len(dir_list):
    done = 'true'
    break
  elif dir_depth >= max_dir_depth:
    # file_count = len([name for name in os.listdir('.') if os.path.isfile(name)])
    file_count = len([name for name in os.listdir('.')])
    if file_count < dir_entry_count:
      add_files = dir_entry_count - file_count
      for j in range(add_files):
        file_name = file_create_rand(max_file_name_len, line_len, max_lines, node_dir)
        print 'file created =', file_name
        