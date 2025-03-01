import subprocess
import threading
import time
import os
import re
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.box import ROUNDED
from rich.markdown import Markdown
from rich.theme import Theme

# Tema personalizado
custom_theme = Theme({
    "info": "cyan",
    "success": "green",
    "error": "bold red",
    "warning": "yellow",
    "highlight": "magenta",
    "prompt": "bold yellow",
    "model": "blue",
    "user": "green",
    "header": "bold cyan underline",
    "ai_response": "white",
    "chat_history": "dim white"
})

console = Console(theme=custom_theme, width=100)

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    """Exibe um cabeçalho estilizado"""
    clear_screen()
    table = Table(show_header=False, box=ROUNDED, border_style="blue", width=100)
    table.add_column()
    table.add_row("🤖 DeepSeek-R1 14B Chat Interface 🤖")
    console.print(table)
    console.print("=" * 100, style="blue")
    console.print()

def strip_ansi_codes(text):
    """Remove códigos ANSI de uma string"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def chat_with_deepseek_r1(prompt, show_thinking=True):
    """
    Função para interagir com o modelo deepseek-r1:14b via Ollama
    com visualização aprimorada usando Rich
    
    Args:
        prompt (str): Mensagem a ser enviada para o modelo
        show_thinking (bool): Se deve mostrar animação de "pensando"
        
    Returns:
        str: Resposta do modelo
    """
    # Preparar o prompt para forçar respostas em português
    prefixo_portugues = """Você é um assistente de IA útil e deve responder sempre em português brasileiro, 
independentemente do idioma usado na pergunta. Use uma linguagem natural e fluente.

