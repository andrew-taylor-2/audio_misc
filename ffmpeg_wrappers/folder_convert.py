# python wrapper for ffmpeg audio conversion

#input: list of folders to convert

#output: converted files in "converted" folder or in specified output folder (if provided)

import sys
#from os import listdir # ().: listdir;  ().path.: dirname,splitext,join,isfile,abspath
#from os.path import dirname,splitext,join,isfile,abspath
import glob
from shutil import copy2
#import subprocess and use instead of os.system? Not sure -- I don't need any output or anything

def folder_convert(folder_list,out_path=None):
	#I think I should actually change this to only work on one folder -- then my "out_path" troubles would be easier

	# cases
	extensions_to_convert=('flac','raw','ogg','mpc','webm')
	extensions_to_keep=('mp3','wav','m4a','aiff') # keeping formats commonly supported by cd burners

	#handle out_path
	if out_path:


	for folder in folder_list:
		folder=os.path.abspath(folder)
		files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))] #hmm I like the more object oriented approach where each of the folder contents has an isFolder attribute; might want a new library

		#categorize files method 1
		#files_to_convert=[f for f in files if os.path.splitext(f)[1:] in extensions_to_convert] # a normal loop here might be more conservative of resources
		#files_to_keep=[f for f in files if os.path.splitext(f)[1:] in extensions_to_keep]

		#categorize files method 2
		#files=filter(lambda x: x.endswith,files)
		#files_to_convert.append(f) for f in files if os.path.splitext(f)[1:] in extensions_to_convert else files_to_keep.append(f)

		files_to_convert=[]
		files_to_keep=[]

		#categorize files method 3
		for f in files:
			base_fn=os.path.splitext(f)[1:]
			if base_fn in extensions_to_convert:
				#files_to_convert.append(f) # do I even need to put them in an array
				os.system('ffmpeg -i ' + base_fn)
			if base_fn in extensions_to_keep:
				files_to_keep.append(f)

		# different way
		out_folder=out_path if out_path else folder # this was previously within file loop, hopefully I'm not missing something
		for base_fn,ext in files.rsplit('.',1) if '.' in files else (files,''):
			if ext in extensions_to_convert:
				#files_to_convert.append(f) # do I even need to put them in an array

				#out_folder=out_path if out_path else folder	# this is pretty dumb. if i change this function to work on a single folder, I think it'll make more sense

				command=f'ffmpeg -i %s %s'
				% (os.path.join(folder,base_fn+'.'+ext),
				   os.path.join(out_folder,base_fn+'.wav')

				os.system(command)#relevant files converted to wav


			elif ext in extensions_to_keep:
				#files_to_keep.append(f)
				# copy the files to the output folder if given
				# I should add a
				copy2(os.path.join(folder,base_fn+'.'+ext),os.path.join(out_folder,base_fn+'.'+ext))

			#else: do nothing to other types of files



		#convert files
		# wrap a call to ffmpeg
		# NOTE: I could actually just put this in the earlier loop
		for f2c in files_to_convert:
			os.system('ffmpeg -i ' + f2c)

		#both types
		# copy to outdir or make "converted" dir


if __name__ == "__main__":
	import argparse
	parser=argparse.ArgumentParser()
	parser.add_argument('folders',nargs='+',help='One or more folders containing audio files to convert')
	parser.add_argument('-o',nargs=1,metavar='out_path',default=None,help='Optional out path for "converted" folder')
	args=parser.parse_args()
	#folder_convert(args.folders,args.out_path)
	print(args.folders)
	if args.o:
		print(args.o)
