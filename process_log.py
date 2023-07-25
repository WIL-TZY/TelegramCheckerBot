# Read status.log file
with open("status.log", "r") as log_file:
    log_contents = log_file.read()

# Process the log_contents to create the formatted output
formatted_output = f"```\n{log_contents}\n```"

# Save the formatted output to console_output.txt
with open("console_output.txt", "w") as output_file:
    output_file.write(formatted_output)
