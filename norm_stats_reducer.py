#!/usr/bin/env python
from __future__ import print_function
import sys
import numpy as np

nchan = 19
nfft = 256
wlen=int((nfft/2)+1)

ch_list=['Fp1-A2','Fp2-A2','F7-A2','F3-A2','Fpz-A2','F4-A2','F8-A2','T3-A2','C3-A2','Cz-A2','C4-A2','T4-A2','T5-A2','P3-A2','Pz-A2','P4-A2','T6-A2','O1-A2','O2-A2']
ch_list = np.array(ch_list)

def read_mapper_output(file,separator=';'):
    for line in file:
        yield line.rstrip().split(separator)

def main(separator=';'):
    # input comes from STDIN (standard input)
    # key = [source file name, window #, channel name, sleep stage]
    # value = signal amplitude over time
    # package 'CustomMultiOutputFormat.java' to output to different directories
    # based on the first element of the key
    data = read_mapper_output(sys.stdin,separator)
    ch_max = ch_min = ch_mean = ch_std = 0
    cur_ch = None
    count = 0
    for line in data:
	if len(line) != 2:
		continue
        ch_name,stats = line
        this_max,this_min,this_mean,this_std = stats.split(',')
        this_max = float(this_max)
        this_min = float(this_min)
        this_mean = float(this_mean)
        this_std = float(this_std)
        if cur_ch != ch_name:
            if count != 0:
                s = '%s%s%s,%s,%s,%s' % (cur_ch,separator,str(ch_max),str(ch_min),str(ch_mean),str(ch_std))
                print(s)
            ch_max = this_max
            ch_min = this_min
            ch_mean = ch_std = 0
            cur_ch = ch_name
            count = 1
        else:
            count += 1
            ch_max = np.max([ch_max,this_max])
            ch_min = np.min([ch_min,this_min])
        ch_mean = ((count-1)*ch_mean + this_mean)/count
        ch_std = ((count-1)*ch_std + this_std)/count
    s = '%s%s%s,%s,%s,%s' % (cur_ch,separator,str(ch_max),str(ch_min),str(ch_mean),str(ch_std))
    print(s)


if __name__ == "__main__":
    main()
