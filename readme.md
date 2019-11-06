# Audio Stuff
Available: conversion of folders to CD format and dynamic range compression of audio
Coming soon: Algorithm for matching movie to genre based on histogram of sound amplitude and fine tuned DRCompression based on genre

# Current usage:
`folder_convert.py [-h] {toCD,compress} ...`

- Function 1
```
folder_convert.py toCD [-h] [-o out_path] folders [folders ...]

positional arguments:
folders  One or more folders containing audio files to convert

optional arguments:
-h, --help show this help message and exit
-o out_path  Out path for "converted" folder
```

- Function 2
```
folder_convert.py compress [-h] [-type MTYPE] movie movie_out

positional arguments:
movie  A movie file for which to compress audio
movie_out  Optional out path for "converted" folder

optional arguments:
-h, --help show this help message and exit
-type MTYPE  User specified type -- if given, skips matching algo. As code is unfinished, only 'None' works for general whisper/scream compression
```
