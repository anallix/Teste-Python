# LLM CLI — Factory, Command, Strategy, Observer

Aplicação em Python (CLI) que consulta dois LLMs (OpenAI e Hugging Face) e escolhe a melhor resposta usando estratégias de avaliação.  
Projeto focado em **padrões de projeto**: **Factory**, **Command**, **Strategy** e **Observer**.

⚠️ **Observações Importantes**
- A integração com OpenAI está implementada. Se não tiver créditos, use o provider `openai-fake` (simulado).  
- A API pública da Hugging Face pode retornar timeout/503/404; a aplicação trata esses erros sem quebrar.


## Requisitos

- Python **3.10+**
- (Opcional para chamadas reais) chaves de API:
  - OpenAI: `OPENAI_API_KEY`
  - Hugging Face: `HUGGINGFACE_API_KEY`

## Instalação

```bash
git clone https://github.com/anallix/Teste-Python.git
cd Teste-Python

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt

# Demonstração garantida (sem depender de HF): resposta mais curta vence
python run_cli.py ask "Explique em 1 frase: por que o céu é azul?" --providers openai,openai-fake --strategy shortest

# Usando Hugging Face + verificação por palavras-chave
python run_cli.py ask "Explique em 1 frase: por que o céu é azul?" --providers openai-fake,hf --keywords luz,atmosfera,dispersa

# Resposta mais criativa 
python run_cli.py ask "Responda de forma criativa: o que é gravidade?" --providers openai-fake,hf --temperature 0.8
