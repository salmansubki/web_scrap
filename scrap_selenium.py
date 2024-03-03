# Scrap table from multiple pages website
# the website using dynamic javascript and didn't change URL when we click next button

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

# using Firefox webdriver so no need install anything
driver = webdriver.Firefox(options=Options())

def scrape_page():
    # choose table selector using XPATH based on html structure
    table = driver.find_element(By.XPATH, '//div[@class="z-listbox-body"]')

    data = []

    # iterate through <tr> and <td> inside table
    for row in table.find_elements(By.XPATH, './/tr'):
        cells = [item.text for item in row.find_elements(By.XPATH, './/td')]
        data.append(cells)

    return data

def main():
    url = 'https://congkhaiketquathau.moh.gov.vn/Pages/admin/report/TT14/manager/mohTsvthcKhacManager.zul?code=2'  # set the URL
    num_pages = 3  # set the total number of pages want to scrap

    all_data = []

    driver.get(url)

    # scrap first page of the table
    page_data = scrape_page()
    all_data.extend(page_data)

    for i in range (num_pages-1):

        # find next button html selector
        next_button = driver.find_element(By.XPATH, '//a[@class="z-paging-button z-paging-next"]')

        # scroll to next button and click to move to next page
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("arguments[0].click();", next_button)

        # wait for the dynamic content to load (adjust timeout and conditions accordingly)
        WebDriverWait(driver, 10).until(EC.staleness_of(next_button))

        # scrap current page
        page_data = scrape_page()
        all_data.extend(page_data)

    # create a DataFrame
    df = pd.DataFrame(all_data)

    # save DataFrame to an Excel file
    df.to_excel('output2.xlsx', index=False)

    print("Data has been saved to excel")

if __name__ == '__main__':
    main()
