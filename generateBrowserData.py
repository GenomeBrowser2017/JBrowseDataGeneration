#!/usr/bin/env python
import glob
import os
from os import path
import shutil
import subprocess
import sys

prepare_refseqs = 'prepare-refseqs.pl'
flatfile_to_json = 'flatfile-to-json.pl'
generate_names = 'generate-names.pl'

# Prepares reference sequence from scaffolds.fasta file.
def prepareReferenceSequence(dataDir, outDir, config):
    print 'Preparing reference sequence...' 
    prepareOptions = ['--fasta', path.join(dataDir, 'scaffolds.fasta'), '--out', outDir]
    configOptions = list(sum((('--%s'%key, value) for key, value in config.get('scaffolds.fasta', {}).iteritems()), ()))
    p = subprocess.Popen([prepare_refseqs] + prepareOptions + configOptions, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = p.communicate()
    sys.stdout.write(out)
    sys.stderr.write(err)
    print 'Done.'

# Generates tracks for all the GFF files in the data directory.
def generateTracks(dataDir, outDir, config):
    commonOptions = ['--trackType', 'CanvasFeatures', '--out', outDir]
    for trackFile in glob.glob(path.join(dataDir, '*.gff')):
        trackLabel = path.splitext(path.basename(trackFile))[0]
        print 'Generating %s track...'%trackLabel
        trackOptions = ['--gff', trackFile, '--trackLabel', trackLabel]
        configOptions = list(sum((('--%s'%key, value) for key, value in config.get(path.basename(trackFile), {}).iteritems()), ()))
        p = subprocess.Popen([flatfile_to_json] + trackOptions + commonOptions + configOptions, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        out, err = p.communicate()
        sys.stdout.write(out)
        sys.stderr.write(err)
        print 'Done.'

# Generates names for autocomplete functionality.
def generateNames(outDir):
    print 'Generating names...'
    p = subprocess.Popen([generate_names, '--out', outDir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = p.communicate()
    sys.stdout.write(out)
    sys.stderr.write(err)
    print 'Done.'

# Generates data for loading into JBrowse from FASTA and GFF files.
def generateData(dataDir, outDir, config):
    if path.exists(outDir):
        shutil.rmtree(outDir)
    prepareReferenceSequence(dataDir, outDir, config) 
    generateTracks(dataDir, outDir, config)
    generateNames(outDir)
    # XXX: Following is a hack.
    os.remove(path.join(outDir, '.htaccess'))
    # Make the generated data readable and writable by everyone.
    subprocess.call(['chmod', 'a+rw', outDir, '-R'])

# Main function.
def main(args):
    global prepare_refseqs, flatfile_to_json, generate_names
    prepare_refseqs = path.join(args.jbrowse, 'bin', 'prepare-refseqs.pl')
    flatfile_to_json = path.join(args.jbrowse, 'bin', 'flatfile-to-json.pl')
    generate_names = path.join(args.jbrowse, 'bin', 'generate-names.pl')
    config = {}
    if args.config:
        import json
        with open(args.config, 'rb') as fp:
            config.update(json.load(fp))
    for sample in args.samples:
        sampleName = 'OB%04d'%sample
        print 'Generating data for %s...'%sampleName
        generateData(path.join(args.datadir, sampleName), path.join(args.outdir, sampleName), config)
        print 'Done.'
        if path.exists(path.join(args.datadir, sampleName, 'plasmids', 'scaffolds.fasta')):
            print 'Generating data for %s...'%os.path.join(sampleName, 'plasmids')
            generateData(path.join(args.datadir, sampleName, 'plasmids'), path.join(args.outdir, sampleName + '_plasmids'), config)
            print 'Done.'

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate JBrowse data from raw data.')
    parser.add_argument('--samples', metavar = 'ID', nargs = '+', default = range(1, 25), type = int, help = 'Identifier of the samples to be generated. Generates data for all the samples by default.')
    parser.add_argument('--jbrowse', metavar = 'PATH', nargs = '?', default = '/data/VirtualHost/gbrowse2017a/html/hp/JBrowse-1.12.1', help = 'Directory containing JBrowse installation.')
    parser.add_argument('--datadir', metavar = 'PATH', nargs = '?', default = '/data/VirtualHost/gbrowse2017a/html/data_groups', help = 'Directory containing raw data files.')
    parser.add_argument('--outdir', metavar = 'PATH', nargs = '?', default = '/data/VirtualHost/gbrowse2017a/html/data', help = 'Directory to which converted files will be written.')
    parser.add_argument('--config', metavar = 'FILE', nargs = '?', default = 'generate_jbrowse.conf', help = 'JSON config file used for generating JBrowse data.')

    main(parser.parse_args())
