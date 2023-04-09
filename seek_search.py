"""
Allow the input of a search term into seek employment webpage and download the results to a csv file for analysis.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import csv

print("Navigate to the seek page and do a blank search with required parameters.")
print("Copy the URL to the prompt below:-")
original_url = input("Enter the Seek URL you have copied: ")
# search_criteria = input("Enter search request: ")
search_criteria = "graduate"
filename = input("Enter filename for csv file: ")
# setting driver
options = webdriver.ChromeOptions()
options.add_argument("--incognito")

# creating driver
driver = webdriver.Chrome(options=options)

# opening webpage at url
driver.get(original_url)

# wait for page to open
wait = WebDriverWait(driver, 5)

# creating search
search_bar = driver.find_element(By.NAME, "keywords")
search_bar.clear()
print("*" * 30)
print(f"Searching for '{search_criteria}'")
print("*" * 30)

# enter the search criteria and return result
search_bar.send_keys(search_criteria)
search_bar.send_keys(Keys.RETURN)

# lose focus on search field so the "next" button can be found later
ActionChains(driver).send_keys(Keys.TAB * 4).perform()

# open the currently used url
found_url = driver.current_url
print("Found jobs at url", found_url)

# ask for the number of jobs found (at top of opened page)
number_of_jobs = int(input("How many jobs were found: "))
if number_of_jobs % 22 == 0:  # there are 22 jobs listed on each page
    pages = number_of_jobs / 22
else:
    pages = (number_of_jobs // 22) + 1
print(f"Scraping {pages} pages")

for i in range(1, pages + 1):
    job_titles = []
    companies = []
    sectors = []
    jobs_details = []
    job_videos = []
    links = []

    driver.minimize_window()

    while True:
        new_links = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//a[contains(@data-automation, 'jobTitle')]")))
        links.extend([link.get_attribute("href") for link in new_links])

        try:  # EC needed as otherwise the element was not clickable
            next_page_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//ul[contains(@class, 'pagination')]/li[last()]/a")))
        except TimeoutException:
            break

    print(f"\nLinks being scraped: page {i} of {pages}")

    # open a new minimised window for the job listings
    driver.switch_to.new_window('window')
    driver.minimize_window()

    for link in links:
        driver.get(link)
        print(driver.title)

        # find company name
        try:
            company = driver.find_element(By.XPATH,
                                          "//div[@class='_1wkzzau0 a1msqir a1msqiem a1msqiej a1msqiba a1msqib7 a1msqi4y a1msqifm'][1]").text
            companies.append(company)
        except NoSuchElementException:
            companies.append("no company name")

        # find sector
        try:
            sector = driver.find_element(By.XPATH,
                                         "//div[@class='_1wkzzau0 a1msqi6u'][3]").text
            sectors.append(sector)
        except NoSuchElementException:
            sectors.append("no sector")

        # find job title
        try:
            job_title = driver.find_element(By.XPATH,
                                            "//h1[contains(@data-automation, 'job-detail-title')]").text
            job_titles.append(job_title)
        except NoSuchElementException:
            job_titles.append("no job title")

        # find company
        try:
            job_detail = driver.find_element(By.XPATH, "//div[contains(@data-automation, 'jobAdDetails')]").text
            jobs_details.append(job_detail)
        except NoSuchElementException:
            jobs_details.append("no job details")

        # find if video present
        try:
            job_video = driver.find_element(By.CLASS_NAME, 'e7teq51').text
            job_videos.append("video present")
        except NoSuchElementException:
            job_videos.append("")

    with open("".join([filename.replace(" ", "-"), ".csv"]), 'a', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["Link", "Job Title", "Company", "Sector", "Job Details", "Job Video"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writer.writeheader()
        for link, job_title, company, sector, job_details, job_video in zip(links, job_titles, companies, sectors,
                                                                            jobs_details, job_videos):
            writer.writerow(
                {"Link": link, "Job Title": job_title, "Company": company, "Sector": sector, "Job Details": job_details,
                 "Job Video": job_video})

    # close secondary window
    driver.close()
    # switch to original window
    driver.switch_to.window(driver.window_handles[0])
    # click the next button
    next_button = driver.find_element(By.LINK_TEXT, "Next")
    next_button.send_keys(Keys.RETURN)

driver.quit()
print("*" * 30)
print("".join([filename.replace(" ", "_"), ".csv file saved"]))
print("Done! :)")
