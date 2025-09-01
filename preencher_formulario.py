import re
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from obter_resposta import obter_resposta

# Preenchimento do formulário
def preencher_formulario(driver):

    modal = abrir_modal(driver)

    textos = [r"Avançar", r"Avancar", r"Revisar"]
    botaoAvancar = obter_botao_por_texto(modal, textos)
    
    while (botaoAvancar):

        campos = modal.find_elements(By.CSS_SELECTOR, "input, select, textarea")

        # Percorre os campos e exibe informações
        for i, campo in enumerate(campos):
            try:

                # Processa o campo por tipo de input
                processar_campo(i, campo, modal)

            except Exception as e:
                print(f"⚠️ Erro ao processar campo {i+1}: {e}")
        
        botaoAvancar.click()
        
        # Botão Avançar
        botaoAvancar = obter_botao_por_texto(modal, textos)

        time.sleep(1)
    
    # Enviar candidatura
    textos = [r"Enviar\s*candidatura"]
    botaoEnviarCandidatura = obter_botao_por_texto(modal, textos)

    botaoEnviarCandidatura.click()    


def abrir_modal(driver):
    try:
        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test-modal].jobs-easy-apply-modal"))
        )
        print("✅ Modal de candidatura encontrado")
    except:
        print("❌ Modal de candidatura não encontrado")
        return False

    modal = driver.find_element(By.CLASS_NAME, "jobs-easy-apply-modal")
    driver.execute_script("arguments[0].scrollIntoView();", modal)
    return driver


def processar_campo(i, campo, modal):
    
    tipo = campo.get_attribute("type")  # Tipo do input
    valor = campo.get_attribute("value")  # Valor já preenchido
    pergunta = obter_pergunta(campo, modal) # Pergunta associada ao campo


    print(f"📌 Campo {i+1}:")
    print(f"   🔹 Tipo: {tipo}")
    print(f"   🏷️ Pergunta: {pergunta}")
    print(f"   ✏️ Valor Atual: {valor}\n")

    if not validar_pergunta(pergunta):
        return

     # 1. Campo de SELEÇÃO (Dropdown)
    if tipo == "select-one":
        processar_campo_select_one(campo, pergunta)
        
    # 2. Campo de TEXTO/NÚMERO
    elif tipo in ["text", "number", "email", "tel"]:
        processar_campo_texto_numero(campo, pergunta)
        
    # 3. Checkbox ou Radio
    elif tipo in ["checkbox", "radio"]:
        processar_campo_checkbox(campo, pergunta, modal)

    # 4. Textarea (para campos de texto longo)
    elif tipo == "textarea":
        processar_campo_textarea(campo, pergunta)





def obter_pergunta(campo, modal):
    try:
        id_campo = campo.get_attribute("id")
        if not id_campo:
            return ""
        
        label = modal.find_element(By.CSS_SELECTOR, f"label[for='{id_campo}']")
        return label.text.strip()
    except:
        return ""


perguntas_sem_respostas = [
    "Configurar alerta",
    '',
    
]

def validar_pergunta(pergunta):
    if pergunta == '' or pergunta == 'pt-br':
        return False
    return True





def processar_campo_select_one(campo, pergunta):
    select = Select(campo)
    valor = campo.get_attribute("value")
    opcoes = [opcao.text for opcao in select.options if opcao.text]
    
    if valor != "Brazil (+55)": 
        if opcoes:
            resposta = obter_resposta(f"{pergunta} (aswer one of this options: {opcoes} )").strip().lower()  # Obtém e normaliza a resposta    
            for i, opcao in enumerate(select.options):
                if resposta.strip().lower() == opcao.text.strip().lower():  # Comparação insensível a maiúsculas/minúsculas
                    select.select_by_visible_text(opcao.text.strip())  # Seleciona a opção correta
                    print(f"  ✅ Selecionado: '{opcao.text.strip()}'")

def processar_campo_texto_numero(campo, pergunta):    
    id_attr = campo.get_attribute("id")

    if "numeric" in id_attr.lower():
        resposta = obter_resposta(f"{pergunta} - Answer with a numeric value")

    else:
        resposta = obter_resposta(pergunta)
        if resposta:
            campo.clear()
            campo.send_keys(resposta)
            print(f"  ✅ Preenchido: '{resposta[:20]}...'") 



def processar_campo_checkbox(campo, pergunta, modal):
    resposta = obter_resposta(f"{pergunta} (Responda 'sim' ou 'não')")
    if "sim" in resposta.lower() and not campo.is_selected():
        campo.click()
        modal.execute_script("arguments[0].click();", campo)
        print("   ✅ Marcado como 'Sim' ")  

def processar_campo_textarea(campo, pergunta):
    resposta = obter_resposta(pergunta)
    if resposta:
        campo.clear()
        campo.send_keys(resposta)
        print(f"   ✅ Texto longo preenchido: '{resposta[:20]}...'")    






def obter_botao_por_texto(modal, textos):
    
    todos_botoes = modal.find_elements(By.TAG_NAME, "button")
    for botao in todos_botoes:
        texto = botao.text
        if any(re.search(padrao, texto, re.IGNORECASE) for padrao in textos):
            return botao
    return None