#!/usr/bin/env python
import os
from os import path
import subprocess

def updateDatasetsConfig(configFile, samplePath, sampleName):
    configFormat = '[datasets.{sample}]\nurl = ?data={path}\nname = {sample}\n\n'
    with open(configFile, 'a') as datasetsConfig:
        datasetsConfig.write(configFormat.format(path = samplePath, sample = sampleName))

def updateTracksConfig(configFile, sampleName, append):
    configFormat = '[general]\ndataset_id = {sample}\n\n'
    with open(configFile, 'a' if append else 'wb') as tracksConfig:
        tracksConfig.write(configFormat.format(sample = sampleName))
    
def main(args):
    datasetsConfig = path.join(args.topdir, 'datasets.conf')
    if not args.append and path.exists(datasetsConfig):
        os.remove(datasetsConfig)
    for dirpath, dirnames, filenames in os.walk(args.topdir):
        # Sort the subdirectory names in-place.
        dirnames.sort()
        if 'seq' in dirnames:
            sampleName = path.basename(dirpath)
            print 'Updating configs for %s...'%sampleName
            updateDatasetsConfig(datasetsConfig, path.relpath(dirpath, path.dirname(args.topdir)), sampleName)
            updateTracksConfig(path.join(dirpath, 'tracks.conf'), sampleName, args.append)
            subprocess.call(['chmod', 'a+rw', path.join(dirpath, 'tracks.conf')])
            print 'Done.'
    subprocess.call(['chmod', 'a+rw', datasetsConfig])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Enable dataset selection for a JBrowse data directory.')
    parser.add_argument('topdir', metavar = 'PATH', nargs = '?', default = '/data/VirtualHost/gbrowse2017a/html/hp/JBrowse-1.12.1/chromosomes_data', help = 'Directory containing all the data.')
    parser.add_argument('--append', action = 'store_true', help = 'Flag for appending to the existing config files. They will be overwritten by default.')

    main(parser.parse_args())
