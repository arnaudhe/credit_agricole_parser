import csv
import sys
import math
import re

if len(sys.argv) < 2:
    print "usage : python soge.py filename.tsv"
    sys.exit()

CA_SYNTAX = \
[{'filter' : 'Virement En Votre Faveur', 'format' : 'VIR - {0}'},                 \
 {'filter' : 'Prelevmnt',                'format' : 'PRELEV - {0}'},              \
 {'filter' : 'Prelevement',              'format' : 'PRELEV - {0}'},              \
 {'filter' : 'Cotisation',               'format' : 'FRAIS BANCAIRES - {0}'}]

def format_motif(motif):
    lines = motif.split(" \r\n")
    for syntax in CA_SYNTAX:
        if syntax['filter'] == lines[1].strip():
            return syntax['format'].format(*lines).upper()
    # no filter found
    return ' - '.join(lines).upper()

debits  = []
credits = []

with open(sys.argv[1]) as tsv:

    # discard the 2 first lines
    for i in range(11):
        next(tsv)

    for line in csv.reader(tsv, delimiter=";", lineterminator=";\n"): #You can also use delimiter="\t" rather than giving a dialect.
        if (len(line) >= 4):
            date        = line[0].strip()
            libelle     = format_motif(line[1])
            debit       = line[2].strip()
            credit      = line[3].strip()

            if (len(debit) > 0):
                debits.append("{}\t{}\t{}".format(date, libelle, debit))
            else:
                credits.append("{}\t{}\t{}".format(date, libelle, credit))

    print "\n".join(debits)
    print ' '
    print "\n".join(credits)