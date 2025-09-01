from cores import alterar_cor
from abrir_navegador import abrir_navegador
from processar_vagas import processar_vagas

def main():
    
    # Abre o navegador
    driver = abrir_navegador()

    try:

        # Processa as vagas
        processar_vagas(driver)

    except Exception as e:
        print(f"{alterar_cor("vermelho")}🔥 ERRO GRAVE: {e}")
    finally:
        driver.quit()
        print("🛑 Navegador fechado. Processo concluído!")

if __name__ == "__main__":
    main()