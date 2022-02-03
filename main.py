from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import slack
import os
from pathlib import Path
from dotenv import load_dotenv

import time
import random


def main():
    url = 'https://www.cnn.com' #or input("URL: ")
    selector = '.banner-text' #or input("Selector: ")

    chromeOptions = Options()
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chromeOptions)
    driver.get(url)

    while True:
        driver.refresh()
        targets = driver.find_elements_by_css_selector(selector)
        message = f"CNN Headline: {procTargets(targets)}"
        send_to_slack(message)
        waitingTime = random.uniform(1*60, 10*60)
        time.sleep(waitingTime)
        print(f"Waited for {int(waitingTime/60)} minutes\n")


def procTargets(targets):
    for target in targets:
        print(target.text.strip())

    print()
    return targets[0].text

def send_to_slack(message):
    envPath = Path('.') / '.env'
    load_dotenv(dotenv_path=envPath)

    client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
    client.chat_postMessage(channel='#notify-me', text=message)

if __name__ == '__main__':
    main()
