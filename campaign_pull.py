import requests
import os
import re

# Define the directory name here
output_directory_campaigns = "TA-Campaigns-1"

def fetch_json_data(url):
    """ Fetch JSON data from the given URL """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to retrieve data due to: {e}")
        return None

def link_campaigns_to_intrusion_sets(data):
    """Create a mapping of campaigns to intrusion sets"""
    relationships = {}
    for obj in data['objects']:
        if obj['type'] == 'relationship' and obj['relationship_type'] == 'uses':
            if obj['source_ref'].startswith('campaign') and obj['target_ref'].startswith('intrusion-set'):
                if obj['source_ref'] not in relationships:
                    relationships[obj['source_ref']] = []
                relationships[obj['source_ref']].append(obj['target_ref'])
    return relationships

def convert_campaign_to_markdown(data, relationships):
    """ Convert campaign JSON data to Markdown format and link to intrusion sets """
    markdown_files = []
    for obj in data['objects']:
        if obj['type'] == 'campaign':
            markdown = f"# {obj['name']}\n\n"
            markdown += f"**ID**: {obj['id']}\n"
            markdown += f"**Description**: {obj.get('description', 'No description available.')}\n\n"
            
            # Add links to related intrusion sets
            if obj['id'] in relationships:
                markdown += "## Related Intrusion Sets\n"
                for intrusion_set in relationships[obj['id']]:
                    markdown += f"- {intrusion_set}\n"
            
            filename = sanitize_filename(f"{obj['name']}.md")
            markdown_files.append((os.path.join(output_directory_campaigns, filename), markdown))
    return markdown_files

def sanitize_filename(filename):
    """ Sanitize filenames to avoid filesystem errors """
    return re.sub(r'[<>:"/\\|?*]', '', filename)[:255]  # Remove problematic characters and truncate

def save_markdown_files(markdown_files, directory):
    """ Save each Markdown file in a specified directory """
    for filepath, content in markdown_files:
        full_path = os.path.join(directory, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            with open(full_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Successfully saved: {full_path}")
        except IOError as e:
            print(f"Failed to write file {full_path}: {e}")

# URL to MITRE CTI Enterprise Attack JSON
json_url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

# Fetch data
data = fetch_json_data(json_url)

# Convert and save if data is successfully fetched
if data:
    relationships = link_campaigns_to_intrusion_sets(data)
    markdown_files = convert_campaign_to_markdown(data, relationships)
    save_markdown_files(markdown_files, output_directory_campaigns)
else:
    print("No data to process.")
