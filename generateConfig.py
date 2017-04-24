#!/usr/bin/env python
import json
import subprocess


allTracks = [
#   (File name,          Category,                                                      Key,                                                    Color),
    ('scaffolds.fasta',  None,                                                          'All scaffolds',                                        None),
    ('Genes.gff',        'Predicted Genes / Protein Coding Genes',                      'All genes',                                            'blue'),
    ('InterProScan.gff', 'Predicted Genes / Protein Coding Genes',                      'InterProScan results',                                 'red'),
    ('Phobius.gff',      'Predicted Genes / Transmembrane Helices and Signal Peptides', 'Transmembrance helices and signal peptides (Phobius)', 'green'),
    ('SignalP.gff',      'Predicted Genes / Transmembrane Helices and Signal Peptides', 'Signal peptides (SignalP)',                            'limegreen'),
    ('TMHMM.gff',        'Predicted Genes / Transmembrane Helices and Signal Peptides', 'Transmembrane helices (TMHMM)',                        'greenyellow'),
    ('Card.gff',         'Predicted Genes / Other',                                     'Antibiotic resistance (CARD)',                         'lightsteelblue'),
    ('Doors.gff',        'Predicted Genes / Other',                                     'Operons (DOORS2)',                                     'teal'),
    ('Lipop.gff',        'Predicted Genes / Other',                                     'Lipoproteins (LipoP)',                                 'midnightblue'),
    ('Pilercr.gff',      'Predicted Genes / Other',                                     'CRISPR repeats (PILER-CR)',                            'darkcyan'),
    ('VFDB.gff',         'Predicted Genes / Other',                                     'Virulence factors (VFDB)',                             'darkorchid'),
]

genesDbxref = """\
function(value) {\
  if (!value) {\
    return null;\
  }\
  else if (typeof value === 'string') {\
    return "<a href='https://www.ncbi.nlm.nih.gov/protein/"+value+"'>" + value + "</a>";\
  }\
  else {\
    return value;\
  }\
}
"""

interProScanName = """\
function(value, feature) {\
  if (!value) {\
    return null;\
  }\
  else if (typeof value === 'string') {\
    var source = feature.get('Source');
    if (source === 'CDD') {\
      return "<a href='https://www.ncbi.nlm.nih.gov/Structure/cdd/cddsrv.cgi?uid="+value+"'>" + value + "</a>";\
    }\
    if (source === 'Gene3D') {\
      var entry = value.split(':')[1];\
      return "<a href='http://www.cathdb.info/version/latest/superfamily/"+entry+"'>" + value + "</a>";\
    }\
    else if (source === 'Hamap') {\
      return "<a href='http://hamap.expasy.org/unirule/"+value+"'>" + value + "</a>";\
    }\
    else if (source === 'PANTHER') {\
      return "<a href='http://www.pantherdb.org/panther/family.do?clsAccession="+value+"'>" + value + "</a>";\
    }\
    else if (source === 'PIRSF') {\
      return "<a href='http://pir.georgetown.edu/cgi-bin/ipcSF?id="+value+"'>" + value + "</a>";\
    }\
    else if (source === 'Pfam') {\
      return "<a href='http://pfam.xfam.org/family/"+value+"'>" + value + "</a>";\
    }\
    else if (source === 'PRINTS') {\
      return "<a href='http://130.88.97.239/cgi-bin/dbbrowser/PRINTS/DoPRINTS.pl?cmd_a=Display&qua_a=none&fun_a=Text&qst_a="+value+"'>" + value + "</a>";\
    }\
    else if (source === 'ProSiteFamilies') {\
      return "<a href='http://prosite.expasy.org/"+value+"'>" + value + "</a>";\
    }\
    else if (source === 'SUPERFAMILY') {\
      var entry = value.substring(3);\
      return "<a href='http://supfam.org/SUPERFAMILY/cgi-bin/scop.cgi?sunid="+entry+"'>" + value + "</a>";\
    }\
    else if (source === 'TIGRFAM') {\
      return "<a href='http://www.jcvi.org/cgi-bin/tigrfams/HmmReportPage.cgi?acc="+value+"'>" + value + "</a>";\
    }\
    else {\
      return value;\
    }
  }\
  else {\
    return value;\
  }\
}\
"""

