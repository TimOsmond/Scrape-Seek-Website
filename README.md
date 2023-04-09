# Scraping Seek using Selenium

## 1 Intro:
This program is designed to open seek.com.au webpages and gather information by saving text to a csv file.
It is enabled to move forward through web pages by clicking 'next' due to a limited number of jobs listed per page (currently 22).
Adjust this number if there are more or less jobs listed on the search page.

## 2 Goals:
The goal is to be able to search through seek job listings and save to csv for statistical analysis.

## 3 Steps:
- Install Selenium --> https://pypi.org/project/selenium/
- Install Chrome WebDriver --> https://chromedriver.chromium.org/downloads
- Import libraries

## 4 Final Output:
- The final output is a csv file with the web address, company name, job title and job description, sector, and states if a video is present.

## How it works:
- Go to the seek job search page and set the parameters on the page as required.
- Do not include any search text. Press search. You will see the URL change to the options chosen.
- Copy the URL
- Run seek_search.py
- Enter the copied URL when requested.
- Enter the term to search for in seek e.g. graduate or accountant or marketing etc.
- Enter a filename to save to. WARNING - file will append to existing filenames if same filename is used as a current file.
- Wait for the search to occur and add the number of jobs listed on the top of the page that has opened in seek.
- Press enter to run the program. The csv file will save and append for each search page it runs.
- The number of pages scraped is calculated on 22 jobs per page on seek, this may change.
