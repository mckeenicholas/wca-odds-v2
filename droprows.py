import csv


with open('WCA_export_Competitions.tsv', 'r') as src, open('Competitions.csv', 'w') as res:
    csrc = csv.reader(src, delimiter='\t')
    cres = csv.writer(res, delimiter=',')
    for row in csrc:
        newrow = [row[0], row[16], row[17], row[18]]
        cres.writerow(newrow)

with open('WCA_export_Results.tsv', 'r') as src, open('Results.csv', 'w') as res:
    csrc = csv.reader(src, delimiter='\t')
    cres = csv.writer(res, delimiter=',')
    for row in csrc:
        newrow = [row[0], row[1], row[2], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]]
        cres.writerow(newrow)
        