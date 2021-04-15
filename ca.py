import xlrd
import sys

COLUMN_DATE         = 0
COLUMN_DESCRIPTION  = 1
COLUMN_DEBIT        = 2
COLUMN_CREDIT       = 3

# Database of format to prettify the displaying of operations descriptions
# The filter value will be used to match the operation kind, in the first line
# of the raw description cell.
# the format parameter ({} token) will be replaced by the second line of raw
# operation description from the cell. 
# The rtrim will be used to remove final useless character in the raw description.
CA_SYNTAX = [
    {'filter' : 'VIREMENT EN VOTRE FAVEUR', 'format' : 'VIREMENT - {}', 'rtrim' : 1},
    {'filter' : 'VIREMENT EMIS',            'format' : 'VIREMENT - {}', 'rtrim' : 5},
    {'filter' : 'PAIEMENT PAR CARTE',       'format' : 'CARTE - {}',    'rtrim' : 5}, 
    {'filter' : 'PRELEVEMENT',              'format' : 'PRELEVMT - {}', 'rtrim' : 1}, 
    {'filter' : 'CHEQUE EMIS',              'format' : 'CHEQUE - {}',   'rtrim' : 1},
    {'filter' : 'REGLEMENT',                'format' : 'REGLEMNT - {}', 'rtrim' : 5},
    {'filter' : 'REMBOURSEMENT DE PRET',    'format' : 'RBT PRET - {}', 'rtrim' : 8},
    {'filter' : 'RETRAIT AU DISTRIBUTEUR',  'format' : 'RETRAIT - {}',  'rtrim' : 12}
]

def sanitize_date(value):
    # Returns a prettified date string from the raw date cell content
    year, month, day, _, _, _ = xlrd.xldate.xldate_as_tuple(value, datemode=0)
    return '{}/{}/{}'.format(year, month, day)

def sanitize_description(description):
    # Returns a prettified operation description from the raw description cell content
    lines = [line.strip() for line in description.split("\n")]
    for syntax in CA_SYNTAX:
        if syntax['filter'] == lines[0]:
            return syntax['format'].format(lines[1][:-syntax['rtrim']].strip())[:43].upper()
    # no filter found
    return ' - '.join(lines).upper()

def sanitize_price(price: str):
    # Returns a prettified operation price from the raw price (debit/credit) cell content
    return str(str(price).replace('.', ','))

def find_first_row(sheet):
    # Returns the index of the first sheet row containing a operation (debit or credit)
    row = 0
    while sheet.cell_value(row, 0) != 'Date':
        row = row + 1
    return row + 1       # Skip table header

# Load the xlsx sheet
sheet = xlrd.open_workbook(sys.argv[1]).sheet_by_index(0)

# Retrieve the first row index
row = find_first_row(sheet)

# Initilialize the operations lists
debits  = []
credits = []

# Iterate over operations
while row < sheet.nrows:
    record = { 'date' : sanitize_date(sheet.cell_value(row, COLUMN_DATE)),
               'description' : sanitize_description(sheet.cell_value(row, COLUMN_DESCRIPTION)),
               'debit' : sanitize_price(sheet.cell_value(row, COLUMN_DEBIT)),
               'credit' : sanitize_price(sheet.cell_value(row, COLUMN_CREDIT))}
    if record['debit'] != '':
        record.pop('credit')
        debits.append(record)
    else:
        record.pop('debit')
        credits.append(record)
    row = row + 1

# Reverse the operations lists to have oldest first
debits.reverse()
credits.reverse()

# Display the operations, by splitting debits and credits
print('\n'.join(['\t'.join(record.values()) for record in debits]))
print('\n')
print('\n'.join(['\t'.join(record.values()) for record in credits]))
