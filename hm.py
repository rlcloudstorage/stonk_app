class WebScraper:

    def __repr__(self):
        return f"<class '{self.__class__.__name__}'> __dict__= {self.__dict__})"

    def webscraper(self):
        """Main entry point to class. Directs workflow of webscraper."""
        if DEBUG:
            logger.debug(f"webscraper(self={self})")

        opt = FirefoxOptions()
        opt.add_argument("--headless=new")
        opt.add_argument("--user-agent='Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0'")
        opt.page_load_strategy = "none"

        for period in self.period:
            if not DEBUG:
                print(f"  fetching heatmap {period}...")
            try:
                driver = Firefox(options=opt)
                mod_url = self._modify_query_time_period(period=period)
                driver.get(mod_url)
                image_src = self._get_png_img_bytes(driver=driver)
                self._save_png_image(image_src=image_src, period=period)
            except (
                ElementClickInterceptedException,
                ElementNotInteractableException,
                TimeoutException,
                Exception,
            ) as e:
                logger.debug(f"*** ERROR *** {e}")
            finally:
                driver.quit()
