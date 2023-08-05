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
        return os.environ[key]
    except KeyError:
        if __name__ == "__main__":
            logger.warning(f"Token value: {error_message}")
        return error_message

# Env vars availability
KEY_TELEBOT = ""
KEY_CHAT = ""

# Check environment
if "GITHUB_REPOSITORY" in os.environ:
    KEY_TELEBOT = "SECRET1"
    KEY_CHAT = "SECRET2"
else:
    KEY_TELEBOT = "TELEBOT_TOKEN"
    KEY_CHAT = "MY_CHAT_ID"

TELEBOT_TOKEN = get_env_variable(KEY_TELEBOT, "Bot token not available!")
MY_CHAT_ID = get_env_variable(KEY_CHAT, "Telegram Chat ID token not available!")

# VARIABLES
MAX_ALLOWED_DURATION_SECONDS = 4 * 3600 + 59 * 60 # (4 hours and 59 minutes)
last_price = None
interval = 5
token = TELEBOT_TOKEN
chatID = MY_CHAT_ID
#url = "https://api.scrapingdog.com/scrape?api_key=64c4aee1b3192c4b3fd9bb67&url=https://www.kabum.com.br/produto/164854/placa-de-video-rtx-3060-asus-dual-o12g-v2-nvidia-geforce-12gb-gddr6-lhr-dlss-ray-tracing-dual-rtx3060-o12g-v2&dynamic=false"
scrapdog_accessor = "https://api.scrapingdog.com/scrape?api_key=64c4aee1b3192c4b3fd9bb67&url="
urls_kabum = [
    f"{scrapdog_accessor}https://www.kabum.com.br/produto/164854/placa-de-video-rtx-3060-asus-dual-o12g-v2-nvidia-geforce-12gb-gddr6-lhr-dlss-ray-tracing-dual-rtx3060-o12g-v2", # GPU
    f"{scrapdog_accessor}https://www.kabum.com.br/produto/112995/processador-intel-core-i7-10700f-2-9ghz-4-8ghz-max-turbo-cache-16mb-lga-1200-bx8070110700f", # CPU
    f"{scrapdog_accessor}https://www.kabum.com.br/produto/172413/memoria-kingston-fury-beast-rgb-32gb-2x16gb-3200mhz-ddr4-cl16-preto-kf432c16bb1ak2-32", # RAM
    f"{scrapdog_accessor}https://www.kabum.com.br/produto/338410/ssd-480-gb-wd-green-m-2-leitura-545mb-s-wds480g3g0b", # SSD WD Green
    f"{scrapdog_accessor}https://www.kabum.com.br/produto/295687/ssd-wd-green-1tb-sata-leitura-545mb-s-gravacao-430mb-s-wds100t2g0a", # SSD Kingston

]

urls_pichau = [
    f"{scrapdog_accessor}https://www.pichau.com.br/gabinete-gamer-pichau-hx350-mid-tower-lateral-de-vidro-com-4-fans-preto-pg-hx35-bl01?gclid=Cj0KCQiA5NSdBhDfARIsALzs2EDDWINb1rakiLO4XJgVT29p9BY7r1_BtSEXCkzROzsdqM-6gikEiLcaApDcEALw_wcB",
]

# Class to handle each site
class SiteChecker:
    def __init__(self, name, url, find_element_method, element_identifier):
        self.name = name
        self.url = url
        self.find_element_method = find_element_method
        self.element_identifier = element_identifier
        self.last_price = None

    def check_price_and_send_message(self):
        req = requests.get(self.url)

        # Debugging
        logger.debug("Requisition status code: %s", req.status_code)
        # logger.debug("Requisition content: %s", req.content)

        html = bs4.BeautifulSoup(req.content, 'html.parser')

        price_element = html.find(self.find_element_method, class_= self.element_identifier)

        if price_element is not None:
            price_content = price_element.string
            real, cents = map(lambda value: re.sub(r'[^0-9]', '', value), price_content.split(','))
            price = float('.'.join([real, cents]))

            if self.last_price and price < self.last_price:
                sendMessage(price, self.url)

            self.last_price = price

            return price

        else:
            logger.warning(f"Price element not found for site: {self.name}")
            return self.last_price

# Create instances of SiteChecker for each site
site_kabum = SiteChecker(
    name = "Kabum",
    url = urls_kabum, 
    find_element_method = "class_",
    element_identifier = "finalPrice"
)

site_pichau = SiteChecker(
    name = "Pichau",
    url = urls_pichau,
    find_element_method = "class_",
    element_identifier = "jss267"
)

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

def sendMessage(price, url, site) :
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

    # List of SiteChecker objects
    sites = [site_kabum, site_pichau]
    
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

        # No need to add the headers parameter with a headers dict since the Scrappingdog API is being used
        #req = requests.get(url)
        
        # Check prices for all sites
        for site in sites:
            site.check_price_and_send_message()

        #html = bs4.BeautifulSoup(req.content, 'html.parser')

        # Argument must be class_, because class is a reserved word in Python
        #price_element = html.find(class_ = "finalPrice")

        '''
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
        '''

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
