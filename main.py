import requests
import bs4
import re 
from time import sleep
import os
import datetime
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

# Function for checking env vars
def get_env_variable(key, error_message):
    try:
        return os.environ[key]
    except KeyError:
        # Print the token value only when it falls into the except block
        if __name__ == "__main__":
            logger.warning(f"Token value: {error_message}")
        return error_message

# Env vars availability
TELEBOT_TOKEN = get_env_variable("TELEBOT_TOKEN", "Bot token not available!")
MY_CHAT_ID = get_env_variable("MY_CHAT_ID", "Telegram Chat ID token not available!")

# Verify script
logger.info('The script ran')

last_price = None
interval = 5
token = os.environ.get('TELEBOT_TOKEN')
chatID = os.environ.get('MY_CHAT_ID')
url = "https://www.kabum.com.br/produto/164854/placa-de-video-rtx-3060-asus-dual-o12g-v2-nvidia-geforce-12gb-gddr6-lhr-dlss-ray-tracing-dual-rtx3060-o12g-v2"

# Simulating the browser to gain access to the domain
headers = {
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

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
    
    while True:
        req = requests.get(url, headers = headers)

        html = bs4.BeautifulSoup(req.content, 'html.parser')

        # Argument must be class_, because class is a reserved word in Python
        price_element = html.find(class_ = "finalPrice")

        if price_element is not None:
            # Returns the text inside the element
            price_content = price_element.string
            
            print(price_content)

            # Returns a list with the words separated
            real, cents = map(lambda value: re.sub(r'[^0-9]', '', value), price_content.split(','))

            # Transforming the two values into a single string
            price = float('.'.join([real, cents])) # XXXX & XX becomes XXXX.XX

            # Converting to float (to compare with other numbers)
            #price = float(price)

            if last_price and price < last_price :
                sendMessage(price)

            last_price = price

            print(price)

            # Update the README.md file with the log content
            log_file_path = 'status.log'
            md_file_path = 'README.md'
            update_log_in_md(log_file_path, md_file_path)
        else:
            logger.warning("Price element not found.")

        # Program runs every 5 hours
        sleep(60 * 60 * interval)

print("Routine ran, now sleeping")

if __name__ == "__main__":
    routine()
