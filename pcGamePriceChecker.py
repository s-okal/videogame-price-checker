from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import tkinter as tk
from tkinter import ttk
import os

# dictionary to be used for storing button links after lookups are completed
platformButtons = {}

def checkSteam(gameEntry): 
    # browser.get('https://store.steampowered.com')
    # # the name attribute of the search box is "term"
    # browser.find_element(By.NAME, "term").send_keys(gameEntry, Keys.ENTER)
    # browser.find_element(By.CSS_SELECTOR, "a href[class='title']")[0].click()
    print("\n----- Steam -----")
    url = (f"https://store.steampowered.com/search/?term={gameEntry}")
    
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    first_result = soup.find(class_="search_result_row")
    
    # search for "0 results match your search" element on webpage. If the element is visible and matches that text, end the Steam game search here.
    # otherwise, continue the scraping process
    try: 
        noResult = soup.find(class_="search_results_count")
        noResultMsg = noResult.get_text(strip=True)
        if noResultMsg == "0 results match your search.":
            print("NO MATCHES")
            with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
                f.write(f"Steam: No results found for '{gameEntry}'\n")
            return "No results found", "Please try again"
    except:
        pass


    if first_result:
        # find these elements on webpage
        resultTitle = first_result.find(class_="title")
        resultPrice = first_result.find(class_="discount_final_price")
        if resultTitle:
            # grab text from elements on webpage
            title = resultTitle.get_text(strip=True)
            print(f"Title: {title}")
            if resultPrice:
                price = resultPrice.get_text(strip=True)
                print(f"Price: {price}")
                with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
                    f.write(f"Steam: {title} -- {price}\n")
                return title, price
            # game has no price, likely because was announced but is not available for preorder yet
            else:
                print("Price: NOT AVAILABLE")
                with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
                    f.write(f"Steam: {title} -- Price: NOT AVAILABLE (has it been released yet?)\n")
                return title, "Price not available"
    else:
        print("No search results found! ")


def checkGMG(gameEntry):
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

    if resultTitle:
        title = resultTitle.get_text(strip=True)
        # Use '0' games found to determine if there are no search results
        if notFound == '0':
            print("No games found -- zero results returned")
            with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
                f.write(f"Green Man Gaming: No results found for '{gameEntry}'\n")
            return "No results found", "Game may be unavailable on this platform"
        # avoids search results that are returned that are irrelevant, like 'forza'
        # TODO: unintended side-effect: if user looks up 'grand theft auto 5', 'grand theft auto v' does not appear. Exclude roman numerals?
        elif gameEntry.lower() not in title.lower():
            print("Not found -- discarded erroneous results")
            with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
                f.write(f"Green Man Gaming: No results found for '{gameEntry}'\n")
            return "Not results found", "Game may be unavailable on this platform"
        else:
            print(f"Title: {title}")
            if resultPrice:
                price = resultPrice.get_text(strip=True)
                print(f"Price: {price}")
                with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
                    f.write(f"Green Man Gaming: {title} -- {price}\n")
                return title, price
            # might not be necessary
            else:
                print("No results found.")


