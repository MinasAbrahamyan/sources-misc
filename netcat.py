#!/usr/bin/env python
""" netcat.py - Copy data between files and/or tcp network sockets
  Author: Minas Abrahamyan
  Edition dates: this is version of 2005.07.14 /copied to new comp 2009.03.16/
   unedited since then
  
 Input and output files specified open file on read or write accordingly
 Input for network data opens server socket and listens on it
 Output for network data creates client socket and sends data
 Sample Usage:
 Client:
  # tar czf - /usr/X11R6 |/root/netcopy/netcat.py -o ce:3000 -p 1024000
 Server:
  C:\> python netcat.py -i ce:3000 -o x11r6.tgz -p1024000
"""
import sys,socket,getopt

class Data:
	"Abstract data"
	NONE,FILE,SOCKET=0,1,2
	INPUT,OUTPUT=1,2
	CHUNKSIZE=512
	def __init__(self):
		self.type=Data.NONE
		self.dirc=Data.NONE  # direction
	def open(self):
		raise Exception,'Unimplemented method'
	def close(self):
		raise Exception,'Unimplemented method'
	def read(self, size=-1):
		"return read data buffer"
		raise Exception,'Unimplemented method'
	def write(self, buffer):
		"write buffer ti Data object"
		raise Exception,'Unimplemented method'
	def eof(self):
		"returns bool - is end of file condition?"
		raise Exception,'Unimplemented method'

class FileData(Data):
	"File data"
	def __init__(self,fname):
		Data.__init__(self)
		self.type=Data.FILE
		self.fname=fname
		self.__file=None
		self.lastread=-1
	def open(self):
		if   self.fname=='stdin': 
			self.__file= sys.stdin; return
		if self.fname=='stdout':
			self.__file= sys.stdout; return
		if   self.dirc==Data.INPUT:
			mode='rb'
		elif self.dirc==Data.OUTPUT:
			mode='wb'    
		self.__file= open(self.fname,mode)
	def close(self):
		#if self.fname!='stdin' and 
		#   self.fname!='stdout':
		self.__file.close()
	def read(self, size=-1):
		"return read data buffer"
		buf= self.__file.read(size)
		self.lastread= len(buf)
		return buf
	def write(self, buffer):
		"write buffer ti Data object"
		self.__file.write(buffer)
	def eof(self):
		"returns bool - is end of file condition?"
		assert self.dirc!=Data.NONE
		if self.dirc==Data.INPUT:
			return self.lastread==0  # are there eof()-like exist?
		return False

class SocketData(Data):
	"TCP socket data"
	def __init__(self,sockaddress):
		Data.__init__(self)
		self.type=Data.SOCKET
		self.addr=sockaddress
		self.s=None #socket
		self.lastread=-1
	def open(self):
		raise Exception,'Unimplemented method'
	def close(self):
		raise Exception,'Unimplemented method'
	def read(self, size=-1):
		"return read data buffer"
		buf=self.s.recv(size)
		self.lastread=len(buf)
		return buf
	def write(self, buffer):
		"write buffer ti Data object"
		self.s.send(buffer)
	def eof(self):
		"returns bool - is end of file condition?"
		assert self.dirc!=Data.NONE
		if self.dirc==Data.INPUT:
			return self.lastread==0
		if self.dirc==Data.OUTPUT:
			return False

class ClientSocketData(SocketData):
	"TCP socket data"
	def __init__(self,sockaddress):
		SocketData.__init__(self,sockaddress)
	def open(self):
		self.s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.connect(self.addr)
		#self.s.setblocking(True)
	def close(self):
		"close; disallow writing"
		self.s.shutdown(1)
		self.s.close()

class ServerSocketData(SocketData):
	"TCP socket data"
	def __init__(self,sockaddress):
		SocketData.__init__(self,sockaddress)
	def open(self):
		self.servsock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.servsock.bind(self.addr)
		self.servsock.listen(1)
		self.s,self.peer_addr= self.servsock.accept()
		#self.s.setblocking(True)
	def close(self):
		"close; disallow reading"
		self.s.shutdown(0)
		self.s.close()
		self.servsock.close()  #shutdown(2)

def copy(inp,outp,opt):
	"Copy data from in-data to out-data"
	progress= opt.get('progress',0)
	inp.open()
	outp.open()
	written=0
	while not inp.eof():
		buffer=inp.read(Data.CHUNKSIZE)
		outp.write(buffer)
		written+=len(buffer)
		if progress and written%progress==0:
			sys.stderr.write('#')
	inp.close()
	outp.close()
	print >>sys.stderr,"%s%d bytes written."%(progress and '\n' or '', written)
	
def main():
	inp,outp,opt = clarg_opts()
	copy(inp,outp,opt)

def usage():
	print """\
Usage: netcat.py [-i input] [-o output] [-p progress_bytes]
Where: 
 -i input - specifies input data file name or network address in form 
	 (ip|domainname):port. If not specified uses standart input stream
 -o output - specifies output data in -i switch format. If not specified 
	 uses standart output stream
 -p progress_bytes - if -p switch specified shows progress sign(#) at 
	 every progress_bytes of data get copied.
""" 
def clarg_opts():
	"Parse command line argument options and return "
	try:
		opts,s= getopt.getopt(sys.argv[1:],'i:o:p:')
	except getopt.GetoptError,e:
		print "Error: "+str(e)
		usage()
		sys.exit(1)
	inp,outp=None,None
	opt={}
	for o,a in opts:
		a=a.strip()
		if   o=='-i':
			if inp!=None: raise Exception,'Input is already specified'
			if a.find(':')!=-1:
				ip,port=a.split(':')
				port=int(port)
				inp=ServerSocketData((ip,port))
			else:
				inp=FileData(a)
			inp.dirc=Data.INPUT 
		elif o=='-o': 
			if outp!=None: raise Exception,'Output is already specified'
			if a.find(':')!=-1:
				ip,port=a.split(':')
				port=int(port)
				outp=ClientSocketData((ip,port))
			else:
				outp=FileData(a)
			outp.dirc=Data.OUTPUT
		elif o=='-p':
			if a=='': opt['progress']= 1024
			else:     opt['progress']= int(a)
	if inp==None and outp==None:
		usage(); sys.exit(2)
	if inp==None:  inp= FileData('stdin');  inp.dirc=Data.INPUT
	if outp==None: outp=FileData('stdout'); inp.dirc=Data.OUTPUT
	return (inp,outp,opt)

if __name__=='__main__':
	main()
