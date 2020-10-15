# Youtube Scraper
Youtube Scraper for videos and channels.

Video contents include link, title, channel, channel link, publish time, view count, description, and thumbnail image src.

Channel contents include link, name, subscriber count, video count, description, and thumbnail image src.

Thumbnail image src may be missing due to BeautifulSoup parsing problem.

## Installation

Install Selenium and beautifulsoup4
```
pip install selenium
pip install beautifulsoup4
```

Install [ChromeDriver - WebDriver for Chrome](http://chromedriver.chromium.org/downloadss)

## Example
```
keyword = 'Car'
page_count = 5
search_type = 'video'

df = scrape(keyword, page_count, search_type)
df.to_csv('Car_video.csv')
```
