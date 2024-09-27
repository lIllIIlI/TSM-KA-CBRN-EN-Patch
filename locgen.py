import xml.etree.ElementTree as ET
import os

def extract_element_info(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        element_data = []

        # Iterate over all top-level elements
        for element in root:
            identifier = element.get('identifier')
            name = element.get('name', 'Unnamed')  # Default to "Unnamed" if no name
            desc = element.get('description', '')  # Keep description empty if not present

            if identifier:
                element_data.append((identifier, name, desc))

        return element_data
    except ET.ParseError as e:
        print(f"Error parsing {file_path}: {e}")
        return []  # Return empty if there's a parsing error

def extract_elements_recursive(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:  # Ensure utf-8 encoding
        # Walk through all files and directories
        for root_dir, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root_dir, file)
                    print(f"Processing file: {file_path}")

                    # Extract element info from the current file
                    element_data = extract_element_info(file_path)
                    for identifier, name, desc in element_data:
                        # Write the identifier and name in the desired format
                        f.write(f"<entityname.{identifier}>{name}</entityname.{identifier}>\n")
                        # Always write the entitydescription, even if empty
                        f.write(f"<entitydescription.{identifier}>{desc}</entitydescription.{identifier}>\n")

    print(f"All entity data written to {output_file}.")

def main():
    # Prompt user to drag and drop the directory
    input_dir = input("Drag and drop your directory here: ").strip().strip('"')

    # Generate output filename
    output_file = "all_entities_info.txt"

    # Extract element info recursively and save to one file
    extract_elements_recursive(input_dir, output_file)

if __name__ == "__main__":
    main()
