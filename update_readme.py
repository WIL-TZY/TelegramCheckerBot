import re

def update_log_in_md(log_file_path, html_file_path):

    # Read the contents of the log file
    with open(log_file_path, "r") as log_file:
        log_contents = log_file.read()

    # Split the log contents into lines
    lines = log_contents.strip().split("\n")

    # Get the last 6 log lines
    last_six_lines = lines[-6:] # Using slicing syntax: [start:end] / "-6" indicates the sixth-to-last element of the lines list

    # Add ">>>" before each line
    formatted_output_with_arrows = "\n".join([f">>> {line}" for line in last_six_lines])

    # Process the log_contents to create the formatted output
    formatted_output = f"```\n{formatted_output_with_arrows}\n```"

    # Storing the README.md content within a new variable
    with open(html_file_path, "r") as readme:
        readme_content = readme.read()

    # Using re.sub() to replace content between markers ``` and ```
    pattern = r"```.*?```"
    updated_readme_content = re.sub(pattern, formatted_output, readme_content, flags=re.DOTALL)

    # Write the updated content back to the README.md file
    with open(html_file_path, "w") as readme:
        readme.write(updated_readme_content)

def main():
    # Path to the log file
    log_file_path = 'status.log'
    
    # Path to the MD file
    md_file_path = 'README.md'

    # Update the HTML file with the log content
    update_log_in_md(log_file_path, md_file_path)

# This part only runs if this script is run as main
if __name__ == "__main__":
    main()
    