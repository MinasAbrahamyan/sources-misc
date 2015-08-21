#!env /usr/bin/python 
#maxlenzero.py - Create file with maximal size, spanning all available disk space. Data is all-zeros.
# Update: there exists another untested option, using truncate:
"""
with open("file-to-create", "wb") as out:
    out.truncate(1024 * 1024 * 1024)
#or
with open("file-to-create", "wb") as out:
    out.seek((1024 * 1024 * 1024) - 1)
    out.write('\0')
From URL: http://stackoverflow.com/questions/8816059/create-file-of-particular-size-in-python
NB question: Doesn't that generate a sparse file, though? (This may be what was needed, but it's not quite the same)
"""
import os,sys

def make_nMb_zero_file(filename, size):
  _1M_buf = "\0" * (1024*1024)
  f = open(filename, "wb")
  for i in range(0,size):
    f.write(_1M_buf)
  f.close()
  os.unlink(filename)

def make_maxzero_file(filename):
  _1M_buf = "\0" * (1024*1024)
  i=0
  try:
    f = open(filename, "wb")
    while True:
      f.write(_1M_buf)
      f.flush()
      sys.stderr.write("#")
      i+=1
      if i%100==0: # Report progress every 100Mb
        print "\n%s Mb"%i
      if False and i>127: #0/1===release/test, 127 = magic test no.
        print "\ntest break:i=%s Mb"%i #warn the user
        break #!
  except IOError:
   print "Error: can\'t write file"
   #-f.close()
   if 1:
     os.unlink(filename)
  else: #else-of-try == finally
   print "Operation finished successfully" #infinite cycle: never will be here
  print "\nTotal: Was written: %s Mb. Done!"%i

if __name__=='__main__':
  #make_nMb_zero_file("C:\\0.txt", 1)
  make_maxzero_file("C:/0.txt") # "./0.txt") 
