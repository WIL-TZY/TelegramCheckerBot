# Read the contents of console_output.txt
with open("console_output.txt", "r") as output_file:
    formatted_output = output_file.read()

# Update the README.md file with the formatted output
readme_file = "README.md"
with open(readme_file, "r") as readme:
    readme_content = readme.read()

# Replace the placeholder with the formatted output
updated_readme_content = readme_content.replace("<output of the formatted status.log file goes here>", formatted_output)

# Write the updated content back to the README.md file
with open(readme_file, "w") as readme:
    readme.write(updated_readme_content)