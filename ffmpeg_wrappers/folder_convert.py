# python wrapper for ffmpeg audio conversion

#input: list of folders to convert

#output: converted files in "converted" folder or in specified output folder (if provided)

import sys
from os import listdir,system,mkdir 
from os.path import dirname,splitext,join,isfile,abspath,exists
import glob
from shutil import copy2
import argparse
import errno

def folder_convert(args):
	
	folders=args.folders
	out_path=args.out_path if hasattr(args,'out_path') else None
	# cases
	extensions_to_convert=('flac','raw','ogg','mpc','webm')
	extensions_to_keep=('mp3','wav','m4a','aiff') # keeping formats commonly supported by cd burners

	for folder in folders:
		#folder=abspath(folder) # don't think this is actually necessary 
		if out_path:
			out_folder=out_path
			if !exists(out_folder): #no need to worry about race condition since there is probably not another process making this
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

# def compress_movie_audio():

if __name__ == "__main__":
	#parsers
	parser=argparse.ArgumentParser()
	subparsers=parser.add_subparsers()
	cd_conv_parser=subparsers.add_parser('toCD')
	cd_conv_parser.add_argument('folders',nargs='+',help='One or more folders containing audio files to convert')
	cd_conv_parser.add_argument('-o',dest='out_path',metavar='out_path',default=None,help='Optional out path for "converted" folder')
	cd_conv_parser.set_defaults(func=folder_convert)

	#movie_comp_parser=subparsers.add_parser('compressMovie')

	args=parser.parse_args()
	#for debugging:
		#args=parser.parse_args(input.split())
		# self.args=args
	args.func(args)
