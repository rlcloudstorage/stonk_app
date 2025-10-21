"""src/pkg/chart_srv/scraper/heat_map.py\n
Use selenium, create a webdriver, update query time value in\n
base_url with urllib parse. Get image source bytes then save\n
PNG image to work directory.
"""

import logging, logging.config
import os

from io import BytesIO
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from PIL import Image

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    TimeoutException,
)


logging.config.fileConfig(fname="src/logger.ini")
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


ctx = {
    'debug': True,
    'heatmap_pool': ['1d'],
    'command': 'heatmap',
    'url': 'https://stockanalysis.com/markets/heatmap/',
    'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
}


class WebScraper:
    """Fetch and save heatmaps from stockanalysis.com"""

    def __init__(self, ctx):
        self.debug = ctx["debug"]
        self.base_url = ctx["url"]
        self.heatmap_pool = ctx["heatmap_pool"]
        self.work_dir = ctx["work_dir"]

    def __repr__(self):
        return f"<class '{self.__class__.__name__}'> __dict__= {self.__dict__})"

    def fetch_heatmap(self):
        """Main entry point to class. Directs workflow of Webscraper."""
        if self.debug:
            logger.debug(f"fetch_heatmap(self={self})")

        opt = FirefoxOptions()
        opt.add_argument("--headless=new")
        opt.add_argument("--user-agent='Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0'")
        opt.page_load_strategy = "none"
        driver = Firefox(options=opt)

        for heatmap in self.heatmap_pool:
            print(f"  fetching heatmap {heatmap}...")
            try:
                mod_url = self._modify_query_time_period(heatmap=heatmap)
                driver.get(mod_url)
                image_src = self._get_png_img_bytes(driver=driver)
                self._save_png_image(image_src=image_src, heatmap=heatmap)
            except (
                ElementClickInterceptedException,
                ElementNotInteractableException,
                TimeoutException,
                Exception,
            ) as e:
                logger.debug(f"*** Error *** {e}")
            finally:
                driver.quit()

    def _modify_query_time_period(self, heatmap: str) -> str:
        """Use urllib.parse to modify the default query parameters
        with new heatmap, symbol."""
        parsed_url = urlparse(url=self.base_url)
        query_dict = parse_qs(parsed_url.query)
        query_dict["time"] = heatmap.upper()
        encoded_params = urlencode(query_dict, doseq=True)
        url = urlunparse(parsed_url._replace(query=encoded_params))
        if self.debug:
            logger.debug(f"_modify_query_time_period()-> {url}")
        return url

    def _get_png_img_bytes(self, driver: object) -> bytes:
        """Get the chart image source and convert the bytes to PNG image"""
        if self.debug:
            logger.debug(f"_get_png_img_bytes(driver{driver})")

        canvas_element = WebDriverWait(driver=driver, timeout=10).until(
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

    def _save_png_image(self, image_src: bytes, heatmap: str):
        """Save image to the work directory"""
        if self.debug:
            logger.debug(f"_save_png_image(image_src={type(image_src)}, heatmap={heatmap})")

        png_image = Image.open(BytesIO(image_src)).convert("RGB")
        png_image.save(os.path.join(self.work_dir, f"SP500_{heatmap.upper()}.png"), "PNG", quality=80)


def main(ctx: dict):
    logger.debug(f"main(ctx={ctx})")
    webscraper = WebScraper(ctx=ctx)
    webscraper.fetch_heatmap()


if __name__ == "__main__":
    logger.debug(f"******* START - beta/beta.py *******")

    main(ctx=ctx)
