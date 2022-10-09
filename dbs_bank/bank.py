import glob
from typing import Dict
from custom import custom_categories

class DbsBank:
    def __init__(s):
        
        # init variables
        s.total_income, s.total_expense = 0, 0
        s.table: Dict[str, Dict[str, str]] = {}

        # load translations
        s.load_bank_codes()

        # parse csv data from different files
        for path in glob.glob(r'D:/data/bank/*'):
            s.read_bank_csv(path)

        # create new csv
        lines = []
        table = list(s.table.values())
        keep = [ 
            'category','keyword',
            'Transaction Date','amount',
        ]
        for row in table:
            s.find_amount(row)            
            s.add_custom_categories(row)
            lines.append(','.join([row[k] for k in keep]))
        fields = ','.join(keep)
        lines = [fields] + lines
        new_csv = '\n'.join(lines)
        with open('./test.csv','w+') as f:
            f.write(new_csv)

        # other info        
        print(f'+{s.total_income:.0f}, {s.total_expense:.0f}')
    
    def find_amount(s, row):
        income = s.float(row['Credit Amount'])
        expense = - s.float(row['Debit Amount'])
        s.total_income += income
        s.total_expense += expense
        row['amount'] = str(income + expense)
    
    def float(s, x=''):
        x = x.strip()
        if x: return float(x)
        return 0

    def add_custom_categories(s, row):
        for field in custom_categories:
            for cat in custom_categories[field]:
                for keyword in custom_categories[field][cat]:
                    if keyword in row[field]:
                        row['category'] = cat 
                        row['keyword'] = keyword
                        return
    
    def load_bank_codes(s):
        with open('bank_codes.txt', errors='ignore') as f:
            text = f.read().replace(',','.')
        lines = [x.strip() for x in text.split('\n')]
        s.codes = {}
        for i in range(0, len(lines), 2):
            k, v = lines[i:i+2]
            s.codes[k] = v

    def read_bank_csv(s, path):
        with open(path) as f:
            text = f.read()
        fields = None
        for line in text.split('\n'):
            line = line.strip()
            if line:
                if 'Transaction Date' in line:
                    fields = line.split(',')
                    continue
                if fields:
                    print(line)
                    cols = line.split(',')
                    dic = {k:v for k,v in zip(fields, cols)}
                    dic['Reference'] = s.codes[dic['Reference']]
                    s.table[line] = dic

if __name__=='__main__':
    bank = DbsBank()
