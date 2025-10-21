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
        driver = Firefox(options=opt)
        driver.get(self.base_url)

        try:
            self._set_indicator_RSI(driver=driver)
            self._set_chart_size_landscape(driver=driver)
            self._set_chart_color_dark(driver=driver)
            # self._click_update_button(driver=driver)
            self.url = self._get_chart_src_attribute(driver=driver)
            driver.quit()
            self._fetch_stockchart(url=self.url)
        except (
            ElementClickInterceptedException,
            ElementNotInteractableException,
            TimeoutException,
            Exception
        ) as e:
            logger.debug(f"*** ERROR *** {e}")
        # finally:
        #     driver.quit()
