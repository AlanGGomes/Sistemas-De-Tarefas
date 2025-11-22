"""
Sistema de Gerenciamento de Tarefas
Descrição: Implementa um gerenciador de tarefas conforme especificações da atividade.
"""

import json
import os
from datetime import datetime, timedelta
import sys

# -------------------------
# Declaração de variáveis globais
# -------------------------
ARQUIVO_TAREFAS = 'tarefas.json'
ARQUIVO_ARQUIVADAS = 'tarefas_arquivadas.json'
TAREFAS = []  
NEXT_ID = 1   

PRIORIDADES = ['Urgente', 'Alta', 'Média', 'Baixa']
ORIGENS = ['E-mail', 'Telefone', 'Chamado do Sistema']
STATUS_VALIDOS = ['Pendente', 'Fazendo', 'Concluída', 'Arquivado', 'Excluída']

# -------------------------
# Funções de persistência
# -------------------------

def verificar_e_criar_arquivos():
    """
    Verifica se os arquivos obrigatórios existem e, se não, cria-os com conteúdo inicial.
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print("Executando a função verificar_e_criar_arquivos")
    inicial = []
    if not os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, 'w', encoding='utf-8') as f:
            json.dump(inicial, f, ensure_ascii=False, indent=2)
    if not os.path.exists(ARQUIVO_ARQUIVADAS):
        with open(ARQUIVO_ARQUIVADAS, 'w', encoding='utf-8') as f:
            json.dump(inicial, f, ensure_ascii=False, indent=2)


def carregar_dados():
    """
    Carrega os dados dos arquivos JSON para as variáveis globais.
    Ajusta o NEXT_ID com base nos IDs já presentes.
    Parâmetros: nenhum
    Retorno: nenhum
    """
    global TAREFAS, NEXT_ID
    print("Executando a função carregar_dados")
    try:
        with open(ARQUIVO_TAREFAS, 'r', encoding='utf-8') as f:
            TAREFAS = json.load(f)
    except Exception:
        TAREFAS = []
    # Ajusta NEXT_ID
    max_id = 0
    for t in TAREFAS:
        try:
            if int(t.get('id', 0)) > max_id:
                max_id = int(t.get('id', 0))
        except Exception:
            continue
    NEXT_ID = max_id + 1


def salvar_dados():
    """
    Salva a lista atual de tarefas no arquivo tarefas.json.
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print("Executando a função salvar_dados")
    try:
        with open(ARQUIVO_TAREFAS, 'w', encoding='utf-8') as f:
            json.dump(TAREFAS, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar tarefas: {e}")


# -------------------------
# Funções utilitárias e de validação
# -------------------------

def validar_prioridade(prio):
    """
    Valida se a prioridade informada é válida.
    Retorna a prioridade formatada (com capitalização correta) ou None.
    """
    print("Executando a função validar_prioridade")
    if not isinstance(prio, str):
        return None
    pr = prio.strip().capitalize()
    # Tratar 'Urgente' que pode ser escrito com U maiúsculo
    for p in PRIORIDADES:
        if p.lower() == pr.lower():
            return p
    return None


def validar_origem(orig):
    """
    Valida se a origem informada é válida.
    Retorna origem formatada ou None.
    """
    print("Executando a função validar_origem")
    if not isinstance(orig, str):
        return None
    o = orig.strip()
    for cand in ORIGENS:
        if cand.lower() == o.lower():
            return cand
    return None


def encontrar_tarefa_por_id(task_id):
    """
    Localiza e retorna a tarefa com id informado ou None se não existir.
    Parâmetros:
        task_id (int)
    Retorno:
        dict|None
    """
    print("Executando a função encontrar_tarefa_por_id")
    for t in TAREFAS:
        try:
            if int(t.get('id')) == int(task_id):
                return t
        except Exception:
            continue
    return None


# -------------------------
# Operações principais
# -------------------------

def criar_tarefa():
    """
    Cria uma nova tarefa solicitando informações ao usuário,
    valida os dados e adiciona a tarefa à lista global de tarefas.
    Parâmetros: nenhum
    Retorno: nenhum
    """
    global TAREFAS, NEXT_ID
    print("Executando a função criar_tarefa")
    titulo = input('Título (obrigatório): ').strip()
    while not titulo:
        print('Título é obrigatório.')
        titulo = input('Título (obrigatório): ').strip()

    descricao = input('Descrição (opcional): ').strip()

    print('Prioridades disponíveis: ' + ', '.join(PRIORIDADES))
    prioridade = input('Prioridade (Urgente/Alta/Média/Baixa) (obrigatório): ')
    prioridade_valida = validar_prioridade(prioridade)
    while prioridade_valida is None:
        print('Prioridade inválida. Opções: ' + ', '.join(PRIORIDADES))
        prioridade = input('Prioridade: ')
        prioridade_valida = validar_prioridade(prioridade)

    print('Origens disponíveis: ' + ', '.join(ORIGENS))
    origem = input('Origem da tarefa (E-mail/Telefone/Chamado do Sistema) (obrigatório): ')
    origem_valida = validar_origem(origem)
    while origem_valida is None:
        print('Origem inválida. Opções: ' + ', '.join(ORIGENS))
        origem = input('Origem da tarefa: ')
        origem_valida = validar_origem(origem)

    data_criacao = datetime.now().isoformat()

    tarefa = {
        'id': NEXT_ID,
        'titulo': titulo,
        'descricao': descricao,
        'prioridade': prioridade_valida,
        'status': 'Pendente',
        'origem': origem_valida,
        'data_criacao': data_criacao,
        'data_conclusao': None
    }
    TAREFAS.append(tarefa)
    NEXT_ID += 1
    print(f"Tarefa criada com ID {tarefa['id']}")


def verificar_urgencia():
    """
    Seleciona a próxima tarefa a ser executada verificando prioridades.
    Atualiza o status da tarefa selecionada para 'Fazendo'.
    Retorna a tarefa selecionada ou None.
    """
    global TAREFAS
    print("Executando a função verificar_urgencia")
    # buscar pela prioridade máxima (Urgente), senão próxima prioridade
    for prioridade in PRIORIDADES:
        for t in TAREFAS:
            if t.get('status') == 'Pendente' and t.get('prioridade') == prioridade:
                t['status'] = 'Fazendo'
                print(f"Tarefa selecionada: ID {t['id']} - {t['titulo']}")
                return t
    print('Não há tarefas pendentes.')
    return None


def atualizar_prioridade():
    """
    Altera a prioridade de uma tarefa.
    Solicita o ID da tarefa e a nova prioridade, validando os dados.
    """
    global TAREFAS
    print("Executando a função atualizar_prioridade")
    try:
        task_id = int(input('Informe o ID da tarefa a ser atualizada: '))
    except Exception:
        print('ID inválido.')
        return
    tarefa = encontrar_tarefa_por_id(task_id)
    if not tarefa:
        print('Tarefa não encontrada.')
        return
    print('Prioridades disponíveis: ' + ', '.join(PRIORIDADES))
    nova = input('Nova prioridade: ')
    nova_valida = validar_prioridade(nova)
    if nova_valida is None:
        print('Prioridade inválida. Operação cancelada.')
        return
    tarefa['prioridade'] = nova_valida
    print(f"Prioridade da tarefa {task_id} atualizada para {nova_valida}.")


def concluir_tarefa():
    """
    Marca uma tarefa como concluída e registra a data de conclusão.
    """
    global TAREFAS
    print("Executando a função concluir_tarefa")
    try:
        task_id = int(input('Informe o ID da tarefa a concluir: '))
    except Exception:
        print('ID inválido.')
        return
    tarefa = encontrar_tarefa_por_id(task_id)
    if not tarefa:
        print('Tarefa não encontrada.')
        return
    if tarefa.get('status') == 'Concluída':
        print('Tarefa já está concluída.')
        return
    tarefa['status'] = 'Concluída'
    tarefa['data_conclusao'] = datetime.now().isoformat()
    print(f"Tarefa {task_id} marcada como Concluída.")


def arquivar_tarefas_antigas():
    """
    Atualiza o status para 'Arquivado' das tarefas concluídas há mais de uma semana.
    Também registra/atualiza o arquivo de tarefas arquivadas acumulando histórico.
    """
    global TAREFAS
    print("Executando a função arquivar_tarefas_antigas")
    agora = datetime.now()
    arquivadas_para_salvar = []
    for t in TAREFAS:
        if t.get('status') == 'Concluída' and t.get('data_conclusao'):
            try:
                dt = datetime.fromisoformat(t['data_conclusao'])
            except Exception:
                continue
            if agora - dt > timedelta(days=7):
                t['status'] = 'Arquivado'
                arquivadas_para_salvar.append(t.copy())
    # Salvar histórico acumulado
    if arquivadas_para_salvar:
        try:
            with open(ARQUIVO_ARQUIVADAS, 'r', encoding='utf-8') as f:
                hist = json.load(f)
        except Exception:
            hist = []
        
        ids_existentes = {item.get('id') for item in hist}
        for item in arquivadas_para_salvar:
            if item.get('id') not in ids_existentes:
                hist.append(item)
        try:
            with open(ARQUIVO_ARQUIVADAS, 'w', encoding='utf-8') as f:
                json.dump(hist, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao atualizar arquivo de arquivadas: {e}")


def excluir_tarefa():
    """
    Realiza exclusão lógica atualizando o status para 'Excluída'.
    """
    global TAREFAS
    print("Executando a função excluir_tarefa")
    try:
        task_id = int(input('Informe o ID da tarefa a excluir: '))
    except Exception:
        print('ID inválido.')
        return
    tarefa = encontrar_tarefa_por_id(task_id)
    if not tarefa:
        print('Tarefa não encontrada.')
        return
    tarefa['status'] = 'Excluída'
    print(f"Tarefa {task_id} marcada como Excluída (exclusão lógica).")


def relatorio_tarefas():
    """
    Exibe na tela todas as tarefas com suas informações completas.
    Para tarefas concluídas, calcula e exibe o tempo de execução.
    """
    print("Executando a função relatorio_tarefas")
    if not TAREFAS:
        print('Nenhuma tarefa cadastrada.')
        return
    for t in TAREFAS:
        
        print('-' * 40)
        print(f"ID: {t.get('id')}")
        print(f"Título: {t.get('titulo')}")
        print(f"Descrição: {t.get('descricao')}")
        print(f"Prioridade: {t.get('prioridade')}")
        print(f"Status: {t.get('status')}")
        print(f"Origem: {t.get('origem')}")
        print(f"Data de criação: {t.get('data_criacao')}")
        if t.get('data_conclusao'):
            print(f"Data de conclusão: {t.get('data_conclusao')}")
            # calcular tempo de execução
            try:
                dt_inicio = datetime.fromisoformat(t.get('data_criacao'))
                dt_fim = datetime.fromisoformat(t.get('data_conclusao'))
                duracao = dt_fim - dt_inicio
                dias = duracao.days
                segundos = duracao.seconds
                horas = segundos // 3600
                minutos = (segundos % 3600) // 60
                print(f"Tempo de execução: {dias} dias, {horas} horas, {minutos} minutos")
            except Exception:
                print('Não foi possível calcular tempo de execução.')
    print('-' * 40)


def relatorio_arquivados():
    """
    Exibe apenas as tarefas com status Arquivado (do arquivo de arquivadas).
    Tarefas Excluídas não devem constar neste relatório.
    """
    print("Executando a função relatorio_arquivados")
    try:
        with open(ARQUIVO_ARQUIVADAS, 'r', encoding='utf-8') as f:
            hist = json.load(f)
    except Exception:
        hist = []
    # Filtrar tarefas excluídas apenas por segurança (não deveriam estar no arquivo)
    filtradas = [t for t in hist if t.get('status') != 'Excluída']
    if not filtradas:
        print('Não há tarefas arquivadas.')
        return
    for t in filtradas:
        print('-' * 40)
        print(f"ID: {t.get('id')}")
        print(f"Título: {t.get('titulo')}")
        print(f"Prioridade: {t.get('prioridade')}")
        print(f"Status: {t.get('status')}")
        print(f"Origem: {t.get('origem')}")
        print(f"Data de criação: {t.get('data_criacao')}")
        if t.get('data_conclusao'):
            print(f"Data de conclusão: {t.get('data_conclusao')}")
    print('-' * 40)


# -------------------------
# Menu principal e fluxo
# -------------------------

def menu_principal():
    """
    Exibe o menu principal do sistema e gerencia a navegação entre opções.
    Valida a opção antes de executar e chama funções modulares.
    """
    print("Executando a função menu_principal")
    opcoes = {
        '1': ('Criar tarefa', criar_tarefa),
        '2': ('Verificar urgência e começar tarefa', verificar_urgencia),
        '3': ('Atualizar prioridade', atualizar_prioridade),
        '4': ('Concluir tarefa', concluir_tarefa),
        '5': ('Arquivar tarefas antigas (limpeza)', arquivar_tarefas_antigas),
        '6': ('Excluir tarefa (exclusão lógica)', excluir_tarefa),
        '7': ('Relatório completo', relatorio_tarefas),
        '8': ('Relatório de arquivadas', relatorio_arquivados),
        '9': ('Salvar e Sair', None)
    }

    while True:
        print('\n=== MENU PRINCIPAL ===')
        for k, v in opcoes.items():
            print(f"{k} - {v[0]}")
        escolha = input('Escolha uma opção: ').strip()
        if escolha not in opcoes:
            print('Opção inválida. Tente novamente.')
            continue
        if escolha == '9':
            # Antes de sair, executar arquivamento automático e salvar
            arquivar_tarefas_antigas()
            salvar_dados()
            print('Dados salvos. Encerrando o programa.')
            sys.exit(0)
        
        func = opcoes[escolha][1]
        try:
            func()
        except Exception as e:
            print(f"Ocorreu um erro ao executar a opção: {e}")


# -------------------------
# Entrada do programa
# -------------------------

if __name__ == '__main__':
    verificar_e_criar_arquivos()
    carregar_dados()
    # Executa arquivamento automático ao iniciar (limpeza)
    arquivar_tarefas_antigas()
    # Inicia menu
    menu_principal()
