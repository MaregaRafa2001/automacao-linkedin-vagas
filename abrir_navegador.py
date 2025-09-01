from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

 # Abre o navegador
def abrir_navegador():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Acesso ao LinkedIn
    acessar_linkedin(driver)

    return driver
    

# Acesso ao LinkedIn
def acessar_linkedin(driver):
    driver.get("https://www.linkedin.com/jobs/")
    input("\033[94m👉 Faça login MANUALMENTE e pressione ENTER para continuar...")