import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from obter_botao_candidatura import localizar_botao_candidatura
from preencher_formulario import preencher_formulario


# Coleta de vagas
def coletar_vagas(driver):
    vagas = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.job-card-container__link"))
    )
    lista_de_vagas = [vaga.get_attribute("href") for vaga in vagas]
    print(f"📊 Total de vagas encontradas: {len(lista_de_vagas)}")
    return lista_de_vagas

def processar_candidatura(driver):
    """Função principal para tentar localizar e clicar no botão"""
    try:
        botao = localizar_botao_candidatura(driver)
        if botao:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
            botao.click()
            print("🖱️ Botão clicado com sucesso!")
            return True
        print("⚠️ Pulando vaga sem botão detectável")
        return False
    except Exception as e:
        print(f"🔥 Erro durante clique: {e}")
        return False

# Processamento das vagas
def processar_vagas(driver):

    lista_de_vagas = coletar_vagas(driver)

    for i, link in enumerate(lista_de_vagas, 1):
        print(f"\n🔹 Processando vaga {i}/{len(lista_de_vagas)}: {link}")
        driver.get(link)
        time.sleep(1)

        if not processar_candidatura(driver):
            continue

        # Preenchimento do formulário
        preencher_formulario(driver)

        # Navegação pelas etapas
        try:
            while True:
                next_btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Avançar')]")))
                next_btn.click()
                time.sleep(1)
        except:
            print("➡️ Todas as etapas concluídas")

        # Envio final
        try:
            submit_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Enviar candidatura')]")))
            submit_btn.click()
            print(f"🎉 Candidatura enviada para {link}")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Erro ao enviar candidatura: {e}")