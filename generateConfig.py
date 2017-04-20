#!/usr/bin/env python
import json
from collections import defaultdict
import subprocess

trackKeys = {
    'scaffolds.fasta' : 'Reference sequence',
    'Genes.gff'       : 'Predicted Genes',
    'Card.gff'        : 'Card hits',
    'Doors.gff'       : 'Doors hits',
    'Lipop.gff'       : 'LipoP hits', 
    'Pilercr.gff'     : 'CRISPR hits', 
    'TMHMM.gff'       : 'TMHMM',
    'VFDB.gff'        : 'VFDB', 
}

trackColors = {
    'Genes.gff'   : 'red', 
    'Card.gff'    : 'blue', 
    'Doors.gff'   : 'yellow', 
    'Lipop.gff'   : 'yellow',  
    'Pilercr.gff' : 'yellow',  
    'TMHMM.gff'   : 'yellow',  
    'VFDB.gff'    : 'yellow',  
}


def generateConfig(configFile):
    configDict = defaultdict(dict)
    for fileName, label in trackKeys.iteritems():
        configDict[fileName]['key'] = label

    for fileName, color in trackColors.iteritems():
        configDict[fileName]['clientConfig'] = json.dumps({'color' : color})

    with open(configFile, 'wb') as fp:
        json.dump(configDict, fp)

def main(args):
    generateConfig(args.file)
    subprocess.call(['chmod', 'a+rw', args.file])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate JSON config used for generating JBrowse data.')
    parser.add_argument('file', metavar = 'FILE', nargs = '?', default = 'generate_jbrowse.conf', help = 'Name of the config file to be generated.')
    main(parser.parse_args())
