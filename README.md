Misc. utilities written on Python
---------------------------------

slice.py
--------
Used to slice the big file on chunks and glue these files chunks back into original.
Main feature is low free space requirement on the disks: all operations are
performed in-place.  
All 'slice' operations are in-place, i.e. they do not require more space, on current disk, then
 the biggest chunk size is.

	Usage: slice (s|g|cut1) [chunk_size_Mb] <file>  
	 where s|g is slice or glue-back operation:  
	   s <chunk_size_Mb> - slice <file> by <chunk_size_Mb> pieces, enumerated;  
	        default *<chunk_size_Mb>* value is 2048, i.e. 2Gb  
	   g - reglue back sliced chunks into original file, <file> here should be first chunk filename  
	        i.e. it should look like 'file.7z.001'  
	   cut1 <chunk_size_Mb> - cut off one piece with specified size from the end of <file>;  
	      for manual operations.  
	      Use cut1 to cut big file on two in place.  

maxlenzero.py
-------------
Use this to create zero-filled file with maxmial size on the C: (or D:, etc) disk.  
Useful for minimizing compressed drive image size.  
It creates such file, named '0.txt', after uou delete it and resulting drive image will be  
smaller on the size of free space of operated drive.

ppi.py
------
Compare 'ppi' feature, i.e. pixels-per-inch, also called 
[pixel density](https://en.wikipedia.org/wiki/Pixel_density), for diverse variety of devices: monitors, tablet and smartphone screens, ebook screens, etc. Uses very simple formula. Information 
gathered in one place allowing easy comparison of all these devices.
Original version is from 2012 or 2013.

netcat.py
---------
Copy file to another computer, netcat/nc utility of *unix implemented on Python,  
allowing it to run in any OS, particularly Windows-client and Windows-server.  
Can also be used to copy virtual machine images from inside to outside, i.e. to host machine,  
After that it can be compressed and sent further.  
Original version is from 2005.  
Usage samples for FreeBSD are in file "netcat.py_usage.txt".

