# MetaScraper

A simple [Selenium](https://www.selenium.dev/) scraper for [MetaFilter](https://www.metafilter.com/) user profiles. Requires [Chrome WebDriver](https://chromedriver.chromium.org/).

## Motivations

This tool is intended to make the archival of historic [MetaFilter](https://www.metafilter.com/) content more accessible. It can quickly and automatically scrape all of a user's site activity.

## Usage

1. Open `MetaScraper.py` in your text editor of choice, make sure to have Selenium installed
1. Set `PATH =`  the location of your Chrome Webdriver installation
1. Make `url =`  equal to the profile page of the user you are attempting to scrape
1. Run the script and the user's posts and comments will be output as two seperate .csv archives
