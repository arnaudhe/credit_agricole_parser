import xlrd
import sys

COLUMN_DATE         = 0
COLUMN_DESCRIPTION  = 1
COLUMN_DEBIT        = 2
COLUMN_CREDIT       = 3

CA_SYNTAX = [
    {'filter' : 'VIREMENT EN VOTRE FAVEUR', 'format' : 'VIREMENT - {}', 'rtrim' : 1},
    {'filter' : 'VIREMENT EMIS',            'format' : 'VIREMENT - {}', 'rtrim' : 5},
    {'filter' : 'PAIEMENT PAR CARTE',       'format' : 'CARTE - {}', 'rtrim' : 5}, 
    {'filter' : 'PRELEVEMENT',              'format' : 'PRELEVMT - {}', 'rtrim' : 1}, 
    {'filter' : 'CHEQUE EMIS',              'format' : 'CHEQUE - {}', 'rtrim' : 1},
    {'filter' : 'REGLEMENT',                'format' : 'REGLEMNT - {}', 'rtrim' : 5},
    {'filter' : 'REMBOURSEMENT DE PRET',    'format' : 'RBT PRET - {}', 'rtrim' : 8},
    {'filter' : 'RETRAIT AU DISTRIBUTEUR',  'format' : 'RETRAIT - {}', 'rtrim' : 12}
]

def sanitize_description(description):
    lines = [line.strip() for line in description.split("\n")]
    for syntax in CA_SYNTAX:
        if syntax['filter'] == lines[0]:
            return syntax['format'].format(lines[1][:-syntax['rtrim']].strip())[:43].upper()
    # no filter found
    return ' - '.join(lines).upper()

def find_first_row(sheet):
    row = 0
    while sheet.cell_value(row, 0) != 'Date':
        row = row + 1
    return row + 1       # Skip table header

# Load the xlsx sheet
sheet = xlrd.open_workbook(sys.argv[1]).sheet_by_index(0)

# Retrieve the first row index
row = find_first_row(sheet)

# Initilialize the lists
debits  = []
credits = []

while row < sheet.nrows:
    record = [sheet.cell_value(row, COLUMN_DATE),
             sanitize_description(sheet.cell_value(row, COLUMN_DESCRIPTION)),
             str(sheet.cell_value(row, COLUMN_DEBIT)).replace('.', ',')]
    if record[2] != '':
        debits.append(record)
    else:
        record[2] = str(sheet.cell_value(row, COLUMN_CREDIT)).replace('.', ',')
        credits.append(record)

    row = row + 1

debits.reverse()
credits.reverse()

print('\n'.join(['\t'.join(record) for record in debits]))
print('\n')
print('\n'.join(['\t'.join(record) for record in credits]))