from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import date

# TODO: make sure that the returned games are explicitly what the user would look for. 'forza' will return non-forza games from most sites--
# maybe use regex to make sure an intended game is returned?


# HEADLESS OPERATION: 
# options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
# browser = webdriver.Chrome(options=options)

# TODO: work in progress- append to a file with collected values
def fileSetup():
    today = date.today()
    with open(os.path.join(os.getcwd(), 'data.txt'), 'a') as file:
        file.write(today)


def checkSteam(gameEntry): # -- WORKS!
    # browser.get('https://store.steampowered.com')
    # # the name attribute of the search box is "term"
    # browser.find_element(By.NAME, "term").send_keys(gameEntry, Keys.ENTER)
    # browser.find_element(By.CSS_SELECTOR, "a href[class='title']")[0].click()
    print("\n----- Steam -----")
    url = (f"https://store.steampowered.com/search/?term={gameEntry}")
    
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    first_result = soup.find(class_="search_result_row")

    if first_result:
        resultTitle = first_result.find(class_="title")
        resultPrice = first_result.find(class_="discount_final_price")
        if resultTitle:
            title = resultTitle.get_text(strip=True)
            print(f"Title: {title}")
            if resultPrice:
                price = resultPrice.get_text(strip=True)
                print(f"Price: {price}")
            # game has no price, likely because was announced but is not available for preorder
            else:
                print("Price: NOT AVAILABLE")
    else:
        print("No search results found! ")


def checkGMG(gameEntry): # 12/7/23 seems to work. able to handle both 0 results and if complete garbage results are returned
    print("\n----- Green Man Gaming -----")
    gameEntry.replace(" ", "%20")
    url = (f"https://www.greenmangaming.com/search?query={gameEntry}&platform=PC")
    browser = webdriver.Chrome()
    browser.get(url)
    browser.minimize_window()
    # we need to wait for all js elements to load
    time.sleep(2)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    time.sleep(5)
    browser.close()

    # Grab  GAMES [int] element from the webpage to determine if search results were found
    resultNotFound = soup.find('span', class_="ais-Stats-text")
    notFound = resultNotFound.get_text(strip=True)
    
    # grabs html elements for title and price. will still be populated if none found, as it shows recommendations
    resultTitle = soup.find('p', class_="prod-name")
    resultPrice = soup.find('span', class_="current-price")

    # resultTitleList = resultTitle.split()

    if resultTitle:
        title = resultTitle.get_text(strip=True)
        # Use '0' games found to notify of no search results
        if notFound == '0':
            print("No games found -- zero results returned")
        # avoids search results that are returned that are irrelevant, like 'forza'
        # another example: 'shit a'
        elif gameEntry.lower() not in title.lower():
            print("Not found -- discarded erroneous results")
        else:
            print(f"Title: {title}")
            if resultPrice:
                price = resultPrice.get_text(strip=True)
                print(f"Price: {price}")
            else:
                print("No results found.")


    # # Doesnt totally work
    # if resultNotFound:
    #     print("RESULTS NOT FOUND")

    # elif resultTitle:
    #     title = resultTitle.get_text(strip=True)
    #     print(f"Title: {title}")
    #     if resultPrice:
    #         price = resultPrice.get_text(strip=True)
    #         print(f"Price: {price}")
    #     else:
    #         print("No results found!")
            
    # PREVIOUS CODE
    # while True:
    #     # avoid recommended games showing false positive
    #     if notFound == '0':
    #         print("No games found!")
    #         return False
    #     elif resultTitle:
    #         title = resultTitle.get_text(strip=True)
    #         print(f"Title: {title}")
    #         if resultPrice:
    #             price = resultPrice.get_text(strip=True)
    #             print(f"Price: {price}")
    #             break
    #     else:
    #         print("No results found!")
    #         break


def checkG2A(gameEntry):
    print("----- G2A -----")

    # website will replace space char with %20
    gameEntry.replace(" ", "%20")
    # url will apply filters for PC games specifically
    url = (f"https://www.g2a.com/category/games-c189?f%5Bdevice%5D%5B0%5D=1118&query={gameEntry}")

    browser = webdriver.Chrome()
    browser.get(url)
    browser.minimize_window()
    soup = BeautifulSoup(browser.page_source, "html.parser")
    time.sleep(5)
    browser.close()

    resultTitle = soup.find(class_="Card__title")
    resultPrice = soup.find(class_="Card__price-cost")

    if resultTitle and resultPrice:
        title = resultTitle.get_text(strip=True)
        price = resultPrice.get_text(strip=True)
        print(f"Title {title}")
        print(f"Price: {price}")
    else:
        print("No search results found!")


