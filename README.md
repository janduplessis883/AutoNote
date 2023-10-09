![AutoNote](https://github.com/janduplessis883/AutoNote/blob/master/AutoNoteSlash.png?raw=true)

## Overview

The AutoNote Python class aims to enhance your Jupyter Notebook experience by adding automation, utility, and interactivity. The class is designed to assist with routine tasks, such as connecting to a MySQL database, It also provides a unique way of managing code snippets, allowing you to save, load, and organize pieces of code directly within your notebook.

## Features

### Database Connection
Quick MySQL Connectivity: AutoNote comes with a built-in method to connect to your MySQL database.
Interactive Connection Management: GUI buttons allow you to connect or disconnect from the database effortlessly.
Error Handling: If the connection fails, an error message is displayed.

### Code Snippets Management
Snippet Saving: Save important code snippets along with a group name and an optional markdown flag.
Code Loading: Load saved snippets into new code cells or markdown cells with a single click.
Group Management: Keep your snippets organized in named groups.
Integrated Google Sheet Logging
Activity Logging: All important events like database connectivity, code snippet addition, etc., are logged into a Google Sheet.
URL Accessibility: The Google Sheet can be accessed through a provided URL.
### Miscellaneous
GUI Elements: The class offers various GUI components like buttons and dropdowns for an interactive user experience.
Markdown Support: The class allows you to insert markdown snippets along with code snippets.
# Installation

bash
Copy code
git clone https://github.com/janduplessis883/AutoNote.git
# Dependencies

mysql-connector<BR>
Google Sheet API<
EmailBuddy library<
# Usage

python
Copy code
from AutoNote import AutoNote

# Instantiate the class
auto_note = AutoNote()

# Connect to MySQL Database
auto_note.connect_to_mysql_with_status()

# Add a new code snippet
auto_note.new_code()

# Load existing code snippet
auto_note.load_code()
License

This project is licensed under the MIT License.
