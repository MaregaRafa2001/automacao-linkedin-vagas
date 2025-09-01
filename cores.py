def alterar_cor(cor="reset"):
    cores = {
        "vermelho": "\033[91m",
        "verde": "\033[92m",
        "amarelo": "\033[93m",
        "azul": "\033[94m",
        "reset": "\033[0m"
    }
    return cores.get(cor.lower(), cores["reset"])
