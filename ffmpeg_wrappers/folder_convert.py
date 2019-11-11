# python wrapper for ffmpeg audio conversion

#input: list of folders to convert

#output: converted files in "converted" folder or in specified output folder (if provided)

import sys
from os import listdir,system,mkdir
from os.path import dirname,splitext,join,isfile,abspath,exists
import subprocess as sp
import glob
from shutil import copy2
import argparse
import errno
import numpy as np

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
	#first I gotta get the audio from the videos
	# for some reason it was hard to find good tools for this so regrettably I think I'm gonna have to get ffmpeg to write an audio file then sample that


	#I can write input sanitizing later
	command='ffmpeg -i "%s" \
	# -ab 45k # audio bitrate: very low (like a bad quality phone call) # Im not using this anymore
	-f flac \ # we want just the raw data
	-sample_fmt s16
	-ac 1 \ # just one audio channel
	-ar 5k \ # well be disregarding very high frequencies -- hope this doesnt come back to bite us
	-vn \ # we dont need video stream
	 pipe:' \ #send output to stdout
	 % args.movie # input

	 p=sp.Popen(command,stdout=sp.PIPE,stderr=sp.PIPE,shell=True) #keep env variables i.e. use PATH to find ffmpeg (or hash table)
	 pout,perr=p.communicate() # get standard out and error from subprocess
	 # I need to test to make sure pout isn't too large

	 #get as numpy array
	 datagen=sf.blocks(io.BytesIO(pout),blocksize=5000) # need to provide this metadata bc the raw format doesn't. Getting audio blocks of one second
	rms=[] 
	for block in datagen: #get rms power
		try:
			rms.append(np.sqrt(np.mean(block**2)))
		except RuntimeError: # This probably isnt that safe, but I get a seek error on the last block...
			pass
	 #hooray, I have the rms.
	 # optionally scale power then get normalized correlation or something like that with audio genre priors


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

	command='ffmpeg -i "%s" -af "aformat=channel_layouts=stereo%s" "%s"' % (movie,', '+compand_inputs,movie_out) # this works for video or audio file, right?
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
	compress_parser.add_argument('movie_out',help='Out path for "converted" folder')
	compress_parser.add_argument('-type',dest='mtype',type=str,default=None,help='User specified type -- if given, skips matching algo. As code is unfinished, only <None> works for general whisper/scream compression')

	#compress_parser.set_defaults(func=match_audio_to_power_histogram)
	#temporarily using the line below for debugging
	compress_parser.set_defaults(func=apply_audio_compression)



	args=parser.parse_args()
	#for debugging:
		#args=parser.parse_args(input.split())
		# self.args=args
	args.func(args)
