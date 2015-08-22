#!env /usr/bin/python 
# -*- coding: utf-8 -*-
# slice.py - split big file in place by chunks, with optional specified size (default is 2Gb)
# Works in both python2 and python3
# Former name: split_in_place.py 
import os, sys, os.path
_1Mb = 1024*1024

# filesize_b == filesize_in_bytes 
#unix version:
def filesize_b_unix(fname):
  statinfo =os.stat(fname)
  byte_size = statinfo.st_size
  return byte_size
  
def filesize_b_2step(fname):
  f = open(fname, "rb")
  f.seek(0, os.SEEK_END)
  byte_size = f.tell()
  f.close()
  return byte_size

def filesize_b(fname):
  return os.path.getsize(fname)
  
def filesize_Mb(fname):
  "returns file size rounded upto nearest 1Mb"
  byte_size = filesize_b(fname)
  MbSize = byte_size/ _1Mb
  if byte_size % _1Mb >0:
    MbSize +=1
  return Mbsize

def copy_tail(fname, cur_chunk_fname, chunk_sz):
  "chunk_sz is in bytes, everywhere in program"
  buf = "" #declare buffer
  j=0
  total_read= 0
  try:
    fin = open(fname, "rb")
    fout = open(cur_chunk_fname, "wb")
    #go to curent chunk start: and end-chunk_sz position
    endpos = os.fstat(fin.fileno()).st_size
    if endpos - chunk_sz<0:  
      print( "Error! copy_tail() negative offset")
    fin.seek(-1*chunk_sz, os.SEEK_END) #negative offset 
    while True:
      buf = fin.read(_1Mb) #copy chunk size, here it is 1Mb  #for debug it was set _1Mb/2 
      read_sz = len(buf)
      if read_sz==0: #EOF?
        break
      fout.write(buf)
      fout.flush()
      
      sys.stderr.write("#")
      total_read += read_sz
      
      j+=1
      if j%100==0: # Report progress every 100Mb
        print ("\b\b\b  %sMb..."%j)
      if False and j>127: #0/1===release/test, 127 = magic test no.
        print ("\ntest break:i=%s Mb" %j)  #warn the user
        break #!
  except IOError,e:
   print ("Error: can\'t write file %s: %s" %(cur_chunk_fname, str(e)) )
   return False
  else: #else-of-try == finally
   fout.close()
   fin.close()
   return True
   
def truncate_by(fname, cur_chunk_sz):
  try:
    endpos = filesize_b(fname)
    fout = open(fname, "a+b")#"wb") 
    #go to last chunk start: and end-cur_chunk_sz position
    #endpos = os.fstat(fout.fileno()).st_size
    if endpos - cur_chunk_sz<0:
      print ("Error! truncate_by() negative offset endpos=%d cur_chunk_sz=%d" \
               %(endpos, cur_chunk_sz))
    fout.truncate(endpos - cur_chunk_sz)
  except IOError:
   print ("Error: can\'t truncate file %s" %fname)
  else:
   fout.close()
  
def cut_one_chunk_from_end(fname, cur_chunk_sz, i):
  print("%d. chunk_size=%d"% (i, cur_chunk_sz))
  if cur_chunk_sz==0:
    return
  
  cur_chunk_fname =  fname + ".7z.%03d"%(i+1)  #was ".%03d"%i  #was "_%03d"%i 
  #special handling for last iteration
  if i==0:
    #skip copy, skip truncate. just rename
    os.rename(fname, cur_chunk_fname)
    return False
    
  #copy tail chunk
  copy_tail(fname, cur_chunk_fname, cur_chunk_sz)
  #truncate original file
  truncate_by(fname, cur_chunk_sz)
  return True
  
def slice_file(fname, chunk_sz):
  "split_file_by_chunks"
  list_sz = []
  remainder = filesize_b(fname) #returns file size rounded upto nearest 1Mb
  print ("filesize=%d" %remainder)
  first_time = True
  cur_chunk_sz = 0
  
  iterations_cnt = int(remainder / chunk_sz) #
  if remainder % chunk_sz>0:
    iterations_cnt+=1
  print ("%d chunks to be written" %iterations_cnt)
  
  for iReverse in range(iterations_cnt):
    # On the next line:  iterations_cnt-1 is for enumeration from 0
    i = iterations_cnt-1 - iReverse # i used in chunk filename; Forward enumeration
    if first_time:
      cur_chunk_sz = remainder % chunk_sz
      if cur_chunk_sz==0:
        continue
      cut_one_chunk_from_end(fname, cur_chunk_sz, i)
      first_time=False
    else:
      cur_chunk_sz = chunk_sz
      cut_one_chunk_from_end(fname, cur_chunk_sz, i)
    remainder-= cur_chunk_sz
  print ("Done. written %d chunks." %iterations_cnt)
  print ("To collect back execute: 7z x -mx0 %s.7z.001" %fname)

g_sUsage = """Usage: slice (s|g) [chunk_size_Mb] file
	where s|g is operation:
	 s - slice <file> by <chunk_size_Mb> pieces, enumerated; 
	      default <chunk_size_Mb> vlue is 2048, i.e. 2Gb
	 g - reglue back sliced chunks into original file, <file> here should be first chunk filename
	      i.e. look like 'file.7z.0001>'"""
 
