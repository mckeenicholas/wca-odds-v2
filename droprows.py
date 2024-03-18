import csv
import sys

def process_competitions(input_file, output_file):
    with open(input_file, 'r') as src, open(output_file, 'w', newline='') as res:
        csrc = csv.reader(src, delimiter='\t')
        cres = csv.writer(res, delimiter=',')
        for row in csrc:
            newrow = [row[0], row[16], row[17], row[18]]
            cres.writerow(newrow)

def process_results(input_file, output_file):
    with open(input_file, 'r') as src, open(output_file, 'w', newline='') as res:
        csrc = csv.reader(src, delimiter='\t')
        cres = csv.writer(res, delimiter=',')
        for row in csrc:
            newrow = [row[0], row[1], row[2], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]]
            cres.writerow(newrow)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 droprows.py competitions_input results_input competitions_output results_output")
        sys.exit(1)

    competitions_input = sys.argv[1]
    results_input = sys.argv[2]
    competitions_output = sys.argv[3]
    results_output = sys.argv[4]

    process_competitions(competitions_input, competitions_output)
    process_results(results_input, results_output)
