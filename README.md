# LinkedIn Auto-Apply Bot

> Documentação técnica e guia de instalação para o robô que automatiza o envio de candidaturas simplificadas no LinkedIn.

---

## Índice

1. Visão geral
2. Requisitos
3. Instalação do Python
4. Instalação do Ollama
5. Instalação do modelo DeepSeek Coder (via Ollama)
6. Configuração do arquivo `obterRespostas.py`
7. Dependências e execução do robô
8. Como o robô funciona (fluxo)
9. Boas práticas, segurança e responsabilidades
10. Testes e solução de problemas
11. Contato e licença

---

## 1. Visão geral

Este projeto automatiza o preenchimento de candidaturas simplificadas no LinkedIn. O objetivo é reduzir o trabalho manual ao responder formulários padrão com informações pessoais e profissionais previamente definidas.

O repositório contém o script central `obterRespostas.py` (responsável por centralizar as respostas) e um robô que abre o navegador, espera o login do usuário, percorre as vagas filtradas e preenche os formulários automaticamente.

---

## 2. Requisitos

* Sistema operacional: Windows, macOS ou Linux (instruções genéricas no documento).
* Python 3.10+ (recomendado).
* Ollama (servidor local para executar modelos LLM como DeepSeek Coder).
* Modelo DeepSeek Coder instalado via Ollama (variante adequada ao seu hardware).
* Navegador compatível (Chrome/Edge/Firefox). Se o robô usa Selenium, um WebDriver compatível deve estar disponível.

---

## 3. Instalação do Python

