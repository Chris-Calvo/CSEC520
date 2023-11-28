import csv

def convert_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        next(reader)

        for row in reader:
            converted_row = [str(0.5) if value == '0' else str(0) if value == '-1' else str(value) for value in row]
            writer.writerow(converted_row)

if __name__ == "__main__":
    input_file = "Training Dataset.csv"  # replace with your input file name
    output_file = "output.csv"  # replace with your output file name

    convert_csv(input_file, output_file)
