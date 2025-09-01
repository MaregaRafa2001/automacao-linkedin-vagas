import ollama
import difflib

# Dicionário de fallback para perguntas comuns
respostas_fallback = {
    "C#": "8",
    "Year": "8",
    "Work": "8",
    "Years": "8",
    "State": "SP",
    "Career": "8",
    "Python": "8",
    "Resume": "Sim",
    "Experience": "8",
    "Country": "Brasil",
    "Last Name": "Marega",
    "First Name": "Rafael",
    "English": "Professional",
    "City": "São Paulo, Brasil",
    "Full Name": "Rafael Marega",
    "ZIP Postal Code": "04279035",
    "Salary Expectation": "10000",
    "Phone Number": "11980569410",
    "Email": "rafaelmarega1@gmail.com",
    "E-mail": "rafaelmarega1@gmail.com",
    "Street": "Rua Malvina Ferrara Samarone",
    "Availability": "Full (remote or on-site)",
    "Profile": "www.linkedin.com/in/rafael-marega",
    "LinkedIn": "www.linkedin.com/in/rafael-marega"
}

"\n".join([f"{k}: {v}" for k, v in respostas_fallback.items()])

# Prompt
system_prompt = """You are a job candidate with 8 years of experience in IT.

You are a job candidate with 8 years of experience in IT.

Respond to the user's question with:
- A SINGLE, CONCRETE ANSWER (numbers or 'Yes' only)
- EXTREMELY SHORT (max 2 words)
- NO explanations
- IF ASKED ABOUT EXPERIENCE IN YEARS, ALWAYS ANSWER '8'
- IF ASKED A YES/NO QUESTION, ALWAYS ANSWER 'Yes'
- DO NOT add extra words or punctuation

Candidate Information:
    Street: Rua Malvina Ferrara Samarone,
    City: São Paulo, Brasil,
    State: SP,
    ZIP Postal Code: 04279035,
    Country: Brasil
    LinkedIn Profile: www.linkedin.com/in/rafael-marega
    Experience: 8
"""

def obter_resposta(pergunta):
    try:
        
        if (pergunta == ""):
            return ""

        pergunta_lower = pergunta.lower()

        # 1. Tenta encontrar correspondência direta (contém a chave na pergunta)
        for key in respostas_fallback:
            if key.lower() in pergunta_lower:
                print(f"✅ Resposta Fallback: {respostas_fallback[key]}")
                return respostas_fallback[key]

        # 2. Se não achou, tenta por similaridade
        correspondencias = difflib.get_close_matches(
            pergunta_lower,
            [key.lower() for key in respostas_fallback.keys()],
            n=1,
            cutoff=0.2
        )

        if correspondencias:
            for key in respostas_fallback:
                if key.lower() == correspondencias[0]:
                    print(f"✅ Resposta Fallback: {respostas_fallback[key]}")
                    return respostas_fallback[key]

        
        # Se não encontrou no fallback, usa o Ollama com prompt restritivo
        resposta = ollama.chat(
            model="deepseek-coder",
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"Pergunta: {pergunta}\nResposta direta:"}
            ],
            options={
                'temperature': 0,  # Totalmente determinístico
                'num_predict': 32  # Resposta muito curta
            }
        )

        print(f"✅ Resposta DeepSeek: {resposta['message']['content'].split(".")[0]}")
        return resposta['message']['content'].split(".")[0]  # Pega apenas a primeira frase
    
    except Exception as e:
        print(f"⚠️ Erro: {e}")
        return "8 anos em TI"  # Fallback genérico

def testar_api():
    pergunta = "Seu inglês é fluente?"
    print("\033[94mpergunta: ->", pergunta)
    print("\033[91mResposta:", obter_resposta(pergunta))
    input("")