1. Baixe o instalador oficial em [https://python.org](https://python.org) e execute-o.
2. **Importante:** marque a opção "Add Python to PATH" durante a instalação (no Windows).
3. Verifique a instalação no terminal/cmd:

```bash
python --version
pip --version
```

---

## 4. Instalação do Ollama

Ollama é o runtime local que permite executar modelos LLM na sua máquina. Instale-o seguindo as instruções oficiais do site do Ollama.

Passos resumidos (exemplo UNIX/WSL/macOS):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

No Windows, faça o download do instalador disponível na página de downloads do Ollama e execute-o.

Após a instalação, inicie o serviço (ou deixe o app rodando):

```bash
# inicia o serviço em background (exemplo)
ollama serve &

# lista modelos instalados
ollama list
```

Obs.: Ollama armazena os modelos localmente; verifique espaço em disco e requisitos de memória/RAM/GPU para os modelos maiores.

---

## 5. Instalação do modelo DeepSeek Coder (via Ollama)

Após instalar o Ollama, faça o download (pull) do modelo DeepSeek Coder desejado. Exemplos:

```bash
# modelo padrão (varia conforme disponibilidade)
ollama run deepseek-coder

# ou variantes por tamanho
ollama run deepseek-coder:6.7b
ollama run deepseek-coder:33b

# deepseek-coder-v2 (ex.: para variantes mais recentes)
ollama run deepseek-coder-v2
```

O comando fará o download do modelo para o diretório configurado pelo Ollama. Modelos maiores exigem mais RAM/VRAM e mais espaço em disco.

---

## 6. Configuração do arquivo `obterRespostas.py`

O arquivo `obterRespostas.py` centraliza as respostas que o robô usa para preencher os formulários.

### Onde colocar suas informações

1. Abra o arquivo `obterRespostas.py` no seu editor de texto/IDE preferido.
2. Atualize o dicionário `respostas_fallback` com suas informações pessoais e profissionais. Cada chave corresponde a um fragmento de pergunta que o robô procura (ex.: "Email", "Phone Number", "Experience").

Exemplo (trecho):

```python
respostas_fallback = {
    "First Name": "Rafael",
    "Last Name": "Marega",
    "Email": "rafaelmarega1@gmail.com",
    "Phone Number": "11980569410",
    "Experience": "8",
    "City": "São Paulo, Brasil",
    "LinkedIn": "www.linkedin.com/in/rafael-marega",
    # ...adicione/ajuste conforme necessário
}
```

3. Revise também a string `system_prompt`. Ela contém informações do candidato (endereço, experiência, LinkedIn etc.) que são enviadas ao modelo DeepSeek caso nenhuma resposta de fallback seja encontrada. Atualize as linhas apropriadas para refletir seus dados.

Exemplo (trecho do `system_prompt`):

```python
system_prompt = """You are a job candidate with 8 years of experience in IT.

Candidate Information:
    Street: [Nome da rua],
    City: São Paulo, Brasil,
    State: SP,
    ZIP Postal Code: [CEP],
    Country: Brasil
    LinkedIn Profile: www.linkedin.com/in/[seu linkedin]
    Experience: 8
"""
```

4. Salve o arquivo em codificação UTF-8.

### Observações sobre comportamento

* O robô primeiro tenta resolver a pergunta procurando por correspondência direta nas chaves do dicionário `respostas_fallback`.
* Se não encontrar correspondência direta, tenta buscar por similaridade (usando `difflib.get_close_matches`).
* Se ainda assim não encontrar, consulta o Ollama (modelo DeepSeek Coder) com o `system_prompt` restritivo.
* Há mensagens de `print()` para logar de qual fonte a resposta veio (fallback direto, correspondência por similaridade ou DeepSeek).
* Em caso de erro, o método retorna um fallback genérico.

---

## 7. Dependências e execução do robô

### Arquivo de dependências (recomendado)

```
ollama
selenium
requests
beautifulsoup4
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

> Ajuste a lista de pacotes conforme o que seu robô realmente utiliza.

### Executando testes locais

Para testar apenas a parte de respostas (sem abrir o robô completo):

```bash
python obterRespostas.py
```

Isso executará a função `testar_api()` presente no arquivo e imprimirá uma pergunta de teste e a resposta retornada.

### Execução do robô (fluxo básico)

1. Abra o terminal e ative o ambiente virtual (se estiver usando `.venv`).
2. Garanta que o Ollama está rodando e que o modelo DeepSeek Coder foi baixado.
3. Inicie o script principal do robô (por exemplo `python main.py` — substitua pelo nome do seu script principal).
4. O robô abrirá o navegador automaticamente.
5. Faça login manualmente no LinkedIn e navegue até a seção de candidaturas simplificadas (filtre as vagas como desejar).
6. Volte ao terminal e pressione `Enter` para que o robô prossiga.
7. O robô acessará cada vaga encontrada e preencherá os campos usando as respostas definidas em `obterRespostas.py`.

---

## 8. Como o robô funciona (fluxo detalhado)

1. **Inicialização:** carrega `respostas_fallback` e `system_prompt` do `obterRespostas.py`.
2. **Abertura do navegador:** o script inicializa uma instância de navegador (Selenium ou alternativa).
3. **Aguardar login:** o robô pausa e espera que o usuário faça login e filtre as vagas.
4. **Sinal do usuário:** o usuário pressiona `Enter` no terminal para que o robô comece a iterar pelas vagas.
5. **Iteração e preenchimento:** para cada vaga o robô: abre o link, identifica os campos do formulário, recupera a pergunta/descritivo do campo e chama `obter_resposta(pergunta)` para obter a resposta.

   * Primeiro verifica `respostas_fallback` por correspondência direta.
   * Se não encontrar, usa similaridade por `difflib`.
   * Se ainda não houver correspondência, consulta o modelo DeepSeek via Ollama usando `system_prompt`.
6. **Submissão:** quando todos os campos estiverem preenchidos, o robô submete a candidatura (quando aplicável).
7. **Logs:** o robô imprime logs simples para indicar sucesso/erro por vaga.

---

## 9. Boas práticas, segurança e responsabilidades

* **Leia os termos de uso do LinkedIn**: automação pode violar termos e resultar em restrições na conta.
* **Limites e cadência:** implemente delays e limites para evitar tráfego que pareça automatizado (esperas aleatórias entre ações).
* **Dados sensíveis:** mantenha suas credenciais e dados pessoais seguros; não comite senhas no repositório.
* **Ambiente de testes:** experimente primeiro em contas de teste antes de usar em contas reais.

---

## 10. Testes e solução de problemas

* **Verifique o Ollama:** `ollama list` e `ollama run <modelo>`.
* **Verifique o Python e dependências:** `python --version`, `pip list`.
* **Logs no terminal:** revise as mensagens `print()` do `obterRespostas.py` para entender se as respostas vêm do fallback ou do modelo.
* **Erros comuns:** problemas de permissão, modelo não baixado, WebDriver incompatível.

---

## 11. Contato e licença

* Autor: Rafael Marega
* E-mail: [rafaelmarega1@gmail.com](mailto:rafaelmarega1@gmail.com)
