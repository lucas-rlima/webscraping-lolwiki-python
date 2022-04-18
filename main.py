from attr import field
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import json

url = "https://leagueoflegends.fandom.com/wiki/List_of_champions/Base_statistics"

option = webdriver.ChromeOptions()
option.add_argument("--window-size=1366,768")
option.add_argument("--disable-extensions")
option.add_argument("--proxy-server='direct://'")
option.add_argument("--proxy-bypass-list=*")
option.add_argument("--start-maximized")
option.add_argument('--disable-gpu')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('--no-sandbox')
option.add_argument('--ignore-certificate-errors')
option.add_argument("--windows-size=19220,1080")
option.add_argument("--allow-insecure-localhost")
option.add_argument("--log-level=3")

driver = webdriver.Chrome(options=option)

top10ranking = {}

ranking = {
    'HP':{'field':'2','value':'HP'},
    'Alcance':{'field': '19','value':'Range'},
    'ADbase':{'field': '10','value':'AD'},
}

driver.get(url)

#Cookie
sleep(1.5)
driver.find_element(By.XPATH, "/html/body/div[9]/div/div/div[2]/div[2]").click()

#Encontrar tabela 
sleep(10)
elements = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/main/div[3]/div[2]/div[1]/h2[1]/span")
driver.execute_script("arguments[0].scrollIntoView()", elements)
""" 
actions = ActionChains(driver)
actions.move_to_element(elements).perform()
elements.click() """

def buildrank(type):
    field = ranking[type]['field']
    label = ranking[type]['value']
    
    #Organizando Tabela
    sleep(5)
    order = driver.find_element(By.XPATH, 
    f"/html/body/div[4]/div[3]/div[2]/main/div[3]/div[2]/div[1]/div[1]/div/div/table/thead/tr/th[{field}]")
    sleep(1.5)
    ActionChains(driver).move_to_element_with_offset(order, 37, 10).click().perform()

    #Recolher HTML da Tabela
    sleep(5)
    element = driver.find_element(By.XPATH, 
                        "/html/body/div[4]/div[3]/div[2]/main/div[3]/div[2]/div[1]/div[1]/div/div/table")
    element_html = element.get_attribute("outerHTML")


    #Parsear
    soup = BeautifulSoup(element_html, "html.parser")
    table = soup.find(name='table')

    #Remover Tags com DataFrame e Pandas
    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Champions',label]]

    driver.get(url)
    #converter para Dicionário
    return  df.to_dict('records')

for value in ranking:
    top10ranking[value] = buildrank(value)
driver.quit()

#converter e salvar JSON
js = json.dumps(top10ranking)
fp = open('lolwiki/ranking.json', 'w')
fp.write(js)
fp.close()



