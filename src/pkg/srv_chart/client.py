"""
src/pkg/srv_chart/client.py
--------------------------
Select data provider, create database, download data

Functions:
    download_and_parse_ohlc_data(): save OHLC price and volume data
    download_and_parse_signal_data(): save signal data
"""
import logging


logger = logging.getLogger(__name__)


from datetime import date
from io import BytesIO
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

# from PIL import Image

# # TODO add Chrome/Firefox option
# # from selenium.webdriver import Chrome, ChromeOptions
# from selenium.webdriver import Firefox, FirefoxOptions
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import (
#     ElementClickInterceptedException,
#     ElementNotInteractableException,
#     TimeoutException,
# )

logging.getLogger("PIL").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class BaseScraper:
    """Fetch and save heatmaps from stockanalysis.com"""

    def __init__(self, ctx: dict):
        self.debug = ctx["debug"]
        self.driver = self._webdriver
        self.url = ctx["url"]
        self.work_dir = ctx["work_dir"]

    @property
    def _webdriver(self):
        """"""
        # # opt = ChromeOptions()
        # opt = FirefoxOptions()
        # opt.add_argument("--headless=new")
        # # opt.add_argument("--user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'")
        # opt.add_argument("--user-agent='Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0'")
        # # opt.page_load_strategy = "eager"
        # opt.page_load_strategy = "none"
        # try:
        #     # driver = Chrome(options=opt)
        #     driver = Firefox(options=opt)
        # except (
        #     ElementClickInterceptedException,
        #     ElementNotInteractableException,
        #     TimeoutException,
        #     Exception,
        # ) as e:
        #     logger.debug(f"*** Error *** {e}")

        return None


    def start_heatmap_download(self):
        """"""
        if self.debug:
            logger.debug(f"start_heatmap_download(self={type(self)})")
        self._webscraper()


class HeatmapScraper(BaseScraper):
    """Fetch S&P heatmaps from stockanalysis.com"""

    def __init__(self, ctx: dict):
        super().__init__(ctx=ctx)
        self.heatmap_pool = ctx['heatmap_pool']


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"debug={self.debug}, "
            f"driver={self.driver}, "
            f"heatmap_pool={self.heatmap_pool}, "
            f"url={self.url}, "
            f"work_dir={self.work_dir})"
        )


    def _webscraper(self) -> None:
        """Direct workflow of webscraper"""
        if self.debug:
            logger.debug(f"_webscraper(self={self})")

        for period in self.heatmap_pool:
            if self.debug:
                print(f"  fetching heatmap {period}...")
    #         try:
    #             # driver = Chrome(options=opt)
    #             driver = Firefox(options=opt)
    #             mod_url = self._modify_query_time_period(period=period)
    #             driver.get(mod_url)
    #             image_src = self._get_png_img_bytes(driver=driver)
    #             self._save_png_image(image_src=image_src, period=period)
    #         except (
    #             ElementClickInterceptedException,
    #             ElementNotInteractableException,
    #             TimeoutException,
    #             Exception,
    #         ) as e:
    #             logger.debug(f"*** ERROR *** {e}")
    #         finally:
    #             driver.quit()

    # def _modify_query_time_period(self, period: str) -> str:
    #     """Use urllib.parse to modify the default query parameters
    #     with new period, symbol."""
    #     parsed_url = urlparse(url=self.base_url)
    #     query_dict = parse_qs(parsed_url.query)
    #     query_dict["time"] = period
    #     encoded_params = urlencode(query_dict, doseq=True)
    #     url = urlunparse(parsed_url._replace(query=encoded_params))
    #     if DEBUG:
    #         logger.debug(f"_modify_query_time_period()-> {url}")
    #     return url

    # def _get_png_img_bytes(self, driver: object) -> bytes:
    #     """Get the chart image source and convert the bytes to PNG image"""
    #     if DEBUG:
    #         logger.debug(f"_get_png_img_bytes(driver{driver})")

    #     canvas_element = WebDriverWait(driver=driver, timeout=10).until(
    #         EC.presence_of_element_located(
    #             (
    #                 # By.XPATH,
    #                 # "/html/body/div/div[1]/div[2]/main/div[2]/div[1]/div/div/svg[1]")
    #                 By.CSS_SELECTOR,
    #                 "svg.main-svg:nth-child(1)",
    #             )
    #         )
    #     )
    #     loc = canvas_element.location_once_scrolled_into_view
    #     if DEBUG:
    #         logger.debug(f"canvas_element: {canvas_element}, loc: {loc}")
    #     return canvas_element.screenshot_as_png

    # def _save_png_image(self, image_src: bytes, period: str):
    #     """Save image to the work directory"""
    #     if DEBUG:
    #         logger.debug(f"_save_png_image(image_src={type(image_src)}, period={period})")

    #     today = str(date.today())
    #     png_image = Image.open(BytesIO(image_src)).convert("RGB")
    #     png_image.save(os.path.join(self.heatmap_dir, f"SP500_{period.lower()}_{today.replace('-', '')}.png"), "PNG", quality=80)
