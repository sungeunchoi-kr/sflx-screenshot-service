import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from PIL import Image
import time


class Snapshotter:
    chrome_driver_path = None
    driver = None
    last_run_time = 0

    def __init__(self):
        chrome_options = Options()
        chrome_options.headless = True

        chrome_driver_path = os.environ.get('CHROME_DRIVER_PATH') or './chromedriver'

        print('Scraper: setting up driver.')
        self.driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
        print('Scraper: driver setup done.')

    ##
    # chart_descriptor: e.g. "charts-top:all-music:us"
    def soundcloud_charts(self, chart_descriptor, filepath):
        url = 'https://soundcloud.com/discover/sets/{}'.format(chart_descriptor)
        print('soundcloud_charts: getting page <{}>.'.format(url))
        self.driver.get(url)
        print('soundcloud_charts: got page <{}>.'.format(url))

        print('soundcloud_charts: taking screenshot.')

        # courtesy: <https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver/57338909#57338909>
        measure = lambda n: self.driver.execute_script('return document.body.parentNode.scroll' + n)
        self.driver.set_window_size(measure('Width'), measure('Height')) # May need manual adjustment
        time.sleep(3)
        self.driver.set_window_size(measure('Width'), measure('Height')) # May need manual adjustment
        time.sleep(3)
        self.driver.set_window_size(measure('Width'), measure('Height')) # May need manual adjustment

        el = self.driver.find_element_by_class_name('systemPlaylistTrackList')

        el.screenshot(filepath)

        print('soundcloud_charts: done.')

    def soundcloud_track_fullpage(self, url):
        url = 'https://soundcloud.com/{}'.format(url)
        print('soundcloud_charts: getting page <{}>.'.format(url))
        self.driver.get(url)
        print('soundcloud_charts: got page <{}>.'.format(url))

        print('soundcloud_charts: taking screenshot.')

        self.driver.screenshot(filepath)

        print('soundcloud_track_fullpage: done.')
