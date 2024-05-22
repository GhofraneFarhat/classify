from collections import defaultdict
import sys

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
        print("Usage: python script.py <input_fasta> <output_fasta>")
        sys.exit(1)

    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]
    classify(input_fasta, output_fasta)
    print(f"Results written to {output_fasta}")