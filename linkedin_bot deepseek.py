import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 🔑 Configuração da API do DeepSeek
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = "sk-8765069be0ee46b0a70fbb9e14e3dd6f"  # Obtenha em: https://platform.deepseek.com/

# Funções para localização do botão de candidatura
def encontrar_botao_candidatura(driver):
    """Busca o botão de candidatura usando múltiplos seletores CSS"""
    seletores = [
        "button.jobs-apply-button",
        "button[aria-label*='Candidatura simplificada']",
        "button[aria-label*='Apply']",
        "button[data-easy-apply*='true']",
        "button.jobs-s-apply",
        "button.jobs-apply-button--top-card",
        "button.artdeco-button--primary"
    ]
    
    for seletor in seletores:
        try:
            botao = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
            return botao
        except:
            continue
    return None

def encontrar_por_texto(driver):
    """Busca o botão analisando o texto visível"""
    padroes = [
        r"Candidatura\s*simplificada",
        r"Aplicar\s*agora",
        r"Apply\s*now",
        r"Quick\s*Apply",
        r"Enviar\s*candidatura"
    ]
    
    todos_botoes = driver.find_elements(By.TAG_NAME, "button")
    for botao in todos_botoes:
        texto = botao.text
        if any(re.search(padrao, texto, re.IGNORECASE) for padrao in padroes):
            return botao
    return None

def encontrar_por_hierarquia(driver):
    """Busca o botão através de containers conhecidos"""
    containers = [
        "div.jobs-apply-button--top-card",
        "div.jobs-s-apply",
        "div.job-details-jobs-unified-top-card__content"
    ]
    
    for container in containers:
        try:
            div_pai = driver.find_element(By.CSS_SELECTOR, container)
            botao = div_pai.find_element(By.CSS_SELECTOR, "button")
            if botao.is_displayed():
                return botao
        except:
            continue
    return None

def encontrar_por_data_attributes(driver):
    """Busca o botão através de atributos data-*"""
    atributos = [
        "data-easy-apply",
        "data-job-id",
        "data-test-apply-button"
    ]
    
    for attr in atributos:
        try:
            botao = driver.find_element(By.CSS_SELECTOR, f"button[{attr}]")
            return botao
        except:
            continue
    return None

def encontrar_via_javascript(driver):
    """Busca o botão via JavaScript como último recurso"""
    script = """
    const botoes = Array.from(document.querySelectorAll('button'));
    return botoes.find(btn => {
        const texto = btn.innerText.toLowerCase();
        return /(aplicar|apply|simplificada|quick)/.test(texto) && 
               getComputedStyle(btn).display !== 'none';
    })?.outerHTML || null;
    """
    
    elemento = driver.execute_script(script)
    if elemento:
        return driver.find_element(By.XPATH, "//button[contains(., 'Aplicar')]")
    return None

def localizar_botao_candidatura(driver):
    """Função consolidada que tenta todos os métodos sequencialmente"""
    metodos = [
        ("Seletores CSS", encontrar_botao_candidatura),
        ("Texto do Botão", encontrar_por_texto),
        ("Hierarquia DOM", encontrar_por_hierarquia),
        ("Atributos Data", encontrar_por_data_attributes),
        ("JavaScript", encontrar_via_javascript)
    ]
    
    for nome_metodo, metodo in metodos:
        try:
            botao = metodo(driver)
            if botao:
                print(f"✅ Botão encontrado via {nome_metodo}")
                return botao
        except Exception as e:
            print(f"⚠️ Erro no método {nome_metodo}: {str(e)[:50]}...")
            continue
    
    print("❌ Nenhum método encontrou o botão de candidatura")
    return None

def processar_candidatura(driver):
    """Função principal para tentar localizar e clicar no botão"""
    try:
        botao = localizar_botao_candidatura(driver)
        if botao:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
            time.sleep(1)
            botao.click()
            print("🖱️ Botão clicado com sucesso!")
            return True
        print("⚠️ Pulando vaga sem botão detectável")
        return False
    except Exception as e:
        print(f"🔥 Erro durante clique: {e}")
        return False

def obter_resposta_deepseek(pergunta):
    """Obtém resposta da API do DeepSeek para preenchimento de campos"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Você é um especialista em preenchimento de formulários de emprego."},
            {"role": "user", "content": pergunta}
        ]
    }
    try:
        resposta = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload).json()
        print(f"🔥 Resposta DeepSeek: {resposta}")
        return resposta["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Erro ao chamar DeepSeek API: {e}")
        return ""

def main():
    # Configuração do WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Acesso ao LinkedIn
        driver.get("https://www.linkedin.com/jobs/")
        print("🔍 Acessando LinkedIn Jobs...")
        input("👉 Faça login MANUALMENTE e pressione ENTER para continuar...")

        # Coleta de vagas
        vagas = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.job-card-container__link")))
        lista_de_vagas = [vaga.get_attribute("href") for vaga in vagas]
        print(f"📊 Total de vagas encontradas: {len(lista_de_vagas)}")

        # Processamento das vagas
        for i, link in enumerate(lista_de_vagas, 1):
            print(f"\n🔹 Processando vaga {i}/{len(lista_de_vagas)}: {link}")
            driver.get(link)
            time.sleep(3)

            if not processar_candidatura(driver):
                continue

            # Preenchimento do formulário
            campos = driver.find_elements(By.TAG_NAME, "input")
            for campo in campos:
                try:
                    pergunta = campo.get_attribute("aria-label") or campo.get_attribute("placeholder")
                    if pergunta and campo.is_displayed():
                        resposta = obter_resposta_deepseek(pergunta)
                        if resposta:
                            campo.clear()
                            campo.send_keys(resposta)
                            print(f"✏️ Campo '{pergunta[:20]}...' preenchido!")
                except Exception as e:
                    print(f"⚠️ Erro ao processar campo: {e}")

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

    except Exception as e:
        print(f"🔥 ERRO GRAVE: {e}")
    finally:
        driver.quit()
        print("🛑 Navegador fechado. Processo concluído!")

if __name__ == "__main__":
    main()