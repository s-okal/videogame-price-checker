# PC Videogame Price Checker

This program uses Python web scraping to find the best deal for PC video games. It searches four popular storefronts, including Steam, Green Man Gaming, Humble Bundle, and the Epic Games Store. The program will produce the output in a GUI and provide links to each storefront when a game is found.

## Dependencies 

NOTE: This program has only been tested with Python 3.11. Use other versions at your own risk.

NOTE: You MUST have Chrome and the associated Web Driver installed for Selenium (and this program) to work. Check your Chrome settings (Settings > About Chrome) to find your version number, then [download and install the corresponding Web Driver](https://chromedriver.chromium.org/downloads).

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following dependencies.

```bash
pip install requests
pip install selenium
pip install beautifulsoup4

```
Requests is used to navigate to a specified URL.

Selenium allows Python to control the web browser.

BeautifulSoup is used to gather content from HTML elements on each webpage.


## Current limitations

Only the English language is supported. Some search functions include regular expressions limiting results to those containing Arabic numerals (0-9) and the English alphabet(A-Z, a-z).

Games containing Roman numerals may not appear if they are searched for with their Arabic numeral counterpart.

A change to the webpage of any storefront may break the functionality of the program entirely. An API should typically be used for this data gathering process, but this program was more of an academic exercise than a complete product.
