#!/usr/bin/env python
import json
import subprocess


allTracks = [
#   (File name,          Category,                                                      Key,                                                    Color), 
    ('scaffolds.fasta',  None,                                                          'All scaffolds',                                        None),                                        
    ('Genes.gff',        'Predicted Genes / Protein Coding Genes',                      'All genes',                                            'blue'),
    ('InterProScan.gff', 'Predicted Genes / Protein Coding Genes',                      'InterProScan results',                                 'red'),
    ('Phobius.gff',      'Predicted Genes / Transmembrane Helices and Signal Peptides', 'Transmembrance helices and signal peptides (Phobius)', 'green'),
    ('SignalP.gff',      'Predicted Genes / Transmembrane Helices and Signal Peptides', 'Signal peptides (SignalP)',                            'yellow'),
    ('TMHMM.gff',        'Predicted Genes / Transmembrane Helices and Signal Peptides', 'Transmembrane helices (TMHMM)',                        'yellow'),
    ('Card.gff',         'Predicted Genes / Other',                                     'Antibiotic resistance (CARD)',                         'yellow'),
    ('Doors.gff',        'Predicted Genes / Other',                                     'Operons (DOORS2)',                                     'yellow'),
    ('Lipop.gff',        'Predicted Genes / Other',                                     'Lipoproteins (LipoP)',                                 'yellow'),
    ('Pilercr.gff',      'Predicted Genes / Other',                                     'CRISPR repeats (PILER-CR)',                            'yellow'),
    ('VFDB.gff',         'Predicted Genes / Other',                                     'Virulence factors (VFDB)',                             'yellow'),
]                                                                                      

def generateConfig(configFile):
    configDict = {}
    configDict['gffFiles'] = [track[0] for track in allTracks if track[0].endswith('.gff')]
    for track in allTracks:
        trackConfig = {}
        if track[1] is not None:
            trackConfig.update({'config' : json.dumps({'category' : track[1]})})
        if track[2] is not None:
            trackConfig.update({'key' : track[2]})
        if track[3] is not None:
            trackConfig.update({'clientConfig' : json.dumps({'color' : track[3]})})
        configDict.update({track[0] : trackConfig})

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