def checkHumbleBundle(gameEntry):

    print("\n----- Humble Bundle -----")

    gameEntry.replace(" ", "%20")
    url = (f"https://www.humblebundle.com/store/search?sort=bestselling&search={gameEntry}&page=1&platform=windows")

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
        title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        print(f"Title: {title}")
        # avoids erroneous search results. Ensures searched game is within the title of the matched game
        if gameEntry.lower() not in title.lower():
            print("No results-- exact match not detected")
            with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
                f.write(f"Humble Bundle: No results found for '{gameEntry}'\n")
            return "No results found", "Game may be unavailable on this platform"
        elif resultPrice:
            price = resultPrice.get_text(strip=True)
            print(f"Price: {price}")
            with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
                f.write(f"Humble Bundle: {title} -- {price}\n")
            return title, price
    else:
        print("No results found!")
        with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
            f.write(f"Humble Bundle: No results found for '{gameEntry}'\n")
        return "No results found", "Game may be unavailable on this platform"

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
    noResults = soup.find('div', class_='css-17qmv99')

    # use "No results found" text from webpage, avoiding erroneously grabbing other displayed games.
    if noResults:
        print("No results found! (avoided grabbing other recommended games)")
        with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
            f.write(f"Epic Games Store: No results found for '{gameEntry}'\n")
        return "No results found", "Game may be unavailable on this platform"
    if results:
        # div container that holds the game title
        resultTitle = results.find('div', class_="css-rgqwpc")
        # span tag that holds the game price. If this was used without the results variable, other css-formatted text would be grabbed
        resultPrice = results.find('span', class_="css-119zqif")
        if resultTitle:
            title = resultTitle.get_text(strip=True)
            # Any special characters will be replaced with a blank string. Following two lines unused but I left them in for use in future updates
            title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
            titleSplit = title.lower().split()
            if gameEntry.lower() == title.lower():
                print(f"Title: {title}")
                if resultPrice:
                    price = resultPrice.get_text(strip=True)
                    print(f"Price: {price}")
                    with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
                        f.write(f"Epic Games Store: {title} -- {price}\n")
                    return title, price

            else:
                ("Exact match not found!")
                with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
                    f.write(f"Epic Games Store: No EXACT match for '{gameEntry}'\n")
                # exact match wasn't found for game, but user can still view search results when pressing button
                return "Exact match not found", "Click Epic Games Store Link to view all results"
    # not necessary?        
    else:
        print("No results found!")

# BEGINNING OF GUI-RELATED FUNCTIONS

# calls check function and returns the values to the GUI function
def processGame(gameEntry):
    steamTitle, steamPrice = checkSteam(gameEntry)
    gmgTitle, gmgPrice = checkGMG(gameEntry)
    hbTitle, hbPrice = checkHumbleBundle(gameEntry)
    epicTitle, epicPrice = checkEpic(gameEntry)
    with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
        f.write("\n---\n")
    return steamTitle, steamPrice, gmgTitle, gmgPrice, hbTitle, hbPrice, epicTitle, epicPrice


