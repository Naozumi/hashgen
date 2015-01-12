from Tkinter import *
import tkMessageBox
from functools import partial
import os
import sys
import hashlib
import gzip

class niUpdater:
	def __init__(self, parent):
		self.myParent = parent
		self.topContainer = Frame(parent)
		self.topContainer.pack(side=TOP, expand=1, fill=X, anchor=NW)
		self.btmContainer = Frame(parent)
		self.btmContainer.pack(side=BOTTOM, expand=1, fill=X, anchor=NW)

		path = StringVar()
		ver = StringVar()
		path.set(myloc + "\\NordInvasion")
		ver.set("0.4.9")
		entry1 = Entry(self.topContainer, textvariable=path)
		entry1.pack(side=LEFT, expand=1, fill=X)
		entry2 = Entry(self.topContainer, textvariable=ver, width =7)
		entry2.pack(side=LEFT, expand=0)

		#------------------ BUTTON #1 ------------------------------------
		button_name = "OK"

		# command binding
		var = StringVar()
		self.button1 = Button(self.topContainer, command=lambda: self.buttonPress(entry1.get(),var,entry2.get()))
		

		# event binding -- passing the event as an argument
		self.button1.bind("<Return>",
			lambda
			event :
			self.buttonHandler_a(entry1.get(),var)
		)

		self.button1.configure(text=button_name, width=5)
		self.button1.pack(side=LEFT)
		self.button1.focus_force()  # Put keyboard focus on button1
		
		self.label = Label(self.btmContainer,textvariable=var, width=55, anchor=W, justify=LEFT)
		self.label.pack(side=LEFT, expand=1, fill=X)
		var.set("Press OK to start")
			
				
	def writeOut(self,dir,hashfile,toplevel,var,folder):
		""" walks a directory, and executes a callback on each file """
		dir = os.path.abspath(dir)
		for file in [file for file in os.listdir(dir) if not file in [".",".."]]:
			nfile = os.path.join(dir,file)
			if os.path.isdir(nfile): # is a directory
				hashfile.write("F::"+nfile.replace(toplevel,"") + "\n")
				hashfile.write("X::\n")
				var.set("Generating... " + "F::"+nfile.replace(toplevel,""))
				root.update()
				if not os.path.exists(folder + '\\' + nfile.replace(toplevel,"")):
					os.mkdir(folder + '\\' + nfile.replace(toplevel,""))

				self.writeOut(nfile,hashfile,toplevel,var,folder)
			else: # is a file
				# Generate the hash and add to hash file
				h=(hashlib.sha1(open(nfile, 'rb').read()).hexdigest())
				hashfile.write(nfile.replace(toplevel,"") + "\n")
				var.set("Generating... " + nfile.replace(toplevel,""))
				root.update()
				hashfile.write(h + "\n")

				# Generate a smaller, gzipped version of the file
				with open(nfile, 'rb') as f_in:
					with gzip.open(folder + '\\' + nfile.replace(toplevel,"") + '.gz', 'wb') as f_out:
						f_out.writelines(f_in)


	def buttonPress(self, path, var, versionNumber):
		self.button1.configure(state=DISABLED)
		import time
		timestamp = int(time.time())
		folderName = (myloc + '\\ni-mod-' + str(timestamp))
		if not os.path.exists(folderName):
			os.mkdir(folderName)
		file = open(myloc + '\\hash.txt','wt')
		file.write("V::1\n")
		file.write("W::http://nordinvasion.com/mod/" + str(versionNumber) + "/\n")
		self.writeOut(path,file,path+'\\',var,folderName)
		file.close()
		var.set("File Generated")
		tkMessageBox.showinfo("NI Hash Gen", "Hash file generated successfully.")
		self.button1.configure(state=NORMAL)

	def buttonHandler_a(self, path, var):
		self.buttonPress(path, var)

pathname = os.path.dirname(sys.argv[0])
myloc = os.path.abspath(pathname)
root = Tk()
niup = niUpdater(root)
root.wm_title("Nord Invasion Hash Generator")
root.mainloop()
