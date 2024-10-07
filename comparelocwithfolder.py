'''
import os
import xml.etree.ElementTree as ET
import re

# List of common materials/vanilla items to ignore
ignored_items = {"lead", "plastic", "copper", "magnesium", "iron", "steel"}

# Regular expression to detect Chinese characters
chinese_char_re = re.compile(r'[\u4e00-\u9fff]')

def load_translations(english_xml):
    """Load translated identifiers from English.xml into a set."""
    tree = ET.parse(english_xml)
    root = tree.getroot()

    translations = set()
    for elem in root.iter():
        if elem.tag.startswith(('entityname', 'entitydescription', 'talentname', 'afflictionname', 'afflictiondescription')):
            translations.add(elem.tag)

    return translations

def contains_chinese(text):
    """Check if a given text contains Chinese characters."""
    if text:
        return bool(chinese_char_re.search(text))
    return False

def check_untranslated(xml_file, translations):
    """Check for untranslated identifiers, names, or descriptions in an XML file, focusing on Chinese content."""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        untranslated = []
        for item in root.iter('Item'):
            identifier = item.get('identifier')
            name = item.get('name')
            description = item.get('description')

            # Filter out unnecessary items like materials/vanilla items
            if identifier in ignored_items:
                continue

            # Check if the name or description contains Chinese characters
            if identifier and contains_chinese(name) and f"entityname.{identifier}" not in translations:
                untranslated.append(f"<entityname.{identifier}>{name}</entityname.{identifier}>\n")
            if identifier and contains_chinese(description) and f"entitydescription.{identifier}" not in translations:
                untranslated.append(f"<entitydescription.{identifier}>{description}</entitydescription.{identifier}>\n")

        return untranslated

    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")
        return []

def append_to_english_xml(output_file, untranslated_entries):
    """Append untranslated entries to English.xml."""
    with open(output_file, 'a', encoding='utf-8') as f:
        for entry in untranslated_entries:
            f.write(entry)

def find_untranslated_in_directory(directory, english_xml, output_file):
    """Recursively find and append untranslated items in a directory."""
    translations = load_translations(english_xml)

    for root_dir, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root_dir, file)
                print(f"Processing: {file_path}")
                untranslated_entries = check_untranslated(file_path, translations)
                if untranslated_entries:
                    append_to_english_xml(output_file, untranslated_entries)

if __name__ == "__main__":
    # Path to the English.xml file
    english_xml =input("Drag and drop your english.xml here: ").strip().strip('"')

    # Directory containing the XML files to scan
    directory_to_scan = input("Enter the directory to scan for XML files: ").strip()

    # Specify the English.xml file to append untranslated entries to
    output_file = english_xml  # Same as the input English.xml in this case

    find_untranslated_in_directory(directory_to_scan, english_xml, output_file)

    print("Untranslated entries have been appended to English.xml.")


'''

import os
import xml.etree.ElementTree as ET
import re

# List of common materials/vanilla items to ignore
ignored_items = {"lead", "plastic", "copper", "magnesium", "iron", "steel"}

# Regular expression to detect Chinese characters
chinese_char_re = re.compile(r'[\u4e00-\u9fff]')

def load_translations(english_xml):
    """Load translated identifiers from English.xml into a set."""
    tree = ET.parse(english_xml)
    root = tree.getroot()

    translations = set()
    for elem in root.iter():
        # Collect translated elements for entities, afflictions, talents, etc.
        if elem.tag.startswith(('entityname', 'entitydescription', 
                                'afflictionname', 'afflictiondescription',
                                'talentname', 'talentdescription')):
            translations.add(elem.tag)

    return translations

def contains_chinese(text):
    """Check if a given text contains Chinese characters."""
    if text:
        return bool(chinese_char_re.search(text))
    return False

def check_untranslated(xml_file, translations):
    """Check for untranslated identifiers, names, or descriptions in an XML file, focusing on Chinese content."""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        untranslated = []
        # Iterate over all elements to find names/descriptions that may need translation
        for element in root.iter():
            identifier = element.get('identifier')
            name = element.get('name')
            description = element.get('description')

            # Filter out unnecessary items like materials/vanilla items
            if identifier in ignored_items:
                continue

            # Check if identifier is present and if its name/description contains Chinese characters
            if identifier and contains_chinese(name):
                tag_name = f"entityname.{identifier}"
                if tag_name not in translations:
                    untranslated.append(f"<{tag_name}>{name}</{tag_name}>\n")

            if identifier and contains_chinese(description):
                tag_desc = f"entitydescription.{identifier}"
                if tag_desc not in translations:
                    untranslated.append(f"<{tag_desc}>{description}</{tag_desc}>\n")

            # Also handle afflictions, talents, etc.
            if contains_chinese(name):
                # For afflictions, talents, etc.
                if element.tag == "Affliction":
                    tag_name = f"afflictionname.{identifier}"
                    if tag_name not in translations:
                        untranslated.append(f"<{tag_name}>{name}</{tag_name}>\n")

                if element.tag == "Talent":
                    tag_name = f"talentname.{identifier}"
                    if tag_name not in translations:
                        untranslated.append(f"<{tag_name}>{name}</{tag_name}>\n")

            if contains_chinese(description):
                if element.tag == "Affliction":
                    tag_desc = f"afflictiondescription.{identifier}"
                    if tag_desc not in translations:
                        untranslated.append(f"<{tag_desc}>{description}</{tag_desc}>\n")

                if element.tag == "Talent":
                    tag_desc = f"talentdescription.{identifier}"
                    if tag_desc not in translations:
                        untranslated.append(f"<{tag_desc}>{description}</{tag_desc}>\n")

        return untranslated

    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")
        return []

def append_to_english_xml(output_file, untranslated_entries):
    """Append untranslated entries to English.xml."""
    with open(output_file, 'a', encoding='utf-8') as f:
        for entry in untranslated_entries:
            f.write(entry)

def find_untranslated_in_directory(directory, english_xml, output_file):
    """Recursively find and append untranslated items in a directory."""
    translations = load_translations(english_xml)

    for root_dir, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root_dir, file)
                print(f"Processing: {file_path}")
                untranslated_entries = check_untranslated(file_path, translations)
                if untranslated_entries:
                    append_to_english_xml(output_file, untranslated_entries)

if __name__ == "__main__":
    # Path to the English.xml file
    english_xml =input("Drag and drop your english.xml here: ").strip().strip('"')

    # Directory containing the XML files to scan
    directory_to_scan = input("Enter the directory to scan for XML files: ").strip()

    # Specify the English.xml file to append untranslated entries to
    output_file = english_xml  # Same as the input English.xml in this case

    find_untranslated_in_directory(directory_to_scan, english_xml, output_file)

    print("Untranslated entries have been appended to English.xml.")
