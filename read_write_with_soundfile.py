song_fn='/Users/chloeteichman/Soulseek Downloads/complete/fallCD/converted_CD2/justwav/04 Dead Pontoon.wav'

import soundfile as sf
import numpy as np

data, sample = sf.read(song_fn)

# method 1
bdata=sf.blocks(song_fn,blocksize=sample) #grab data in chunks of 1 second
rms=[np.sqrt(np.mean(block**2)) for block in bdata]

# method 2
bdata=[]
rms=[]
for block in sf.blocks(song_fn,blocksize=sample):
	bdata.append(block)
	rms.append(np.sqrt(np.mean(block**2)))

#end methods


normbdata=[d*min(1/rmss,15) for d,rmss in zip(bdata,rms)]
chonk=np.concatenate(normbdata)
sf.write('/Users/chloeteichman/Soulseek Downloads/complete/fallCD/converted_CD2/justwav/04 Dead Pontoon no op.wav', chonk,44100)

