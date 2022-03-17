from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

class YahooFinanceScraper:
    @staticmethod
    def extract_info(soup):
        columns = soup.find('div', class_="D(tbhg)").find_all('span')
        rows = soup.find_all("div", "D(tbr) fi-row Bgc($hoverBgColor):h")

        getText = lambda lst: [x.text if x else None for x in lst]

        df = pd.DataFrame(columns = getText(columns))
        num_cols = len(columns)
        for row in rows:
            info = getText(row.find_all("div"))
            del info[2]
            del info[0]
            for i, val in enumerate(info):
                if val == "" or val == "-":
                    info[i] = None
                else:
                    val = val.replace(',','')
                    try:
                        if '.' in val:
                            info[i] = float(val)
                        else:
                            info[i] = int(val)
                    except:
                        pass
            if len(info) != num_cols:
                raise Exception("Invalid scraping")
            df.loc[len(df)] = info
        return df

    @staticmethod
    def retrieve_income_statement(ticker:str = "AAPL") -> pd.DataFrame:
        browser = webdriver.Edge("C:/Users/james/AppData/Local/Programs/Common/MicrosoftWebDriver.exe")
        browser.get(f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}')
        try:
            elem = browser.find_element(By.NAME, 'agree')  # Accept Cookies
            elem.click()
        except:
            pass
        WebDriverWait(browser, 3600).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Expand All']"))).click()

        html = browser.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html, 'lxml')
        return YahooFinanceScraper.extract_info(soup)

    @staticmethod
    def retrieve_balance_sheet(ticker:str = "AAPL") -> pd.DataFrame:
        browser = webdriver.Edge("C:/Users/james/AppData/Local/Programs/Common/MicrosoftWebDriver.exe")
        browser.get(f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}')
        try:
            elem = browser.find_element(By.NAME, 'agree')  # Accept Cookies
            elem.click()
        except:
            pass
        WebDriverWait(browser, 3600).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Expand All']"))).click()


        html = browser.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html, 'lxml')
        return YahooFinanceScraper.extract_info(soup)


def test_retrieve_aapl():
    df = YahooFinanceScraper.retrieve_income_statement('AAPL')
    print(df)
# test_retrieve_aapl()
# print(YahooFinanceScraper.retrieve_balance_sheet('AAPL'))