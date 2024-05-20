import requests
import os
import re

# Define the directory name here
output_directory = "TA-IntrusionSets-1"

def fetch_json_data(url):
    """ Fetch JSON data from the given URL """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to retrieve data due to: {e}")
        return None

def categorize_intrusion_set(description, aliases):
    """ Categorize the intrusion set based on description and aliases """
    categories = {
        'Financially motivated / Cybercriminals': ["financial", "fraud", "money", "bank", "ransomware"],
        'Nation-states': ["apt", "state-sponsored"],
        'Hacktivists': ["hacktivist", "activist", "protest"]
    }
    countries = ['North Korea', 'Iran', 'Russia', 'China']
    
    # Check for specific country names for nation-states
    for country in countries:
        if country.lower() in description.lower():
            return os.path.join("APT", country)
    
    # General category checks
    for category, keywords in categories.items():
        if any(keyword.lower() in description.lower() for keyword in keywords):
            return category
        for alias in aliases:
            if any(keyword.lower() in alias.lower() for keyword in keywords):
                return category
    
    return "Other"  # Default category if no match is found

def convert_to_markdown(data):
    """ Convert JSON data to Markdown format """
    markdown_files = []
    for obj in data['objects']:
        if obj['type'] == 'intrusion-set':
            category = categorize_intrusion_set(obj.get('description', ''), obj.get('aliases', []))
            markdown = f"# {obj['name']}\n\n"
            markdown += f"**ID**: {obj['id']}\n"
            markdown += f"**Description**: {obj.get('description', 'No description available.')}\n\n"
            
            if 'aliases' in obj:
                markdown += "## Aliases\n"
                alias_tags = ', '.join([f"#alias-{alias.replace(' ', '_').replace('/', '-').lower()}" for alias in obj['aliases']])
                markdown += alias_tags + "\n\n"
            
            if 'external_references' in obj:
                markdown += "## References\n"
                for ref in obj['external_references']:
                    if 'url' in ref:
                        markdown += f"- [{ref['source_name']}]({ref['url']})\n"
                    else:
                        markdown += f"- {ref['source_name']}\n"

            filename = sanitize_filename(f"{obj['name']}.md")
            markdown_files.append((os.path.join(category, filename), markdown))
    return markdown_files

def sanitize_filename(filename):
    """ Sanitize filenames to avoid filesystem errors """
    return re.sub(r'[<>:"/\\|?*]', '', filename)[:255]  # Remove problematic characters and truncate

def save_markdown_files(markdown_files):
    """ Save each Markdown file in a specified directory """
    for filepath, content in markdown_files:
        full_path = os.path.join(output_directory, filepath)
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
    markdown_files = convert_to_markdown(data)
    save_markdown_files(markdown_files)
else:
    print("No data to process.")
