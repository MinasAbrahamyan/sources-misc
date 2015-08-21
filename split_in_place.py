#!env /usr/bin/python 
# split_in_place.py - split big file in place by chunks, with optional specified size 
# Works in both python2 and python3
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
  try:
    fin = open(fname, "rb")
    fout = open(cur_chunk_fname, "wb")
    #go to curent chunk start: and end-chunk_sz position
    endpos = os.fstat(fin.fileno()).st_size
    if endpos - chunk_sz<0:  
      print( "Error! copy_tail() negative offset")
    fin.seek(-1*chunk_sz, os.SEEK_END) #negative offset 
    total_read= 0
    while True:
      buf = fin.read(_1Mb) #copy chunk size, here it is 1Mb  #for debug it was set _1Mb/2 
      read_sz = len(buf)
      if read_sz==0: #EOF?
        break
      fout.write(buf)
      fout.flush()
      
      #-\/sys.stderr.write("#")
      total_read += read_sz
      
      j+=1
      if j%100==0: # Report progress every 100Mb
        print ("\b\b\b  %sMb..."%j)
      if False and j>127: #0/1===release/test, 127 = magic test no.
        print ("\ntest break:i=%s Mb" %j)  #warn the user
        break #!
  except IOError:
   print ("Error: can\'t write file %s" %cur_chunk_fname)
  else: #else-of-try == finally
   fout.close()
   fin.close()
   sys.stderr.write("#")
   
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
  #-print "cut_one_chunk_from_end(): cur_chunk_sz=", cur_chunk_sz, "i=", i
  print("i=%d chunk_size="% (i, cur_chunk_sz))
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
  
def split_file_by_chunks(fname, chunk_sz):
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
  
def main(argv):  
  #internal sizes are all in bytes, not Megabytes
  chunk_sz = 1* _1Mb #2048 * _1Mb #default value of splitter
  fname=""
  if   len(argv)>=3:
    chunk_sz_str = argv[1] #chunk size in Megabytes 
    fname = sys.argv[2]
    chunk_sz = int(chunk_sz_str)
    chunk_sz *= _1Mb
  elif len(argv)==2:
    fname = argv[1]
  else:
    print ("Usage: split_in_place [nMbs] filename")
    sys.exit(1)
    print ("after exit()") #strange ipython-for-Windows
  # main worker function: 
  split_file_by_chunks(fname, chunk_sz)
  #sys.exit()
  
if __name__=='__main__':
  main(sys.argv)
  
def test(): #test split_file_by_chunks()
  import shutil
  shutil.copy("dump.orig", "dump") 
  split_file_by_chunks("dump", 1000000)

 # Reconstruct back: cat
 # >/$ cat dump_*>dump.restored
 # Bug! Windows version of ">" appends '\r' chars after '\n' chars. corrupting restored file.
  
 # Reconstruct back: "7z -mx0" (zero-compressor)
 # > 7z x -mx0 dump.7z.001
 # #splitting with 7z on 5Mb chunks is:> 7z a -v5m -mx0 src_file.7z src_file.iso
 
 ##=======================================================
 # Rebuild: inplace!
 def get_rebuilding_fname_n_count(fname_001):
   if fname_001
   return True
   
 def rebuild_in_place(fname_001):
    ok,fname,count = get_rebuilding_fname_n_count(fname_001)
    if not ok:
      print("Error trying to rebuild large file: index parsing error")
      return
    for i in range(2, count):
      chunk_fname= fname + ".%03d"%i
      append_ith_chunk(fname, chunk_fname)
    print ("done")
    
    