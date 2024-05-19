# Obsidian-ATTACK

Overview
This Python script automatically fetches intrusion set data from the MITRE CTI (Common Threats and Techniques Information) Enterprise Attack repository and converts it to Markdown format. The Markdown files are saved in a specified directory and can be used directly in applications like Obsidian for note-taking and data organization.

Features
Data Fetching: Retrieves JSON data directly from MITRE's CTI GitHub repository.
Markdown Conversion: Converts intrusion set information into Markdown files with tags formatted as #alias-aliasname.
Flexible Output: Easily change the output directory by modifying a single variable.
Prerequisites
Python 3.6 or higher
requests library

bash
Copy code
python fetch_intrusion_set_md.py
The script will fetch the latest intrusion set data from the MITRE CTI repository, convert it to Markdown, and save it in the specified directory (my_notes by default). You can change the output directory by editing the output_directory variable in the script.

Configuration

Output Directory: Modify the output_directory variable at the top of the script to change where the Markdown files are saved.

Contributing
Contributions to the script are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

License
This project is licensed under the MIT License - see the LICENSE.md file for details.

Contact
For support or queries, please email me at 

Acknowledgments

Thanks to MITRE for providing the CTI repository which made this script possible.