def checkHumbleBundle(gameEntry):

    # TODO: modify to make headless
    # JS makes it harder to scrape the page. We'll use Selenium and Beautiful Soup here.

    print("\n----- Humble Bundle -----")

    gameEntry.replace(" ", "%20")
    print(gameEntry)
    url = (f"https://www.humblebundle.com/store/search?sort=bestselling&search={gameEntry}&page=1&platform=windows")
    # url = "https://www.humblebundle.com/store/search?search=poop"


    browser = webdriver.Chrome()
    browser.get(url)
    browser.minimize_window()
    # grab the HTML source from the webpage
    time.sleep(2)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    # for some reason without sleep, it won't always grab accurate results. perhaps waiting on js event?
    time.sleep(4)
    browser.close()

    resultTitle = soup.find('span', class_="entity-title")
    resultPrice = soup.find('span', class_='price')

    if resultTitle:
        title = resultTitle.get_text(strip=True)
        print(f"Title: {title}")
        if resultPrice:
            price = resultPrice.get_text(strip=True)
            print(f"Price: {price}")
    else:
        print("No results found!")


def checkEpic(gameEntry):
    print("----- Epic Games Store -----")
    gameEntry.replace(" ", "%20")
    url = (f"https://store.epicgames.com/en-US/browse?q={gameEntry}&sortBy=relevancy&sortDir=DESC&count=40")

    
    browser = webdriver.Chrome()
    browser.get(url)
    browser.minimize_window()
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    time.sleep(5)
    browser.close()

    # grabbing the div "container" that holds the game title and price information
    results = soup.find('div', class_="css-hkjq8i")
    

    if results:
        # div container that holds the game title
        resultTitle = results.find('div', class_="css-rgqwpc")
        # span tag that holds the game price. If this was used without the results variable, other css-formatted text would be grabbed
        resultPrice = results.find('span', class_="css-119zqif")
        if resultTitle:
            title = resultTitle.get_text(strip=True)
            print(f"Title: {title}")
            if resultPrice:
                price = resultPrice.get_text(strip=True)
                print(f"Price: {price}")
    else:
        print("No results found!")

def checkEpicAccurate(gameEntry):
    print("----- Epic Games Store ACCURATE -----")
    gameEntry.replace(" ", "%20")
    url = (f"https://store.epicgames.com/en-US/browse?q={gameEntry}&sortBy=relevancy&sortDir=DESC&count=40")

    # Split user-entered title into split strings
    titleWords = gameEntry.lower().split()
    excludedWords = ['the', 'of']

    

    
    browser = webdriver.Chrome()
    browser.get(url)
    browser.minimize_window()
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    time.sleep(5)
    browser.close()

    # grabbing the div "container" that holds the game title and price information
    results = soup.find('div', class_="css-hkjq8i")
    noResults = soup.find('div', class_='css-17qmv99')

    # use "No results found" text from webpage, avoiding erroneously grabbing other displayed games.
    if noResults:
        print("No results found! (avoided grabbing other recommended games)")
        if results:
            # div container that holds the game title
            resultTitle = results.find('div', class_="css-rgqwpc")
            # span tag that holds the game price. If this was used without the results variable, other css-formatted text would be grabbed
            resultPrice = results.find('span', class_="css-119zqif")
            if resultTitle:
                title = resultTitle.get_text(strip=True)
                # Any special characters will be replaced with a blank string
                title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
                titleSplit = title.lower().split()
                if gameEntry.lower() == title.lower():
                    print(f"Title: {title}")
                    if resultPrice:
                        price = resultPrice.get_text(strip=True)
                        print(f"Price: {price}")

                else:
                    ("Exact match not found!")
                
        else:
            print("No results found!")
        
   
gameEntry = input("Enter a PC game you'd like to check the price for: ")

fileSetup()
# checkSteam(gameEntry)
checkGMG(gameEntry)
# checkHumbleBundle(gameEntry)
# checkEpic(gameEntry)
# checkEpicAccurate(gameEntry)
# checkG2A(gameEntry)


# TODO: Functionality to split user entered string into separate strings in order to capture every word in game title.
#   From here, see if a word within the string is present in the title to ensure greater accuracy. Exclude common words like
#   'the' and 'of'. If it has a number, make sure the number is in the title. Include roman numerals ????

# TODO: brute force link that lets a user manually enter a url and grab the price?

# TODO: track historic price data in a shelve

# TODO: Since Steam is the most popular store platform, only allow games that match the Steam name??




















# HEADLESS UNIT TEST OPERATION: 
# https://www.zenrows.com/blog/headless-browser-python#switch-to-python-selenium-headless-mode
# https://www.selenium.dev/blog/2023/headless-is-going-away/
# 
# import unittest
# from selenium import webdriver

# class GoogleTestCase(unittest.TestCase):

#     def setUp(self):
#         options = webdriver.ChromeOptions()
#         options.add_argument("--headless=new")
#         self.driver = webdriver.Chrome(options=options)
        
        

#     def test_page_title(self):
#         self.driver.get('https://store.steampowered.com')
#         self.assertIn('Welcome to Steam', self.driver.title)

# if __name__ == '__main__':
#     unittest.main(verbosity=2)

# https://stackoverflow.com/questions/71418546/beautiful-soup-not-working-on-this-website