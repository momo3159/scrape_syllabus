import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


def initDriver(options):
  return webdriver.Chrome(options=options)

def setWait(driver, time):
  return WebDriverWait(driver, time)

def selectByValueWithWait(value, wait, finder):
  select = Select(wait.until(finder))
  select.select_by_value(value)
  # イベントハンドラによってHTMLがリロードされるため, waitする（これがない場合, element is not attached to the page documentが出る）
  return Select(wait.until(finder))

def clickBtnWithWait(wait, finder):
  btn = wait.until(finder)
  btn.click()
  return wait.until(finder)
