#! /usr/bin/env python
# Copyright 2014 Uri Laserson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import argparse

from Bio import SeqIO

argparser = argparse.ArgumentParser(description=None)
argparser.add_argument('-i','--input',required=True)
argparser.add_argument('-o','--output',required=True)
argparser.add_argument('-p','--packetsize',type=int,required=True)
args = argparser.parse_args()

input_filename = args.input
output_dir = os.path.abspath(args.output)
os.makedirs(output_dir,mode=0755)
packetsize = args.packetsize

num_processed = 0
file_num = 1
outfilename = os.path.join(output_dir,'part.%s.fastq' % file_num)
for record in SeqIO.parse(input_filename,'fastq'):
    if num_processed == 0:
        op = open(outfilename,'w')
    
    op.write(record.format('fastq'))
    num_processed += 1
    
    if num_processed == packetsize:
        op.close()
        num_processed = 0
        file_num += 1
        outfilename = os.path.join(output_dir,'part.%s.fastq' % file_num)

if not op.closed:
    op.close()
