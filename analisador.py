import re

# cores ansi
C = '\033[96m'
G = '\033[92m'
Y = '\033[93m'
R = '\033[91m'
W = '\033[97m'
D = '\033[90m'
RS = '\033[0m'

# dicionários de palavras-chave reais para o rgpd
dicionario_principios = {
    "licitude": ["consentimento", "base legal", "finalidade do tratamento", "legítimo interesse", "contrato"],
    "finalidade": ["propósito específico", "finalidade", "não processamos para outros fins", "apenas para"],
    "minimizacao": ["minimização", "estritamente necessário", "apenas o necessário", "adequados e limitados"],
    "exatidao": ["atualizar", "corrigir", "exatidão", "precisos", "retificar"],
    "conservacao": ["prazo de retenção", "eliminação automática", "período necessário", "exclusão", "conservação"],
    "seguranca": ["criptografia", "medidas técnicas", "acesso não autorizado", "confidencialidade", "segurança"],
    "responsabilidade": ["dpo", "encarregado de proteção", "auditoria", "comprovar", "accountability", "responsabilidade proativa"]
}

dicionario_direitos = {
    "acesso": ["direito de acesso", "solicitar uma cópia", "acessar seus dados"],
    "retificacao": ["direito de retificação", "corrigir seus dados", "atualizar informações"],
    "supressao": ["direito ao esquecimento", "apagar", "excluir conta", "direito de supressão"],
    "portabilidade": ["portabilidade", "transferir seus dados", "formato estruturado"],
    "oposicao": ["direito de oposição", "recusar", "opt-out", "cancelar inscrição"],
    "decisoes_auto": ["decisões automatizadas", "profiling", "intervenção humana", "definição de perfis"]
}

def limpar_texto(texto):
    return texto.lower()

def buscar_palavras(dicionario, texto):
    encontradas = {}
    total_ocorrencias = 0
    for palavra in dicionario:
        qtd = len(re.findall(r'\b' + re.escape(palavra) + r'\b', texto))
        if qtd > 0:
            encontradas[palavra] = qtd
            total_ocorrencias += qtd
    return encontradas, total_ocorrencias

def barra_progresso(nivel):
    if nivel == 2: return f"{G}[████████████████████]{RS}"
    if nivel == 1: return f"{Y}[██████████░░░░░░░░░░]{RS}"
    return f"{R}[░░░░░░░░░░░░░░░░░░░░]{RS}"

def analisar_politica():
    print(f"{C}╔══════════════════════════════════════════════════════╗{RS}")
    print(f"{C}║     ANALISADOR DE POLÍTICAS DE PRIVACIDADE — RGPD    ║{RS}")
    print(f"{C}╚══════════════════════════════════════════════════════╝{RS}")
    
    empresa = input(f"\nNome da empresa/serviço analisado: {C}")
    print(f"{RS}Cole a política. Digite {Y}FIM{RS} em uma nova linha para analisar:")
    print(f"{D}> ", end="")
    
    linhas_texto = []
    while True:
        linha = input()
        if linha.strip().upper() == "FIM":
            break
        linhas_texto.append(linha)
    
    texto_analise = limpar_texto(" ".join(linhas_texto))
    total_palavras = len(texto_analise.split())

    print(f"\n{Y}⏳ Analisando...{RS}\n")

    print(f"{D}──────────────────────────────────────────────────────{RS}")
    print(f"{W} RESULTADO — {empresa.upper()}{RS}")
    print(f"{D}──────────────────────────────────────────────────────{RS}")
    print(f" Texto analisado : {total_palavras} palavras")
    print(f"{D}──────────────────────────────────────────────────────{RS}\n")

    # analisando princípios reais
    score_principios = 0
    titulos_principios = ["Licitude e Transparência", "Limitação de Finalidade", "Minimização de Dados", "Exatidão", "Limitação da Conservação", "Integridade e Segurança", "Responsabilidade Proativa"]
    
    for i, (chave, palavras) in enumerate(dicionario_principios.items()):
        encontradas, total = buscar_palavras(palavras, texto_analise)
        
        print(f" PRINCÍPIO {i+1} · {titulos_principios[i]}")
        
        if total >= 2:
            print(f" {barra_progresso(2)} {G}ENCONTRADO{RS}")
            score_principios += 1
        elif total == 1:
            print(f" {barra_progresso(1)} {Y}PARCIAL{RS}")
            score_principios += 0.5
        else:
            print(f" {barra_progresso(0)} {R}NÃO ENCONTRADO{RS}")
            
        if encontradas:
            for p, qtd in encontradas.items():
                print(f"   ✓ Menciona \"{p}\" ({qtd}x)")
        else:
            print(f"   {R}✗ Nenhuma palavra-chave detectada{RS}")
        print()

    # analisando direitos reais
    print(f"{D}──────────────────────────────────────────────────────{RS}")
    print(f"{W} DIREITOS DOS USUÁRIOS{RS}")
    print(f"{D}──────────────────────────────────────────────────────{RS}")
    
    score_direitos = 0
    for direito, palavras in dicionario_direitos.items():
        encontradas, total = buscar_palavras(palavras, texto_analise)
        nome_formatado = direito.replace("_", " ").title()
        
        if total > 0:
            print(f" ✓ Direito de {nome_formatado.ljust(16)} {G}mencionado{RS}")
            score_direitos += 1
        else:
            print(f" {R}✗{RS} Direito de {nome_formatado.ljust(16)} {R}não encontrado{RS}")

    print(f"\n{D}──────────────────────────────────────────────────────{RS}")
    print(f"{W} PONTUAÇÃO FINAL{RS}")
    print(f"{D}──────────────────────────────────────────────────────{RS}\n")
    
    # cálculo de score de 0 a 100
    peso_principios = (score_principios / 7) * 60
    peso_direitos = (score_direitos / 6) * 40
    score_geral = round(peso_principios + peso_direitos)

    print(f" Princípios cobertos  : {score_principios}/7")
    print(f" Direitos cobertos    : {score_direitos}/6")
    
    if score_geral >= 80:
        status = f"{G}{score_geral}/100 — ALTA CONFORMIDADE{RS}"
    elif score_geral >= 50:
        status = f"{Y}{score_geral}/100 — CONFORMIDADE PARCIAL{RS}"
    else:
        status = f"{R}{score_geral}/100 — BAIXA CONFORMIDADE{RS}"
        
    print(f" Score geral          : {status}\n")
    print(f"{D}──────────────────────────────────────────────────────{RS}")

if __name__ == "__main__":
    while True:
        analisar_politica()
        resp = input(f" Analisar outra política? (s/n): {D}_{RS}\b")
        if resp.lower() != 's':
            break
        print("\n" * 2)