import csv
import random

def convert_csv_training(input_file, output_file_90, output_file_10):
    with open(input_file, 'r') as infile, open(output_file_90, 'w', newline='') as outfile_90, open(output_file_10, 'w', newline='') as outfile_10:
        reader = csv.reader(infile)
        writer_90 = csv.writer(outfile_90)
        writer_10 = csv.writer(outfile_10)
        
        # Read the header row and exclude the 26th and 27th columns
        header = next(reader)
        modified_header_90 = [value for idx, value in enumerate(header) if idx not in [25, 26]]
        modified_header_10 = [value for idx, value in enumerate(header) if idx not in [25, 26]]

        writer_90.writerow(modified_header_90)
        writer_10.writerow(modified_header_10)

        # Read the remaining rows, shuffle, and write to the output files
        rows = list(reader)
        random.shuffle(rows)

        # Calculate the split indices
        split_index = int(0.9 * len(rows))

        # Write 90% of the rows to the first file
        for row in rows[:split_index]:
            # Exclude the 26th and 27th columns (indices 25 and 26)
            modified_row = [str(0.5) if value == '0' else str(0) if value == '-1' else str(value) for idx, value in enumerate(row) if idx not in [25, 26]]
            writer_90.writerow(modified_row)

        # Write the remaining 10% of the rows to the second file
        for row in rows[split_index:]:
            # Exclude the 26th and 27th columns (indices 25 and 26)
            modified_row = [str(0.5) if value == '0' else str(0) if value == '-1' else str(value) for idx, value in enumerate(row) if idx not in [25, 26]]
            writer_10.writerow(modified_row)

def convert_csv_testing(input_file,input_file2, output_file):
    with open(input_file, 'r') as infile,open(input_file2, 'r') as infile2, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        # reader2 = csv.reader(infile2)
        writer = csv.writer(outfile)

        # Read the header row
        header = next(reader)
        modified_header = [(f'label_{idx}', value) for idx, value in enumerate(header)]
        modified_header.append(('label', '1'))  # Add a label column with all values set to 1
        writer.writerow([item[0] for item in modified_header])

        # Read the remaining rows, shuffle, and write to the output file
        rows = list(reader)
        random.shuffle(rows)
        for row in rows:
            modified_row = [str(0.5) if value == '0' else str(0) if value == '-1' else str(value) for value in row]
            modified_row.append('1')  # Add the label value for the new column
            writer.writerow(modified_row)

        # Read the remaining rows, shuffle, and write to the output file
        # next(reader2)
        # rows = list(reader2)
        # random.shuffle(rows)
        # for row in rows:
        #     modified_row = [str(0.5) if value == '0' else str(0) if value == '-1' else str(value) for value in row]
        #     modified_row.append('0')  # Add the label value for the new column
        #     writer.writerow(modified_row)

if __name__ == "__main__":
    input_file = "Training Dataset.csv"  # replace with your input file name
    output_file = "training_output.csv"  # replace with your output file name
    output_file2 = "training_output_test.csv"  # replace with your output file name

    convert_csv_training(input_file, output_file,output_file2)
