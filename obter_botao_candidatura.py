from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

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
    
    botao = encontrar_por_texto(driver)
    if botao:
        print(f"✅ Botão encontrado via 'encontrar_por_texto'")
        return botao

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