Pergunta do usuário: """
    
    prompt_completo = prefixo_portugues + prompt
    
    # Comando específico
    cmd = ["ollama", "run", "deepseek-r1:14b"]
    
    # Log estilizado
    console.print(Panel(
        "[model]Iniciando comunicação com DeepSeek-R1 (14B)[/model]",
        title="[header]STATUS[/header]",
        border_style="blue",
        box=ROUNDED
    ))
    
    # Criar uma tabela para o envio de prompt (mostrando apenas a pergunta original, não o prefixo)
    prompt_table = Table(box=ROUNDED, border_style="green", width=100)
    prompt_table.add_column("Prompt enviado:", style="bold green")
    prompt_table.add_row(prompt)
    console.print(prompt_table)
    
    # Preparar o processo
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Variável para armazenar a resposta e controlar a thread
    result = {"stdout": "", "stderr": "", "complete": False}
    progress_event = threading.Event()
    
    # Thread para mostrar indicação de progresso
    def show_progress_indicator():
        if not show_thinking:
            return
            
        # Usa um método mais simples que não conflita
        thinking_phrases = [
            "Processando informações",
            "Analisando contexto",
            "Gerando resposta",
            "Aplicando conhecimentos",
            "Elaborando conteúdo"
        ]
        spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        
        start_time = time.time()
        progress_line = ""
        
        try:
            while not result["complete"] and not progress_event.is_set():
                elapsed = time.time() - start_time
                minutes, seconds = divmod(int(elapsed), 60)
                
                # Seleciona uma frase baseada no tempo decorrido
                phrase_index = int(elapsed / 5) % len(thinking_phrases)
                phrase = thinking_phrases[phrase_index]
                
                # Atualiza o spinner
                spinner_char = spinner_chars[int(elapsed * 10) % len(spinner_chars)]
                
                # Limpa a linha anterior e exibe novo status
                if progress_line:
                    # Calcula o número de caracteres para limpar (largura + alguns extras)
                    clear_len = len(progress_line) + 5
                    print("\r" + " " * clear_len, end="\r")
                
                # Novo texto de progresso
                progress_line = f"{spinner_char} {phrase}... ({minutes:02d}:{seconds:02d})"
                print("\r" + progress_line, end="", flush=True)
                
                # Pausa curta
                time.sleep(0.1)
        finally:
            # Garante que limpamos a linha no final
            if progress_line:
                print("\r" + " " * (len(progress_line) + 5), end="\r", flush=True)
    
    # Iniciar thread de progresso
    progress_thread = threading.Thread(target=show_progress_indicator)
    progress_thread.daemon = True
    progress_thread.start()
    
    try:
        # Enviar o prompt completo (com o prefixo de português) e receber a resposta
        stdout, stderr = process.communicate(input=prompt_completo)
        result["stdout"] = stdout
        
        # Limpar códigos ANSI do stderr antes de armazenar
        if stderr:
            result["stderr"] = strip_ansi_codes(stderr)
        
    except Exception as e:
        result["stderr"] = str(e)
    finally:
        # Marcar como completo para parar a animação
        result["complete"] = True
        progress_event.set()
        
        # Garantir que a thread termine
        if progress_thread.is_alive():
            progress_thread.join(timeout=1.0)
        
        # Limpar qualquer resíduo da linha de progresso
        print("\r" + " " * 100, end="\r", flush=True)
    
    # Verificar erros (apenas exibir se houver conteúdo útil)
    if result["stderr"] and len(result["stderr"].strip()) > 0:
        # Remover caracteres de controle mais uma vez para garantir
        cleaned_error = strip_ansi_codes(result["stderr"]).strip()
        
        # Verificar se ainda há conteúdo útil
        if cleaned_error and not cleaned_error.isspace() and not "spinner" in cleaned_error.lower():
            console.print(Panel(
                f"[error]{cleaned_error}[/error]",
                title="[header]ERRO[/header]",
                border_style="red",
                box=ROUNDED
            ))
    else:
        # Log de conclusão
        console.print("[success]✓ Resposta recebida![/success]")
    
    return result["stdout"].strip()

def format_response(text):
    """Formata a resposta para exibição mais bonita"""
    # Remover possíveis tags <think></think> que o modelo às vezes adiciona
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    
    # Detectar se a resposta contém markdown
    if '```' in text or '#' in text or '*' in text:
        return Markdown(text)
    else:
        return text

def get_user_input():
    """Obtém entrada do usuário com estilo"""
    return Prompt.ask("[prompt]Sua pergunta[/prompt]")

def continuous_chat():
    """Inicia um chat contínuo com o DeepSeek-R1"""
    show_header()
    
    console.print(Panel(
        "[info]Modo de Chat Contínuo[/info]\n"
        "Digite suas perguntas e converse continuamente com o modelo.\n"
        "Para sair a qualquer momento, digite [bold]'sair'[/bold] ou [bold]'exit'[/bold].",
        title="[header]INSTRUÇÕES[/header]",
        border_style="cyan",
        box=ROUNDED
    ))
    
    # Histórico de chat
    chat_history = []
    
    while True:
        # Obter a pergunta do usuário
        console.print()
        pergunta = get_user_input()
        
        # Verificar se o usuário quer sair
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            console.print("[warning]Saindo do chat contínuo...[/warning]")
            break
        
        console.print()
        
        # Adicionar ao histórico
        chat_history.append(("user", pergunta))
        
        # Obter resposta
        resposta = chat_with_deepseek_r1(pergunta)
        
        # Adicionar ao histórico
        chat_history.append(("ai", resposta))
        
        # Exibir a resposta em um painel estilizado
        console.print(Panel(
            format_response(resposta),
            title="[header]Resposta do DeepSeek-R1[/header]",
            border_style="cyan",
            box=ROUNDED,
            expand=False,
            width=100
        ))
        
        # Mostrar opções
        console.print("\n[info]Digite sua próxima pergunta ou 'sair' para voltar ao menu principal[/info]")
        
    # Retornar ao menu principal
    return

def chat_with_context():
    """Chat com contexto personalizado"""
    show_header()
    
    nome_usuario = Prompt.ask("[prompt]Seu nome[/prompt]")
    idade = Prompt.ask("[prompt]Sua idade[/prompt]")
    pergunta = get_user_input()
    
    prompt_personalizado = f"""
    Informações do usuário:
    - Nome: {nome_usuario}
    - Idade: {idade}

    Pergunta: {pergunta}
    """
    
    console.print()
    resposta = chat_with_deepseek_r1(prompt_personalizado)
    
    # Exibindo a resposta em um painel estilizado
    console.print(Panel(
        format_response(resposta),
        title="[header]Resposta Personalizada[/header]",
        border_style="cyan",
        box=ROUNDED,
        expand=False,
        width=100
    ))

def predefined_questions():
    """Chat com perguntas pré-definidas"""
    show_header()
    
    table = Table(box=ROUNDED, border_style="green", width=100)
    table.add_column("ID", style="bold cyan", width=5)
    table.add_column("Perguntas pré-definidas", style="green")
    
    perguntas = [
        "Explique o que é inteligência artificial em termos simples.",
        "Quais são os melhores frameworks de machine learning em 2025?",
        "Como a IA está transformando a área da saúde?",
        "Quais são as considerações éticas no desenvolvimento de IA?",
        "Qual é a diferença entre machine learning e deep learning?"
    ]
    
    for i, pergunta in enumerate(perguntas, 1):
        table.add_row(str(i), pergunta)
        
    console.print(table)
    
    choice = Prompt.ask(
        "[prompt]Selecione uma pergunta[/prompt]", 
        choices=[str(i) for i in range(1, len(perguntas)+1)]
    )
    
    pergunta_selecionada = perguntas[int(choice)-1]
    console.print(f"[user]Pergunta selecionada:[/user] {pergunta_selecionada}")
    console.print()
    
    resposta = chat_with_deepseek_r1(pergunta_selecionada)
    
    # Exibindo a resposta em um painel estilizado
    console.print(Panel(
        format_response(resposta),
        title="[header]Resposta do DeepSeek-R1[/header]",
        border_style="cyan",
        box=ROUNDED,
        expand=False,
        width=100
    ))

def main():
    """Função principal com menu"""
    show_header()
    
    # Menu inicial
    table = Table(box=ROUNDED, border_style="yellow", width=100)
    table.add_column("Opções de Chat", style="bold yellow")
    table.add_row("1. Chat contínuo")
    table.add_row("2. Chat com contexto personalizado")
    table.add_row("3. Perguntas pré-definidas")
    table.add_row("4. Sair")
    
    console.print(table)
    
    choice = Prompt.ask("[prompt]Selecione uma opção[/prompt]", choices=["1", "2", "3", "4"])
    
    if choice == "1":
        # Chat contínuo
        continuous_chat()
    elif choice == "2":
        # Chat com contexto personalizado
        chat_with_context()
    elif choice == "3":
        # Perguntas pré-definidas
        predefined_questions()
    else:
        # Sair
        console.print("[warning]Saindo do programa![/warning]")
        return
    
    # Verificar se deseja voltar ao menu principal
    if choice != "1":  # Para o chat contínuo, já voltamos ao menu automaticamente
        continuar = Prompt.ask(
            "\n[prompt]Voltar ao menu principal?[/prompt]", 
            choices=["s", "n"], 
            default="s"
        )
        
        if continuar.lower() == "s":
            main()  # Reiniciar o menu

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[warning]Programa interrompido pelo usuário![/warning]")
    except Exception as e:
        console.print(f"[error]Erro inesperado: {str(e)}[/error]")
    finally:
        console.print("\n[info]Obrigado por usar a interface DeepSeek-R1![/info]")