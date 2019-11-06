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
			if not exists(out_folder): #no need to worry about race condition since there is probably not another process making this
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

def match_audio_to_power_histogram(args):
	pass

#def apply_audio_compression(mtype,movie,movie_out):
#temporarily using the line below for debugging
def apply_audio_compression(args):
	#basically just call ffmpeg and "compand" based on which movie audio power contour type was selected
	# if none has been selected, do the default/"secret recipe"

	#debugging
	mtype=args.mtype
	movie=args.movie
	movie_out=args.movie_out

	#horror_transfer=
	#comedy_transfer=
	#drama_transfer=
	default_transfer='compand=0 0:1 1:-90/-900 -70/-70 -30/-9 0/-3:6:0:0:0'

	#mt2c_in={None:default_transfer,'horror':horror_transfer,'comedy':comedy_transfer,'drama':drama_transfer}
	mt2c_in={None:default_transfer}
	compand_inputs=mt2c_in[mtype]

	command='ffmpeg -i "%s" -af "aformat=channel_layouts=stereo, compand=0 0:1 1:-90/-900 -70/-70 -30/-9 0/-3:6:0:0:0" "%s"' % (movie,movie_out) # this works for video or audio file, right?
	system(command)




if __name__ == "__main__":

	#parsers
	parser=argparse.ArgumentParser()
	subparsers=parser.add_subparsers()

	#subparser "toCD" for folder_convert
	cd_conv_parser=subparsers.add_parser('toCD')
	cd_conv_parser.add_argument('folders',nargs='+',help='One or more folders containing audio files to convert')
	cd_conv_parser.add_argument('-o',dest='out_path',metavar='out_path',default=None,help='Optional out path for "converted" folder')
	cd_conv_parser.set_defaults(func=folder_convert)

	#subparser "compress" for match_audio_to_power_histogram
	compress_parser=subparsers.add_parser('compress')
	compress_parser.add_argument('movie',help='A movie file for which to compress audio')
	compress_parser.add_argument('movie_out',help='Optional out path for "converted" folder')
	compress_parser.add_argument('-type',dest='mtype',type=str,default=None,help='User specified type -- if given, skips matching algo')

	#compress_parser.set_defaults(func=match_audio_to_power_histogram)
	#temporarily using the line below for debugging
	compress_parser.set_defaults(func=apply_audio_compression)



	args=parser.parse_args()
	#for debugging:
		#args=parser.parse_args(input.split())
		# self.args=args
	args.func(args)
