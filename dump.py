import xml.etree.ElementTree as ET
import os

def extract_identifiers_from_file(file_path, attribute="identifier"):
    tree = ET.parse(file_path)
    root = tree.getroot()

    identifiers = []
    for elem in root:
        identifier_value = elem.get(attribute)
        if identifier_value:
            identifiers.append(identifier_value)

    return identifiers

def extract_identifiers_recursive(directory, output_file, attribute="identifier"):
    with open(output_file, 'w') as f:
        # Walk through all files and directories
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    print(f"Processing file: {file_path}")

                    # Extract identifiers from the current file
                    identifiers = extract_identifiers_from_file(file_path, attribute)
                    for identifier in identifiers:
                        f.write(f"{identifier}\n")

    print(f"All identifiers written to {output_file}.")

def main():
    # Prompt user to drag and drop the directory
    input_dir = input("Drag and drop your directory here: ").strip().strip('"')

    # Generate output filename
    output_file = "all_identifiers.txt"

    # Extract identifiers recursively and save to one file
    extract_identifiers_recursive(input_dir, output_file)

if __name__ == "__main__":
    main()