interProScanDbxref = """\
function(value) {\
  if (!value) {\
    return null;\
  }\
  else if (typeof value === 'string') {\
    value = value.replace(/\"+/g, '');
    var entry = value.split(':');\
    if (entry[0] === 'InterPro') {\
      return "<a href='http://www.ebi.ac.uk/interpro/entry/"+entry[1]+"'>" + value + "</a>";\
    }\
    else if (entry[0] === 'KEGG') {\
      return "<a href='http://www.genome.jp/kegg-bin/show_pathway?ko"+entry[1]+"'>" + value + "</a>";\
    }\
    else if (entry[0] === 'MetaCyc') {\
      return "<a href='https://biocyc.org/META/NEW-IMAGE?object="+entry[1]+"'>" + value + "</a>";\
    }\
    else if (entry[0] === 'Reactome') {\
      return "<a href='http://www.reactome.org/content/detail/"+entry[1]+"'>" + value + "</a>";\
    }\
    else {\
      return value;\
    }
  }\
  else {\
    return value;\
  }\
}\
"""

interProScanOntology_term = """\
function(value) {\
  if (!value) {\
    return null;\
  }\
  else if (typeof value === 'string') {\
    value = value.replace(/\"+/g, '');
    var entry = value.split(':');\
    if (entry[0] === 'GO') {\
      return "<a href='http://amigo.geneontology.org/amigo/term/"+value+"'>" + value + "</a>";\
    }\
    else {\
      return value;\
    }
  }\
  else {\
    return value;\
  }\
}\
"""

genesColor = """\
function(feature) {\
  var source = feature.get('Source');\
  if (!source) {\
    return 'gray';\
  }\
  else if (typeof source === 'string') {\
    if (source === 'ab_initio') {\
      return 'deepskyblue';\
    }\
    else if (source === 'protein_homology') {\
      return 'royalblue';\
    }\
    else {\
      return 'gray';\
    }\
  }\
  else {\
    return 'gray';\
  }\
}\
"""

interProScanColor = """\
function(feature) {\
  var source = feature.get('Source');\
  if (!source) {\
    return 'gray';\
  }\
  else if (typeof source === 'string') {\
    if (source === 'CDD') {\
      return 'maroon';\
    }\
    if (source === 'Gene3D') {\
      return 'orange';\
    }\
    else if (source === 'Hamap') {\
      return 'mediumvioletred';\
    }\
    else if (source === 'PANTHER') {\
      return 'pink';\
    }\
    else if (source === 'Pfam') {\
      return 'mediumorchid';\
    }\
    else if (source === 'PIRSF') {\
      return 'magenta';\
    }\
    else if (source === 'PRINTS') {\
      return 'tomato';\
    }\
    else if (source === 'ProSiteFamilies') {\
      return 'lightcoral';\
    }\
    else if (source === 'SUPERFAMILY') {\
      return 'red';\
    }\
    else if (source === 'TIGRFAM') {\
      return 'orangered';\
    }\
    else {\
      return 'palevioletred';\
    }\
  }\
  else {\
    return 'gray';\
  }\
}\
"""

detailValueFormatters = {
  'Genes.gff'        : {'Dbxref' : genesDbxref},
  'InterProScan.gff' : {'Name' : interProScanName, 'Dbxref' : interProScanDbxref, 'Ontology_term' : interProScanOntology_term},
}

colorFunctions = {
  'Genes.gff'        : genesColor,
  'InterProScan.gff' : interProScanColor, 
}

def generateConfig(configFile):
    configDict = {}
    configDict['gffFiles'] = [track[0] for track in allTracks if track[0].endswith('.gff')]
    for track in allTracks:
        trackConfig = {}
        if track[1] is not None:
            thisConfigs = {'category' : track[1]}
            for field, function in detailValueFormatters.get(track[0], {}).iteritems():
                thisConfigs.update({'fmtDetailValue_%s'%field : function})
            trackConfig.update({'config' : json.dumps(thisConfigs)})
        if track[2] is not None:
            trackConfig.update({'key' : track[2]})
        if track[3] is not None:
            trackConfig.update({'clientConfig' : json.dumps({'color' : colorFunctions.get(track[0], track[3])})})
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
