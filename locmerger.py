import xml.etree.ElementTree as ET

def extract_tags_with_content(file_path):
    """Extracts all tags and their content from an XML file."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    entries = {}
    # Iterate over all elements in the root and add their tag and text to the dictionary
    for subelement in root:
        entries[subelement.tag] = subelement  # Store the element itself, not just the text
    
    return entries

def merge_files(chinese_file, english_file, output_file):
    """Merges missing items from the Chinese XML into the English XML."""
    # Extract all entries (tags and their contents) from the Chinese and English XML files
    chinese_entries = extract_tags_with_content(chinese_file)
    english_entries = extract_tags_with_content(english_file)

    # Parse the English XML file for modification
    english_tree = ET.parse(english_file)
    english_root = english_tree.getroot()

    # Append missing entries from the Chinese file into the English file
    for tag, chinese_element in chinese_entries.items():
        if tag not in english_entries:
            print(f"Adding missing tag: {tag}")
            english_root.append(chinese_element)  # Append the whole element

    # Write the modified English XML to the output file
    english_tree.write(output_file, encoding='utf-8', xml_declaration=True)

    print(f"Merge complete. Output written to {output_file}.")


def main():
    # Prompt user for Chinese and English file paths
    chinese_file = input("Drag and drop the Chinese file here: ").strip().strip('"')
    english_file = input("Drag and drop the English file here: ").strip().strip('"')

    # Set output filename
    output_file = "merged_english_file.txt"

    # Merge missing items from the Chinese file into the English one
    merge_files(chinese_file, english_file, output_file)

if __name__ == "__main__":
    main()
