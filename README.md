
---

# 🚀 AI Chat Interface  

Uma interface de chat interativa e altamente customizável para **qualquer modelo do Ollama**, com uma experiência visual aprimorada utilizando a biblioteca **Rich**.  

---

## ✨ Principais Funcionalidades  
✅ **Compatível com qualquer modelo do Ollama** – Escolha e personalize o modelo que deseja utilizar.  
✅ **Chat Contínuo** – Converse de forma interativa e ininterrupta.  
✅ **Chat com Contexto Personalizado** – Adapte as respostas de acordo com seu perfil.  
✅ **Perguntas Pré-definidas** – Acesse rapidamente respostas sobre IA e tecnologia.  
✅ **Interface Estilizada** – Um layout visual moderno e agradável, impulsionado pelo Rich.  

---

## 🛠️ Requisitos  
Antes de iniciar, certifique-se de ter instalado:  

🔹 **Python 3.8+**  
🔹 **[Ollama](https://ollama.ai/)** (para rodar o modelo de IA)  
🔹 **Dependências Python**:  
```bash
pip install rich
```  

---

## ⚙️ Configuração do Modelo  
Este projeto é compatível com **qualquer modelo do Ollama**! Para alterar o modelo padrão, edite a variável `AGENT` no código:  

```python
AGENT = cmd = ["ollama", "run", "seu-modelo-aqui"]
```  

🔹 Substitua `"seu-modelo-aqui"` pelo modelo desejado, como `mistral`, `gemma`, `llama3`, etc.  

---

## 🚀 Como Executar  
1️⃣ Clone o repositório ou baixe os arquivos:  
   ```bash
   git clone https://github.com/NicollasRezende/IA-CHAT.git
   cd IA-CHAT
   ```  
2️⃣ Instale as dependências necessárias.  
3️⃣ Execute o script principal:  
   ```bash
   python main.py
   ```  

---

## 🎮 Como Usar  
Ao iniciar o programa, você verá um menu interativo com as seguintes opções:  

```
🤖 AI Chat Interface 🤖
=============================================
Selecione uma opção:
1️⃣ Chat contínuo
2️⃣ Chat com contexto personalizado
3️⃣ Perguntas pré-definidas
4️⃣ Sair
```  

📌 Escolha uma opção e aproveite a interação com a IA!  

---

## 📌 Exemplo de Uso  
```bash
> python main.py
🤖 AI Chat Interface 🤖
=============================================
Selecione uma opção:
1. Chat contínuo
2. Chat com contexto personalizado
3. Perguntas pré-definidas
4. Sair
Sua escolha: 1
```  

---