def convert_str_to_bsize(chunk_sz_str):
    chunk_sz = int(chunk_sz_str)
    chunk_sz *= _1Mb 
    return chunk_sz

def main(argv):  
  #internal sizes are all in bytes, not Megabytes
  chunk_sz = 1* _1Mb #2048 * _1Mb #default value of splitter
  # Parse command line:
  oper = ""
  fname= ""
  if   len(argv)>=4:
    oper = argv[1]
    if oper !="s":
  	  print("Error, expecting 's' operation\n")
  	  print(g_sUsage)
  	  sys.exit(1)
    chunk_sz_str = argv[2] #chunk size in Megabytes 
    chunk_sz = convert_str_to_bsize(chunk_sz_str)
    fname = sys.argv[3]
  elif len(argv)==3:
    oper = argv[1]
    fname = argv[2]
  else:
    print (g_sUsage)
    sys.exit(1)
  # Main worker function:
  if   oper=="s":
    split_file_by_chunks(fname, chunk_sz)
  elif oper=="g":
    reglue_in_place(fname)
  else:
  	print("Error operation '%s', expecting (s|g)\n" %oper)
  	print(g_sUsage)
  #sys.exit()
  
if __name__=='__main__':
  main(sys.argv)
  
def test_slice(): #test slice_file()
  import shutil
  shutil.copy("dump.orig", "dump") 
  slice_file("dump", 1000000)

# Reconstruct back: cat
# >/$ cat dump_*>dump.restored
# Bug! Windows version of ">" appends '\r' chars after '\n' chars. corrupting restored file.
  
# Reconstruct back: "7z -mx0" (zero-compressor)
# > 7z x -mx0 dump.7z.001
# #splitting with 7z on 5Mb chunks is:> 7z a -v5m -mx0 src_file.7z src_file.iso
 
#=======================================================
# Rebuild: inplace!
def get_rebuilding_fname_n_count(fname_001):
  if fname_001[-4] not in [".", "_"]:
    return False,"",0
  fname = fname_001[:-4]
  
  # Get chunks count
  # get the first:
  i=0
  try:
    i = int( fname_001[-3:])
  except ValueError,e:
    return False,fname,count
  chunk_fname= fname + ".%03d"%i
  if not os.path.exists(chunk_fname):
    return False,fname,0
  
  # iterate while possible
  i=1 #base for "_%03d"  
  while True:
    chunk_fname= fname + ".%03d"%i
    if not os.path.exists(chunk_fname):
      i-= 1
      break    
    i+= 1
  return True,fname,(i+1)
  
def append_n_remove_ith_chunk_file(fname, chunk_fname):
  ok = False
  with open(fname,"ab") as fout:
    with open(chunk_fname, "rb") as fin:
      ok = copy_data(fin,fout)
  if ok:
    os.unlink(chunk_fname)
    
def copy_data(fin,fout):
  "note: this function has similar function: copy_tail()"
  buf = "" #declare buffer
  j=0
  total_read= 0
  try:
    while True:
      buf = fin.read(_1Mb) #copy chunk size, here it is 1Mb  #for debug it was set _1Mb/2 
      read_sz = len(buf)
      if read_sz==0: #EOF?
        break
      fout.write(buf)
      fout.flush()
      
      sys.stderr.write("#")
      total_read += read_sz
      
      j+=1
      if j%100==0: # Report progress every 100Mb
        print ("\b\b\b  %sMb..."%j)
      if False and j>127: #0/1===release/test, 127 = magic test no.
        print ("\ntest break:i=%s Mb" %j)  #warn the user
        break #!
    return True
  except IOError,e:
   print ("Error while copying: %s" %str(e))
   return False

def reglue_in_place(fname_001):
  "reconstruct_in_place"
  ok,fname,count = get_rebuilding_fname_n_count(fname_001)
  if not ok:
    print("Error finding large file for rebuild: index parsing error or file doesn't exist")
    return
  chunk_001_fname= fname + ".%03d"%1
  os.rename(chunk_001_fname, fname)
  for i in range(2, count):
    chunk_fname= fname + ".%03d"%i
    append_n_remove_ith_chunk_file(fname, chunk_fname)
  print ("Done. Written %d chunks." %(count-1)) #count-1, since chunks enumeration starts with 1

def test_reglue(orig_test_f): #test rebuild_in_place(fname_001)
  # slice
  import shutil
  shutil.copy(orig_test_f, "dump") 
  slice_file("dump", 1000000)
  # reglue
  reglue_in_place("dump.7z.001")

  x = os.system("fc %s dump.7z" %orig_test_f)
  #x = os.system("cmp %s dump.7z" %orig_test_f) #cmp utility is from *nix/MinGW
  if x==0: #"FC: различия не найдены"
    print("test_reglue %s ok" %orig_test_f)
  else: 
  	print("test_reglue %s failed" %orig_test_f)
  return x==0

def test_reglue1():
  #test_reglue("dump.orig")
  test_reglue("dump339.rar") #dump339.rar = D:\Шлахтер\Tehnologija kar.rar
