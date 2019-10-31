# python wrapper for ffmpeg audio conversion

#input: list of folders to convert

#output: converted files in "converted" folder or in specified output folder (if provided)

import sys
from os import listdir,system,mkdir # ().: listdir;  ().path.: dirname,splitext,join,isfile,abspath
from os.path import dirname,splitext,join,isfile,abspath
import glob
from shutil import copy2
#import subprocess and use instead of os.system? Not sure -- I don't need any output or anything

def folder_convert(folder_list,out_path=None):
	#I think I should actually change this to only work on one folder -- then my "out_path" troubles would be easier

	# cases
	extensions_to_convert=('flac','raw','ogg','mpc','webm')
	extensions_to_keep=('mp3','wav','m4a','aiff') # keeping formats commonly supported by cd burners

	for folder in folder_list:
		
		folder=abspath(folder)

		if out_path:
			out_folder=out_path
			mkdir(out_folder)
		else: 
			out_folder=folder

		for file in listdir(folder):
			if isfile(join(folder,file)) and '.' in file:
				print(file)
				base_fn,ext=file.rsplit('.',1)
				if ext in extensions_to_convert:
					command='ffmpeg -i "%s" "%s"' % (join(folder,base_fn+'.'+ext),join(out_folder,base_fn+'.wav'))
					system(command) #relevant files converted to wav

				elif ext in extensions_to_keep:
					# copy the files to the output folder
					copy2(join(folder,base_fn+'.'+ext),join(out_folder,base_fn+'.'+ext))

if __name__ == "__main__":
	import argparse
	parser=argparse.ArgumentParser()
	parser.add_argument('folders',nargs='+',help='One or more folders containing audio files to convert')
	parser.add_argument('-o',dest='out_path',metavar='out_path',default=None,help='Optional out path for "converted" folder')
	args=parser.parse_args()
	print(args.out_path)
	folder_convert(args.folders,args.out_path)
