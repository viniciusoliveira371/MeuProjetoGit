import json
import os
import sys

ARQUIVO_TAREFAS = "tarefas.json"

def carregar_tarefas():
    """Lê as tarefas do arquivo JSON com tratamento de erros."""
    if not os.path.exists(ARQUIVO_TAREFAS):
        return []

    try:
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        print("Aviso: Arquivo de tarefas contém dados inválidos.")
        return []

    except OSError as erro:
        print(f"Erro ao acessar o arquivo: {erro}")
        return []

def salvar_tarefas(tarefas):
    """Grava a lista de tarefas no arquivo JSON."""
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

def adicionar_tarefa(descricao):
    """Adiciona uma nova tarefa com id incremental e salva."""
    descricao = descricao.strip()
    if not descricao:
        print("Erro: A descrição da tarefa não pode ser vazia.")
        return

    tarefas = carregar_tarefas()
    novo_id = max([t["id"] for t in tarefas], default=0) + 1
    
    nova_tarefa = {
        "id": novo_id,
        "descricao": descricao,
        "concluida": False
    }
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    print(f"Tarefa #{novo_id} adicionada com sucesso: \"{descricao}\"")

def listar_tarefas():
    """Exibe as tarefas e um resumo estatístico."""
    tarefas = carregar_tarefas()

    if not tarefas:
        print("\nNenhuma tarefa encontrada.")
        print("Use 'python Nexus.py add \"Descrição\"' para cadastrar uma!\n")
        return

    concluidas = sum(1 for t in tarefas if t["concluida"])
    pendentes = len(tarefas) - concluidas

    print("\n================== SUAS TAREFAS ==================")

    for t in tarefas:
        marcador = "[✔️]" if t["concluida"] else "[ ]"
        print(f"{marcador} #{t['id']:02d} - {t['descricao']}")

    print("--------------------------------------------------")
    print(f"Total: {len(tarefas)} | Concluídas: {concluidas} | Pendentes: {pendentes}")
    print("==================================================\n")

def concluir_tarefa(tarefa_id):
    """Marca uma tarefa como concluída pelo seu id."""
    tarefas = carregar_tarefas()
    encontrada = False

    for t in tarefas:
        if t["id"] == tarefa_id:
            if t["concluida"]:
                print(f"Aviso: A tarefa #{tarefa_id} já estava concluída.")
            else:
                t["concluida"] = True
                salvar_tarefas(tarefas)
                print(f"Tarefa #{tarefa_id} concluída com sucesso! [✔]")
            encontrada = True
            break

    if not encontrada:
        print(f"Erro: Tarefa #{tarefa_id} não foi encontrada.")

def remover_tarefa(tarefa_id):
    """Remove uma tarefa pelo seu id."""
    tarefas = carregar_tarefas()
    tarefas_filtradas = [t for t in tarefas if t["id"] != tarefa_id]

    if len(tarefas_filtradas) == len(tarefas):
        print(f"Erro: Tarefa #{tarefa_id} não foi encontrada.")
    else:
        salvar_tarefas(tarefas_filtradas)
        print(f"Tarefa #{tarefa_id} removida com sucesso!")

def exibir_ajuda():
    """Exibe o guia de comandos do Nexus CLI."""
    print("\n=== Nexus CLI - Gerenciador de Tarefas ===")
    print("Uso: python nexus.py <comando> [argumentos]\n")
    print("Comandos disponíveis:")
    print("  add \"<descricao>\" : Adiciona uma nova tarefa")
    print("  list              : Exibe todas as tarefas e o resumo")
    print("  done <id>         : Marca uma tarefa como concluída")
    print("  remove <id>       : Remove uma tarefa")
    print("  help, -h, --help  : Mostra esta mensagem de ajuda\n")
    print("Exemplos:")
    print("  python nexus.py add \"Comprar café\"")
    print("  python nexus.py done 1")
    print("  python nexus.py remove 2\n")

def main():
    if len(sys.argv) < 2:
        exibir_ajuda()
        return

    comando = sys.argv[1].lower()

    if comando in ("help", "-h", "--help"):
        exibir_ajuda()

    elif comando == "add":
        if len(sys.argv) < 3:
            print("Erro: Informe a descrição da tarefa.")
            print('Exemplo: python Nexus.py add "Comprar café"')
            return

        descricao = " ".join(sys.argv[2:])
        adicionar_tarefa(descricao)

    elif comando == "list":
        listar_tarefas()

    elif comando == "done":
        if len(sys.argv) < 3:
            print("Erro: Informe o ID da tarefa.")
            return

        try:
            tarefa_id = int(sys.argv[2])
            concluir_tarefa(tarefa_id)
        except ValueError:
            print("Erro: O ID deve ser um número inteiro.")

    elif comando == "remove":
        if len(sys.argv) < 3:
            print("Erro: Informe o ID da tarefa.")
            return

        try:
            tarefa_id = int(sys.argv[2])
            remover_tarefa(tarefa_id)
        except ValueError:
            print("Erro: O ID deve ser um número inteiro.")

    else:
        print(f"Comando desconhecido: '{comando}'.")
        print("Digite 'python Nexus.py help' para consultar a ajuda.")

if __name__ == "__main__":
    main()
