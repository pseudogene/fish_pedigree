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


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--vcf', '-i', dest='vcf', type=str, required=True, help='Path to the VCF file aligned with the reference genome')
    args = parser.parse_args()

    if args.vcf is None or os.path.exists(args.vcf) is False:
        parser.print_help()
        exit(1)

    with open(args.vcf, 'r') as handle:
        maxpos = None
        minpos = None
        lastchr = None
        tmpchr = list()
        print('#CHROM\tPOS\tGMAP\tSNP_ID\n', end='')

        for line in handle:
            if not line.startswith('#'):
                line.rstrip()
                tab = line[:-1].split('\t')
                if len(tab) > 3 and int(tab[1]) > 0:
                    if lastchr is not None and lastchr != tab[0]:
                        if len(tmpchr) > 1:
                            for val in tmpchr:
                                print(val[0] + '\t' + str(val[1]) + '\t' + str("%.3f" % float((val[1]-minpos)/(maxpos-minpos)*100)) + '\t' + val[2] + '\n', end='')
                        tmpchr = list()
                        minpos = maxpos = int(tab[1])
                    tmpchr.append([tab[0], int(tab[1]), tab[2]])
                    if maxpos is None or maxpos < int(tab[1]):
                        maxpos = int(tab[1])
                    if minpos is None or minpos > int(tab[1]):
                        minpos = int(tab[1])
                    lastchr = tab[0]
        if lastchr is not None and len(tmpchr) > 1:
            for val in tmpchr:
                print(val[0] + '\t' + str(val[1]) + '\t' + str("%.3f" % float((val[1]-minpos)/(maxpos-minpos)*100)) + '\t' + val[2] + '\n', end='')


if __name__ == '__main__':
    main()
