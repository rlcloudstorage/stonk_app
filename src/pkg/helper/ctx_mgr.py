"""
src/pkg/helper/ctx_mgr.py
-------------------------
All classes inherit from BaseProcessor class

Class:
    SpinnerManager(): Context manager for CLI spinner object
    SqliteConnectManager(): Context manager for Sqlite3 database
"""

import logging
import os


logger = logging.getLogger(__name__)


class SpinnerManager:
    """Context manager for CLI spinner object
    -----------------------------------------
    Parameters
    ----------
    `debug` : bool
    `delay` : float
        default is 0.2\n
    Returns
    -------
    context manager\n
    """
    import sys
    import threading
    from time import sleep

    busy = False
    # delay = 0.2

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in "|/-\\":
                yield cursor

    def __init__(self, debug: bool, delay: float=None):
        self.debug = debug
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay):
            self.delay = delay
        elif not delay:
            self.delay = 0.2

    def spinner_task(self):
        while self.busy:
            self.sys.stdout.write(next(self.spinner_generator))
            self.sys.stdout.flush()
            self.sleep(self.delay)
            self.sys.stdout.write("\b")
            self.sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        if self.debug:
            logger.debug("SpinnerManager().__enter__()")
        self.threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        self.sleep(self.delay)
        if self.debug:
            logger.debug("SpinnerManager().__exit__()")
        if exception is not None:
            return False


class SqliteConnectManager:
    """Context manager for Sqlite3 database
    ------------------------------------
    Commits changes on exit.\n
    Parameters
    ----------
    `ctx` : dict
        dictionary containing various default settings\n
    `mode` : string
        open database for read-only 'ro', read-write 'rw', \n
        read-write-create 'rwc', or 'memory' for in-memory db\n
    Returns
    -------
    context manager\n
    """
    import sqlite3

    def __init__(self, ctx: dict, mode: str = "ro"):
        self.debug = ctx["debug"]
        self.db_path = ctx["database"]
        self.mode = mode

    def __repr__(self):
        return f"{self.__class__.__name__}(db_path='{self.db_path}', mode='{self.mode}')"

    def __enter__(self):
        if self.debug:
            logger.debug(f"{self}.__enter__()")
        try:
            self.connection = self.sqlite3.connect(
                f"file:{os.path.abspath(self.db_path)}?mode={self.mode}",
                detect_types=self.sqlite3.PARSE_DECLTYPES | self.sqlite3.PARSE_COLNAMES,
                uri=True,
            )
            self.cursor = self.connection.cursor()
            if self.debug:
                logger.debug(f"cursor: {self.cursor}")
            return self
        except self.sqlite3.Error as e:
            print(f"{e}: {self.db_path}")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.debug:
            logger.debug(f"{self.__class__.__name__}.__exit__()")
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()


# class WebDriverManager:
#     """Manage Selenium WebDriver.\n
#     Put Firefox geckodriver somewhere on sysetm path.
#     """
#     # from selenium.webdriver import Chrome
#     # from selenium.webdriver import ChromeOptions
#     from selenium.webdriver import Firefox
#     from selenium.webdriver import FirefoxOptions

#     def __init__(self, debug: bool):
#         # self.opt = self.ChromeOptions()
#         self.opt = self.FirefoxOptions()
#         self.opt.add_argument("--headless=new")
#         # self.opt.add_argument("--user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'")
#         self.opt.add_argument("--user-agent='Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0'")
#         # self.opt.page_load_strategy = "eager"
#         self.opt.page_load_strategy = "none"

#     def __enter__(self):
#         # self.driver = self.Chrome(options=self.opt)
#         self.driver = self.Firefox(options=self.opt)
#         if DEBUG: logger.debug(f'{self.__class__.__name__}.__enter__(session={self.driver.session_id})')
#         # Install ad blocker if used
#         # if os.path.exists(ADBLOCK):
#         #     self.driver.install_addon(ADBLOCK)
#         #     pyautogui.PAUSE = 2.5
#         #     pyautogui.click()  # position browser window
#         #     pyautogui.hotkey('ctrl', 'w')  # close ADBLOCK page
#         return self.driver

#     def __exit__(self, exc_type, exc_value, exc_traceback):
#         self.driver.quit()
#         if DEBUG: logger.debug(f'{self.__class__.__name__}.__exit__({self.driver.session_id})')
