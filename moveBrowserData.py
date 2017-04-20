#!/usr/bin/env python
import os
from os import path
import shutil
import subprocess

def moveSampleData(source, target):
    if path.exists(source):
        print "Moving %s to %s..."%(source, target)
        if path.exists(target):
            shutil.rmtree(target)
        shutil.move(source, target)
        print 'Done.'

def moveBrowserData(samples, sourceDir, chromosomesDir, plasmidDir):
    for sample in xrange(1, 25): 
        sampleName = 'OB%04d'%sample
        moveSampleData(path.join(sourceDir, sampleName), path.join(chromosomesDir, sampleName))

        plasmidName = 'OB%04d_plasmids'%sample
        moveSampleData(path.join(sourceDir, plasmidName), path.join(plasmidDir, sampleName))

def main(args):
    moveBrowserData(args.samples, args.source, args.chromosomes, args.plasmid)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate JBrowse data from raw data.')
    parser.add_argument('--samples', metavar = 'ID', nargs = '+', default = range(1, 25), type = int, help = 'Identifier of the samples to be moved. Moves data for all the samples by default.')
    parser.add_argument('--source', metavar = 'PATH', nargs = '?', default = '/data/VirtualHost/gbrowse2017a/html/data', help = 'Directory from which data is to be moved.')
    parser.add_argument('--chromosomes', metavar = 'PATH', nargs = '?', default = '/data/VirtualHost/gbrowse2017a/html/hp/JBrowse-1.12.1/chromosomes_data', help = 'Directory containing chromosomes data.')
    parser.add_argument('--plasmid', metavar = 'PATH', nargs = '?', default = '/data/VirtualHost/gbrowse2017a/html/hp/JBrowse-1.12.1/plasmid_data', help = 'Directory containing plasmid data.')

    main(parser.parse_args())
