"""
src/pkg/srv_chart/client.py
---------------------------
All classes inherit from BaseScraper class

Class:
    HeatmapScraper(): https://stockanalysis.com/markets/heatmap/
    StockChartScraper(): https://stockcharts.com/sc3/ui/?s=AAPL
"""
import io, logging, os

from io import BytesIO
from time import sleep
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import urllib3

from PIL import Image

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    TimeoutException,
)


logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class BaseScraper:
    """"""
    def __init__(self, ctx):
        self.debug = ctx["debug"]
        self.base_url = ctx["url"]
        self.dir = f"{ctx['work_dir']}/{ctx['command']}"
        self.item_list = ctx["item_list"]
        self.opt = FirefoxOptions()
        self.opt.add_argument("--disable-notifications")
        self.opt.add_argument("--headless=new")
        self.opt.add_argument("--user-agent='Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0'")
        self.opt.page_load_strategy = "none"

    def __repr__(self):
        return f"<class '{self.__class__.__name__}'> __dict__= {self.__dict__})"

    def __del__(self):
        if self.debug:
            logger.debug(f"DELETE {self.__class__.__name__}()")


class HeatmapScraper(BaseScraper):
    """Get heatmap from https://stockanalysis.com/markets/heatmap/

        Functions:
            fetch_heatmap(): Main entry point to class. Directs workflow of webscraper
    """

    def __init__(self, ctx: dict):
        super().__init__(ctx=ctx)


    def fetch_heatmap(self):
        """Main entry point to class. Directs workflow of Webscraper"""
        if self.debug:
            logger.debug(f"fetch_heatmap(self={self})")

        for item in self.item_list:
            try:
                if not self.debug:
                    print(f"  setting url...", end="\r", flush=True)
                driver = Firefox(options=self.opt)
                mod_url = self._modify_heatmap_query_time_period(period=item)
                if not self.debug:
                    print(f"  fetching {item} heatmap...", end=" ")
                driver.get(mod_url)
                image_src = self._return_png_img_bytes(driver=driver)
                if not self.debug:
                    print("saving...", end=" ")
                self._save_png_image(image_src=image_src, period=item)
            except (
                ElementClickInterceptedException,
                ElementNotInteractableException,
                TimeoutException,
                Exception,
            ) as e:
                logger.error(f"*** Error *** {e}")
                return
            finally:
                driver.quit()
                if not self.debug:
                    print("done")


    def _modify_heatmap_query_time_period(self, period: str) -> str:
        """Use urllib.parse to modify the default query parameters
        with new heatmap, symbol"""
        parsed_url = urlparse(url=self.base_url)
        query_dict = parse_qs(parsed_url.query)
        query_dict["time"] = period.upper()
        encoded_params = urlencode(query_dict, doseq=True)
        url = urlunparse(parsed_url._replace(query=encoded_params))
        if self.debug:
            logger.debug(f"_modify_heatmap_query_time_period()-> {url}")
        return url


    def _return_png_img_bytes(self, driver: object) -> bytes:
        """Get the chart image source and convert the bytes to PNG image"""
        if self.debug:
            logger.debug(f"_return_png_img_bytes(driver{driver})")

        canvas_element = WebDriverWait(driver=driver, timeout=7).until(
            EC.presence_of_element_located(
                (
                    # By.XPATH,
                    # "/html/body/div/div[1]/div[2]/main/div[2]/div[1]/div/div/svg[1]")
                    By.CSS_SELECTOR,
                    "svg.main-svg:nth-child(1)",
                )
            )
        )
        loc = canvas_element.location_once_scrolled_into_view
        if self.debug:
            logger.debug(f"canvas_element: {canvas_element}, loc: {loc}")
        return canvas_element.screenshot_as_png


    def _save_png_image(self, image_src: bytes, period: str):
        """Save image to the work directory"""
        if self.debug:
            logger.debug(f"_save_png_image(image_src={type(image_src)}, period={period})")

        png_image = Image.open(BytesIO(image_src)).convert("RGB")
        png_image.save(os.path.join(self.dir, f"SP500_{period.upper()}.png"), "PNG", quality=80)


