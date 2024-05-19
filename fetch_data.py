import requests
import os

def fetch_json_data(url):
    """ Fetch JSON data from the given URL """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to retrieve data due to: {e}")
        return None

def convert_to_markdown(data):
    """ Convert JSON intrusion set data to Markdown format """
    markdown_files = []
    for obj in data['objects']:
        if obj['type'] == 'intrusion-set':
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
            markdown_files.append((filename, markdown))
    return markdown_files

def sanitize_filename(filename):
    """ Sanitize filenames to avoid filesystem errors """
    import re
    return re.sub(r'[<>:"/\\|?*]', '', filename)[:255]  # Remove problematic characters and truncate

def save_markdown_files(markdown_files):
    """ Save each Markdown file in a specified directory """
    directory = "obsidian_notes"
    os.makedirs(directory, exist_ok=True)
    for filename, content in markdown_files:
        path = os.path.join(directory, filename)
        try:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Successfully saved: {path}")
        except IOError as e:
            print(f"Failed to write file {path}: {e}")

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