# create the tkinter GUI
def createGui():
    root = tk.Tk()
    root.title("PC Game Price Checker")

    # nested function to grab user entry from GUI and send to processGame function
    def triggerProcessGame():
        # grab user entry
        gameEntry = entry.get()
        steamTitle, steamPrice, gmgTitle, gmgPrice, hbTitle, hbPrice, epicTitle, epicPrice = processGame(gameEntry)
        
        # Update the labels when the values are returned from each function
        steamLabel.config(text=f"Steam: {steamTitle} -- {steamPrice}")
        gmgLabel.config(text=f"Green Man Gaming: {gmgTitle} -- {gmgPrice}")
        hbLabel.config(text=f"Humble Bundle: {hbTitle} -- {hbPrice}")
        epicLable.config(text=f"Epic Games Store: {epicTitle} -- {epicPrice}")

        # Assigns text to the button and provides the search link. Title is sent because it may contain "No results found" text meant for buttonUpdate function
        buttonUpdate("Steam", steamTitle, f"https://store.steampowered.com/search/?term={steamTitle}")
        buttonUpdate("Green Man Gaming", gmgTitle, f"https://www.greenmangaming.com/search?query={gameEntry}&platform=PC")
        buttonUpdate("Humble Bundle", hbTitle, f"https://www.humblebundle.com/store/search?sort=bestselling&search={gameEntry}&page=1&platform=windows")
        buttonUpdate("Epic Games Store", epicTitle, f"https://store.epicgames.com/en-US/browse?q={gameEntry}&sortBy=relevancy&sortDir=DESC&count=40")       

    # add a link button to the page if the button doesn't exist, OR updates the link if another game was previously assigned
    def buttonUpdate(platform, title, link):
        # calls deleteButton function which will remove it from the page if no results were found
        if title == "No results found":
            deleteButton(platform)
        # if the button exists already and the new search found a game, update the link
        elif platform in platformButtons:
            platformButtons[platform].config(command=lambda: openLink(link))
        # create a new button 
        else:
            if platform not in platformButtons:
                new_button = ttk.Button(root, text=f"{platform} Link", command=lambda l=link: openLink(l))
                new_button.pack()
                platformButtons[platform] = new_button
        

    # if a button exists from a prior search, and a new search returns no results, delete the platform button from the gui
    # called from buttonUpdate()
    def deleteButton(platform):
        if platform in platformButtons:
            platformButtons[platform].destroy()
            del platformButtons[platform]
        
    # opens the link when a button is clicked
    def openLink(link):
        import webbrowser
        webbrowser.open_new(link)

    def openReadMe():
        readMeWindow = tk.Toplevel(root)
        readMeWindow.title("ReadMe - Background Information")
        text = "This program will search four PC videogame storefronts to help you find the best price for a game.\n"
        text2 = """IMPORTANT INFO BELOW:\n
                1. This Python script REQUIRES that you have Selenium, BeautifulSoup, and the Chrome webdriver installed.
                It has only been tested with Python 3.11.\n
                2. Type the title of the game you want to search for as close to its original title format as possible! The search
                function on each website behaves differently and this program simply retrieves the first store result.
                For instance, searching for 'grand theft auto 5' instead of 'grand theft auto v' may not work as intended. Abbreviations typically
                won't work either (don't type 'rdr2' when looking for 'read dead redemption 2')\n
                3. The program may take some time after hitting the 'Search' button to gather the price from each website. Your
                computer may state the program is 'Not reponding'... please disregard this message and wait up to ONE MINUTE for results
                to be returned.\n"""
        text3 = """ADDITIONAL INFO:\n\nAlthough Steam can be scraped in 'headless' mode (without opening a browser window), the other sites have either JavaScript
                elements OR anti-scraping measures in place that force the use of an open browser window. The browser is set to minimize automatically
                for these sites. They will remain open for around 10-12 seconds each, as some JavaScript elements take time to load onto the screen. Please be patient!\n
                Some good examples to test this application are 'red dead redemption 2', 'doom', 'modern warfare 3',
                or some garbage text 'aisdfiafadfafd'\n
                """
        label1 = tk.Label(readMeWindow, text=text)
        label2 = tk.Label(readMeWindow, text=text2)
        label3 = tk.Label(readMeWindow, text=text3)
        label1.pack()
        label2.pack()
        label3.pack()
        


    # informational button at top of window
    readmeButton = tk.Button(root, text="READ ME", command=openReadMe)
    readmeButton.pack()

    label = tk.Label(root, text="Enter a PC game you'd like to check the price for: ")
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    button = tk.Button(root, text="Search", command=triggerProcessGame)
    button.pack()

    steamLabel = tk.Label(root, text="Steam: ", fg="blue")
    steamLabel.pack()

    gmgLabel = tk.Label(root, text="Green Man Gaming: ", fg="green")
    gmgLabel.pack()

    hbLabel = tk.Label(root, text="Humble Bundle: ", fg="red")
    hbLabel.pack()

    epicLable = tk.Label(root, text="Epic Games: ")
    epicLable.pack()

    

    root.mainloop()



# beginning of program. starts gui window        
if __name__ == '__main__':
    currentDate = date.today()
    # file is written to in every checkX() function. It will be stored in the same directory as this script.
    with open(os.path.join(os.getcwd(), 'videoGamePrices.txt'), 'a') as f:
        f.write(f"-----------------\nPC game prices - {currentDate}:\n-----------------\n")
              
    createGui()



# USED ONLY for command line version of program.
# gameEntry = input("Enter a PC game you'd like to check the price for: ")
# checkSteam(gameEntry)
# checkGMG(gameEntry)
# checkHumbleBundle(gameEntry)
# checkEpic(gameEntry)


# FUTURE FUNCTIONALITY??
# TODO: After the search is complete, make buttons appear for each game found that links to the 'search' page they were found on (just return url variable)

# TODO: Functionality to split user entered string into separate strings in order to capture every word in game title.
# From here, see if a word within the string is present in the title to ensure greater accuracy. Exclude common words like
# 'the' and 'of'. If it has a number, make sure the number is in the title. Include roman numerals ???? 

# TODO: brute force link that lets a user manually enter a url and grab the price?

# TODO: track historic price data in a shelve ??

# TODO: Since Steam is the most popular store platform, only allow games that match the Steam name??