class StockChartScraper(BaseScraper):
    """Get stockchart from https://stockcharts.com/sc3/ui/?s=AAPL

        Functions:
            fetch_stockchart(): Main entry point to class. Directs workflow of webscraper
    """

    def __init__(self, ctx: dict):
        super().__init__(ctx=ctx)
        self.http = urllib3.PoolManager()
        self.period = ctx["period"]


    def fetch_stockchart(self):
        """Main entry point to class. Directs workflow of Webscraper"""
        if self.debug:
            logger.debug(f"fetch_stockchart(self={self})")

        try:
            driver = Firefox(options=self.opt)
            driver.get(self.base_url)
            if not self.debug:
                print(f"  setting url...", end="\r", flush=True)
            self._set_indicator_RSI(driver=driver)
            self._set_chart_size_landscape(driver=driver)
            self._set_chart_color_dark(driver=driver)
            # self._click_update_button(driver=driver)
            self.url = self._get_chart_src_attribute(driver=driver)
        except (
            ElementClickInterceptedException,
            ElementNotInteractableException,
            TimeoutException,
            Exception
        ) as e:
            logger.debug(f"*** Error *** {e}")
            return
        finally:
            driver.quit()

        for item in self.item_list:
            for period in self.period:
                if not self.debug:
                    print(f"  fetching {item} {period}...", end=" ")
                mod_url = self._modify_chart_query_period_and_symbol(chart=item, period=period)
                if not self.debug:
                    print("saving...", end=" ")
                self._get_img_src_convert_bytes_to_png_and_save(url=mod_url, period=period, symbol=item)


    def _set_chart_color_dark(self, driver: object):
        """set color to night"""
        color_element = WebDriverWait(driver=driver, timeout=3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="chart-settings-color-scheme-menu"]'))
        )
        loc = color_element.location_once_scrolled_into_view
        if self.debug:
            logger.debug(f"color_element: {color_element}, loc: {loc}")

        color = Select(color_element)
        color.select_by_value("night")
        if self.debug:
            logger.debug(f"color: {color}")


    def _set_chart_size_landscape(self, driver: object):
        """set chart size to Landscape"""
        size_element = WebDriverWait(driver=driver, timeout=3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="chart-settings-chart-size-menu"]'))
        )
        loc = size_element.location_once_scrolled_into_view
        if self.debug:
            logger.debug(f"size_element: {size_element}, loc: {loc}")

        size = Select(size_element)
        size.select_by_value("Landscape")
        if self.debug:
            logger.debug(f"size: {size}")


    def _set_indicator_RSI(self, driver: object):
        """set indicator overlay to RSI"""
        indicator_element = WebDriverWait(driver=driver, timeout=3).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#indicator-menu-1",
                    # By.XPATH,
                    # '//*[@id="indicator-menu-1"]'
                )
            )
        )
        loc = indicator_element.location_once_scrolled_into_view
        if self.debug:
            logger.debug(f"indicator_element: {indicator_element}, loc: {loc}")

        indicator = Select(indicator_element)
        indicator.select_by_value("RSI")
        if self.debug:
            logger.debug(f"indicator: {indicator}")


    def _get_chart_src_attribute(self, driver: object) -> str:
        """modify base_url, set size, color, and RSI indicator, return modified base_url"""
        sleep(1)
        try:
            img_element = WebDriverWait(driver=driver, timeout=3).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "#chart-image",
                        # By.XPATH,
                        # '//*[@id="chart-image"]'
                    )
                )
            )
            loc = img_element.location_once_scrolled_into_view
            if self.debug:
                logger.debug(f"img_element: {img_element}, loc: {loc}")
            return img_element.get_attribute("src")
        except Exception as e:
            logger.debug(f"an error occured while getting chart source url: {e}")
            url = input(" Input chart source url manually or press enter to exit:")
            if url:
                return url
            else:
                SystemExit


    def _get_img_src_convert_bytes_to_png_and_save(self, url: str, period: str, symbol: str):
        """Get the chart image source and convert the bytes to
        a .png image then save to the chart work directory.
        """
        if self.debug:
            logger.debug(f"_get_img_src_convert_bytes_to_png_and_save(url={url} {type(url)})")

        image_src = self.http.request("GET", url, headers={"User-agent": "Mozilla/5.0"})
        image = Image.open(io.BytesIO(image_src.data)).convert("RGB")
        image.save(os.path.join(self.dir, f"{symbol}_{period[:1].lower()}.png"), "PNG", quality=80)


    def _modify_chart_query_period_and_symbol(self, chart: str, period: str) -> str:
        """Use urllib.parse to modify the default query parameters
        with new chart, period
        """
        if self.debug:
            logger.debug(f"_modify_chart_query_period_and_symbol(chart={chart} {type(chart)}, period={period} {type(period)})")

        parsed_url = urlparse(url=self.url)
        query_dict = parse_qs(parsed_url.query)
        if period != "Daily":
            query_dict["p"] = period[0]
            query_dict["yr"] = "5"
        query_dict["s"] = chart
        encoded_params = urlencode(query_dict, doseq=True)
        url = urlunparse(parsed_url._replace(query=encoded_params))
        if self.debug:
            logger.debug(f"_modify_chart_query_period_and_symbol()-> {url}")
        return url


    def _click_update_button(self, driver: object):
        """click refresh chart"""
        try:
            button = WebDriverWait(driver=driver, timeout=3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[1]/div[2]/div[5]/div[2]/div[1]/div[1]/div[3]/button[1]")
                )
            )
            loc = button.location_once_scrolled_into_view
        except Exception as e:
            logger.debug(
                f"_click_update_button(self, driver)\nExpected condition element to be clickable not met.\n{e} Trying alternate XPATH.\n"
            )
            try:
                button = WebDriverWait(driver=driver, timeout=3).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "/html/body/div[1]/div[2]/div[6]/div[2]/div[1]/div[1]/div[3]/button[1]")
                    )
                )
                loc = button.location_once_scrolled_into_view
            except Exception as e:
                logger.debug(f"_click_update_button(self={self}, driver={driver}) {e}")
        finally:
            if self.debug:
                logger.debug(f"button: {button}, loc: {loc}")
            button.click()
