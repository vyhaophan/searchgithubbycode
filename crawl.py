from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from datetime import datetime
from dateutil.relativedelta import relativedelta

def parse_relative_time(relative_time):
    now = datetime.now()
    if 'week' in relative_time:
        if 'last' in relative_time:
            weeks_ago=1
        else:
            weeks_ago = int(relative_time.split()[0])
        return now - relativedelta(weeks=weeks_ago)
    elif 'month' in relative_time:
        if 'last' in relative_time:
            months_ago = 1
        else:
            months_ago = int(relative_time.split()[0])
        return now - relativedelta(months=months_ago)
    elif 'yesterday' in relative_time:
        days_ago = 1
    elif 'day' in relative_time:
        if 'last' in relative_time:
            days_ago = 1
        else:
            days_ago = int(relative_time.split()[0])
        return now - relativedelta(days=days_ago)
    elif 'year' in relative_time:
        if 'last' in relative_time:
            years_ago = 1
        else:
            years_ago = int(relative_time.split()[0])
        return now - relativedelta(years=years_ago)
    else:
        return None

def crawl_latest_update(url):
    WINDOW_SIZE = "1920,1080"
    # create and open a silent Chrome website
    chrome_options = webdriver.chrome.options.Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(chrome_options)
    driver.get(url)
    driver.implicitly_wait(5)
    print(f"Getting the last modified date of code: {url}")
    elem = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/main/turbo-frame/div/react-app/div/div/div[1]/div/div/div[2]/div[2]/div/div[3]/div[1]/div/div[2]/div[1]/span[1]/relative-time')
    time_text = elem.text
    assert "No results found." not in driver.page_source
    driver.close()
    relative_time = parse_relative_time(time_text)
    return relative_time, time_text

# crawl_latest_update('https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/azure.yaml')