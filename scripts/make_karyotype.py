#! /usr/bin/env python
# coding: utf8
#
# Copyright 2019-2020 Michaël Bekaert. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
import argparse
import os
from Bio import SeqIO
import re


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--fasta', '-f', '-i', dest='fasta', type=str, required=True, help='Path to the genome (FASTA format)')
    parser.add_argument('--circos', dest='circos', action='store_true', help='Format for CIRCOS rather than BED format')
    args = parser.parse_args()

    if args.fasta is None or os.path.exists(args.fasta) is False:
        parser.print_help()
        exit(1)

    with open(args.fasta, 'r') as handle:
        count = 0
        relg = re.compile("\Wlg(\w+)", re.IGNORECASE)
        rechr = re.compile("\Wchr(\w+)", re.IGNORECASE)
        for record in SeqIO.parse(handle, 'fasta'):
            count += 1
            name = None

            result = relg.findall(record.id)
            if result:
                name = 'LG' + result[0]
            else:
                result = rechr.findall(record.id)
                if result:
                    name = 'Chr' + result[0]
                else:
                    result = relg.findall(record.description)
                    if result:
                        name = 'LG' + result[0]
                    else:
                        result = rechr.findall(record.description)
                        if result:
                            name = 'Chr' + result[0]
            if args.circos:
                print('chr - ' + record.id + ' ' + (name if name is not None else str(count)) + ' 1 ' + str(len(record.seq)) + '\n', end='')
            else:
                print(record.id + '\t0\t' + str(len(record.seq) - 1) + '\t' + (name if name is not None else str(count)) + '\n', end='')


if __name__ == '__main__':
    main()
