Python-written my misc. utilities
---------------------------------

slice.py
--------
Used to slice the big file on chunks and glue these files chunks back into original.
Main feature is low free space requirement on the disks: all operations are
performed in-place.
All 'slice' operations are in-place, i.e. they do not require more space, on current disk, then
 the biggest chunk size is

**Usage**: `slice (s|g|cut1) [chunk_size_Mb] <file>`
 where s|g is slice or glue-back operation:
   `s` *<chunk_size_Mb>* - slice <file> by <chunk_size_Mb> pieces, enumerated; 
        default *<chunk_size_Mb>* value is 2048, i.e. 2Gb
   `g` - reglue back sliced chunks into original file, <file> here should be first chunk filename
        i.e. it should look like 'file.7z.001'
   `cut1` *<chunk_size_Mb>* - cut off one piece with specified size from the end of <file>; 
      for manual operations.
      Use cut1 to cut big file on two in place.

maxlenzero.py
-------------
Use this to create zero-filled file with maxial size on the disk. 
Useful for minimizing compressed drive image size.

### .md-markup testing zone:
README.md Heading-1
===================

Sub-heading-2
-------------
 
### Another deeper heading
 
Paragraphs are separated
by a blank line.

Leave 2 spaces at the end of a line to do a  
line break

Text attributes *italic*, **bold**, 
`monospace`, ~~strikethrough~~ .

The [Markdown language](https://en.wikipedia.org/wiki/Markdown).
