from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape(keyword: str, page_count: int, search_type: str = 'video'):
    """
    Searches for Youtube videos or channels and returns several pages' results.
    Video contents include link, title, channel, channel link, publish time, view count, description, and thumbnail image src.
    Channel contents include link, name, subscriber count, video count, description, and thumbnail image src.
    Thumbnail image src may be missing due to BeautifulSoup parsing problem.

    :param keyword: string of keyword
    :type keyword: str
    :param page_count: count for scrolling pages
    :type page_count: int
    :param search_type: type of searching, 'video' or 'channel'
    :type search_type: str
    :return: df: DataFrame containing search results
    :rtype df: DataFrame
    """

    # Check parameter types
    if type(keyword) != str:
        raise ValueError("keyword must be a string")
    if type(page_count) != int:
        raise ValueError("page_count must be an integer")
    if search_type not in ['video', 'channel']:
        raise ValueError("Please choose search_type between video and channel")

    driver = webdriver.Chrome()
    driver.maximize_window()

    # Navigate to url
    if search_type == 'video':
        driver.get('https://www.youtube.com/results?search_query={}&sp=CAMSAhAB'.format(keyword))
    elif search_type == 'channel':
        driver.get('https://www.youtube.com/results?search_query={}&sp=CAMSAhAC'.format(keyword))

    # Scroll page to get more results
    for i in range(1, page_count):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1)  # wait until contents show up

    time.sleep(2)

    # Parse page source and search elements
    soup = BeautifulSoup(driver.page_source, "html.parser")
    if search_type == 'video':
        contents = ['link', 'title', 'channel', 'channel_link', 'publish_time', 'view_count', 'view_count_simple',
                    'description', 'img']
        df = pd.DataFrame(columns=contents)
        for i in soup.select("ytd-video-renderer"):
            # for every video, search and get above contents
            link = 'https://www.youtube.com' + i.find("a", {"id": "video-title"})['href']
            title = i.find("a", {"id": "video-title"})['title']
            aria = i.find("a", {"id": "video-title"})['aria-label'].split(' ')
            view_count = aria[-2]
            channel = i.find("div", {"id": "tooltip"}).text.replace('\n', '').strip()
            channel_link = 'https://www.youtube.com' + i.find("div", {"id": "channel-info"}).find("a")['href']
            metadata = i.find("div", {"id": "metadata-line"}).text.strip('\n').split('\n')
            if len(metadata) == 2:
                view_count_simple = metadata[0].strip(' views')
                publish_time = metadata[1]
            else:
                view_count_simple = ''
                publish_time = ''
            description = i.find("yt-formatted-string", {"id": "description-text"}).text
            # sometimes BeautifulSoup can't parse out img src
            try:
                img = "https:" + i.find("img")['src']
            except:
                img = ''
            df.loc[len(df)] = [link, title, channel, channel_link, publish_time, view_count, view_count_simple,
                               description, img]
    elif search_type == 'channel':
        contents = ['link', 'name', 'subscriber', 'video_count', 'description', 'img']
        df = pd.DataFrame(columns=contents)
        for i in soup.select("ytd-channel-renderer"):
            # for every channel, search and get above contents
            link = "https://www.youtube.com" + i.select(".yt-simple-endpoint")[0]["href"].strip() + "/about"
            name = i.select(".ytd-channel-name")[0].text.replace('\n', '').strip()
            name = name.split('    ')[0]
            subscriber = i.find("span", {"id": "subscribers"}).text
            video_count = i.find("span", {"id": "video-count"}).text
            description = i.find("yt-formatted-string", {"id": "description"}).text
            # sometimes BeautifulSoup can't parse out img src
            try:
                img = "https:" + i.find("img")['src']
            except:
                img = ''
            df.loc[len(df)] = [link, name, subscriber, video_count, description, img]
    return df


if __name__ == "__main__":
    keyword = 'Car'
    page_count = 5
    search_type = 'video'

    df = scrape(keyword, page_count, search_type=search_type)

    # Saving to CSV file
    filename = keyword + '_' + search_type + '.csv'
    df.to_csv(filename)
    print('saved to', filename)
