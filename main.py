import requests
import bs4
import re 
from time import sleep
import os
from datetime import datetime, timedelta
import logging
import logging.handlers
from update_readme import update_log_in_md

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create log file handler
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)

# Handler formatter 
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

# Verify script
logger.info('The script ran')

# Function for checking env vars
def get_env_variable(key, error_message):
    try:
        # Check environment
        if "GITHUB_REPOSITORY" in os.environ:
            # Changes the repository name from e.g. "owner/repo" to "owner_repo" to create a valid GH Actions prefix
            repo_prefix = os.environ["GITHUB_REPOSITORY"].replace("/", "_") 
            return os.environ[f"{repo_prefix}_{key}"]
        else:
            return os.environ[key]
    except KeyError:
        if __name__ == "__main__":
            logger.warning(f"Token value: {error_message}")
        return error_message

# Env vars availability
TELEBOT_TOKEN = get_env_variable("SECRET1", "Bot token not available!")
MY_CHAT_ID = get_env_variable("SECRET2", "Telegram Chat ID token not available!")

# VARIABLES
MAX_ALLOWED_DURATION_SECONDS = 4 * 3600 + 59 * 60 # (4 hours and 59 minutes)
last_price = None
interval = 5
token = os.environ.get('TELEBOT_TOKEN')
chatID = os.environ.get('MY_CHAT_ID')
url = "https://www.kabum.com.br/produto/164854/placa-de-video-rtx-3060-asus-dual-o12g-v2-nvidia-geforce-12gb-gddr6-lhr-dlss-ray-tracing-dual-rtx3060-o12g-v2"

# Simulating the browser to gain access to the domain
headers = {
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

# Calculate when next hour's minute is equal to :59
def get_next_occurrence():
    now = datetime.now()
    MIN = 59
    next_occurrence = now.replace(minute=MIN, second=0, microsecond=0)

    if now.minute >= MIN:
        # If the current minute is 59 or greater, schedule the next occurrence for the next hour
        next_occurrence += timedelta(hours=1)

    time_difference = next_occurrence - now

    return time_difference.total_seconds(), next_occurrence

def sendMessage(price) :
    global last_price
    urlReq = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        'chat_id' : f'{chatID}', 
        'text': f'O preço abaixou! De R${last_price} por R${price}.\nLink:\n{url}'
        }
    requests.post(urlReq, data=data)

def routine():
    global last_price
    loop_counter = 0

    # Calculate the time until the next XX:59
    # (The next duration variable needs to be declared outside the loop)
    # sleep_duration is the time in seconds until XX:59
    sleep_duration, next_occurrence = get_next_occurrence()

    # Get the start time of the routine
    start_time = datetime.now()

    while True:
        now = datetime.now()

        # Check if it's 13:59 or if the maximum allowed duration is exceeded, if yes, break the loop
        if now.hour == 13 and now.minute == 59 or (now - start_time).total_seconds() >= MAX_ALLOWED_DURATION_SECONDS:
            logger.info("Stopping the script.")
            break

        # Log the time and counter when the routine runs
        loop_counter += 1
        logger.info(f"Running the routine. Loop count: {loop_counter}")

        req = requests.get(url, headers = headers)

        html = bs4.BeautifulSoup(req.content, 'html.parser')

        # Argument must be class_, because class is a reserved word in Python
        price_element = html.find(class_ = "finalPrice")

        # Note: This block of code seems to be skipped in the GitHub Action... Gotta find out why
        if price_element is not None:
            # Returns the text inside the element
            price_content = price_element.string
            
            print(price_content)

            # Returns a list with the words separated
            real, cents = map(lambda value: re.sub(r'[^0-9]', '', value), price_content.split(','))

            # Transforming the two values into a single string and converting to float (to compare with other numbers)
            price = float('.'.join([real, cents])) # XXXX & XX becomes XXXX.XX

            if last_price and price < last_price :
                sendMessage(price)

            last_price = price

            print(price)

        else:
            logger.warning("Price element not found. Stopping the script.")
            break

        # Update the README.md file with the log content
        log_file_path = 'status.log'
        md_file_path = 'README.md'
        update_log_in_md(log_file_path, md_file_path)

        # Program sleeps until the next XX:59
        sleep(sleep_duration)

        # Update next_occurrence for the next loop iteration
        sleep_duration, next_occurrence = get_next_occurrence()
    
    print(f"Routine stopped at {next_occurrence.strftime('%H:%M')}.")

if __name__ == "__main__":
    routine()
