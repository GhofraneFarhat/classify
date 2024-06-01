from collections import defaultdict
import sys
import os

def classify_contig(description):
    attributes = {part.split(':')[0]: part.split(':')[1] for part in description.split()[2:]}

    # Check for plasmid-specific attributes
    if 'SH' in attributes:
        if not attributes['SH'].isdigit():
            return 'plasmid'

    # Check for chromosome-specific attributes
    if 'LN' in attributes and int(attributes['LN']) >= 1000000:
        return 'chromosome'

    # If neither plasmid nor chromosome attributes are present, classify as ambiguous
    if 'LN' in attributes or 'RC' in attributes or 'FC' in attributes or 'KC' in attributes:
        return 'ambiguous'

    # If no attributes are present, classify as unlabeled
    return 'unlabeled'

def classify(input_fasta, output_fasta):
    classifications = defaultdict(str)

    with open(input_fasta, 'r') as file:
        for line in file:
            if line.startswith('>'):
                contig_name, description = line.strip('>\n').split(' ', 1)
                classification = classify_contig(description)
                classifications[contig_name] = classification

    with open(output_fasta, 'w') as output_file:
        for contig, classification in classifications.items():
            output_file.write(f'>{contig} ({classification})\n')

            # Write the sequence
            with open(input_fasta, 'r') as input_file:
                found_contig = False
                for seq_line in input_file:
                    if seq_line.startswith(f'>{contig}'):
                        found_contig = True
                    elif found_contig and not seq_line.startswith('>'):
                        output_file.write(seq_line)
                    elif found_contig and seq_line.startswith('>'):
                        break






if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python script.py <input_fasta> <output_path>")
        sys.exit(1)

    input_fasta = sys.argv[1] #get the input file
    output_fasta = sys.argv[2] #get the output file

<<<<<<< HEAD
    
=======


>>>>>>> c52a06a2f88efda9192486a3fb1fe0c5ceb019f0
    output_directory = os.path.dirname(output_fasta) #get the directory where the file want to be saved

    #check if the file of the path is created else create the path
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
<<<<<<< HEAD
    


=======
        
>>>>>>> c52a06a2f88efda9192486a3fb1fe0c5ceb019f0
    classify(input_fasta, output_fasta)
    print(f"Results written to {output_fasta}")




        
