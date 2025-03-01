# AI Chat Interface

## Sobre o Projeto
Este projeto fornece uma interface de chat interativa para comunicação com o modelo **DeepSeek-R1 14B** via **Ollama**. A interface é estilizada utilizando a biblioteca **Rich**, oferecendo uma experiência visual aprimorada.

## Funcionalidades
- **Chat Contínuo**: Permite conversas interativas e ininterruptas.
- **Chat com Contexto Personalizado**: Personaliza a interação de acordo com o usuário.
- **Perguntas Pré-definidas**: Fornece perguntas comuns sobre IA e tecnologia.
- **Interface Estilizada**: Utiliza a biblioteca Rich para um layout visual agradável.

## Requisitos
Antes de executar o projeto, certifique-se de ter os seguintes requisitos instalados:

- Python 3.8+
- [Ollama](https://ollama.ai/) (para rodar o modelo DeepSeek-R1 14B)
- ollama run deepseek-r1:14b baixe esse modelo ou modifique para um de sua preferencia
- Dependências Python:
  ```bash
  pip install rich
  ```

## Como Executar
1. Clone o repositório ou baixe os arquivos.
2. Instale as dependências necessárias.
3. Execute o script principal:
   ```bash
   python main.py
   ```

## Uso
Ao iniciar o programa, você verá um menu com as seguintes opções:
1. **Chat Contínuo**: Digite suas perguntas para conversar com o modelo continuamente.
2. **Chat com Contexto Personalizado**: Insira algumas informações pessoais para uma resposta mais personalizada.
3. **Perguntas Pré-definidas**: Escolha uma pergunta sobre IA para obter uma resposta automatizada.
4. **Sair**: Encerra o programa.

## Exemplo de Uso
```bash
> python main.py
🤖 DeepSeek-R1 14B Chat Interface 🤖
=============================================
Selecione uma opção:
1. Chat contínuo
2. Chat com contexto personalizado
3. Perguntas pré-definidas
4. Sair
Sua escolha: 1
```



