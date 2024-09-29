import xml.etree.ElementTree as ET
import random
import string

# Load the XML file
input_file = input("Drag and drop the Chinese file here: ").strip().strip('"')
tree = ET.parse(input_file)
root = tree.getroot()

# Generate a random lowercase letter to make tags unique per file
random_char = random.choice(string.ascii_lowercase)

# Dictionary to store Chinese text and its corresponding tsm tag
text_dict = {}
count = 1

# Function to extract and replace text
def extract_text(elem):
    global count
    # Check if the element has text attributes we are interested in
    if 'text' in elem.attrib:
        text = elem.attrib['text'].strip()
        if any(u'\u4e00' <= char <= u'\u9fff' for char in text):  # Check if it's Chinese text
            if text not in text_dict:
                # Generate a unique tag with a random character and count
                tsm_tag = f"tsm.tl_{random_char}_{count}"
                text_dict[text] = tsm_tag
                count += 1
            else:
                # If the text already exists, reuse the existing tsm tag
                tsm_tag = text_dict[text]
            # Replace the original text with the tsm tag
            elem.attrib['text'] = f"<{tsm_tag}>"

    # Recursively process child elements
    for child in elem:
        extract_text(child)

# Start the extraction process
extract_text(root)

# Save the modified XML to a new file
output_file = 'output.xml'
tree.write(output_file, encoding='utf-8', xml_declaration=True)

# Output the localized tags for translation
localization_file = 'localization_output.txt'
with open(localization_file, 'w', encoding='utf-8') as f:
    for original_text, tsm_tag in text_dict.items():
        f.write(f"  <{tsm_tag}>{original_text}</{tsm_tag}>\n")

# Notify user
print(f"Processed {input_file}. Output written to {output_file} and {localization_file}")
