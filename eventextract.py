import xml.etree.ElementTree as ET
import re

# Function to extract and replace text in the XML file
def extract_and_replace_text_from_file(file_path, output_file, text_output_file):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    texts = []
    text_count = 1

    # Define a regex to match Chinese characters
    chinese_regex = re.compile(r'[\u4e00-\u9fff]+')

    # Function to process elements with 'text' attribute
    def process_element(element):
        nonlocal text_count
        if 'text' in element.attrib and chinese_regex.search(element.attrib['text']):
            original_text = element.attrib['text']
            tag = f"tsm.tl{text_count}"
            texts.append(f"<{tag}>{original_text}</{tag}>")
            element.attrib['text'] = f"[{tag}]"
            text_count += 1

    # Traverse the XML and process relevant elements
    for elem in root.iter():
        process_element(elem)

    # Write the modified XML back to the output file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    # Write the extracted text to a separate file
    with open(text_output_file, 'w', encoding='utf-8') as f:
        for line in texts:
            f.write(line + '\n')

    print(f"Modified XML written to: {output_file}")
    print(f"Extracted text written to: {text_output_file}")

# Replace these with your actual file paths
input_file_path = input("Drag and drop the Chinese file here: ").strip().strip('"')
output_file_path = 'modified_output.xml'
text_output_file_path = 'extracted_texts.txt'

# Run the function
extract_and_replace_text_from_file(input_file_path, output_file_path, text_output_file_path)
