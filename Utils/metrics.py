import math
from Utils.utils import clean_movie_name

def calculate_average_metrics(results):
    """
    Calcula a média das métricas 'hit', 'precision', 'recall' e 'ndcg' dentro do dicionário results.
    
    Parâmetros:
        results (dict): Dicionário contendo os resultados das recomendações.
    
    Retorna:
        dict: Dicionário com a média de cada métrica.
    """
    
    # Inicializa um dicionário para armazenar a soma das métricas
    metric_sums = {
        'hit': 0,
        'precision': 0,
        'recall': 0,
        'ndcg': 0
    }
    
    # Contador para armazenar quantas recomendações foram processadas
    num_recommendations = 0
    
    # Percorre as chaves e valores do dicionário results
    for key, value in results.items():
        # Verifica se a chave é um número inteiro (ou seja, um índice de recomendação)
        if isinstance(key, int) and isinstance(value, dict):
            # Percorre cada métrica relevante e soma os valores
            for metric in metric_sums.keys():
                if metric in value:
                    metric_sums[metric] += value[metric]
            
            # Incrementa o contador de recomendações processadas
            num_recommendations += 1
    
    # Verifica se há recomendações para evitar divisão por zero
    if num_recommendations == 0:
        return {metric: 0 for metric in metric_sums}  # Retorna 0 para todas as métricas
    
    # Calcula a média de cada métrica
    average_metrics = {
        metric: total / num_recommendations for metric, total in metric_sums.items()
    }
    
    return average_metrics

def calculate_metrics(query, relevants):
    """
    Calcula as métricas de precisão, revocação e F1 para uma lista de recomendações e itens relevantes.
    
    Args:
    - query (list): Lista de itens recomendados.
    - relevants (list): Lista de itens relevantes.
    
    Returns:
    - dict: Dicionário com as métricas calculadas.
    """

    recommendations_set = {clean_movie_name(movie) for movie in query.split("; ")}
    ground_truth_set = {clean_movie_name(relevants)}

    # Calcula o HirRate (eficácia)
    hit = calculate_hit(recommendations_set,ground_truth_set)

    # Calcula a precisão
    precision = calculate_precision(recommendations_set, ground_truth_set)
    
    # Calcula a revocação
    recall = calculate_recall(recommendations_set, ground_truth_set)
    
    # Calcula o NDGC
    ndcg = calculate_ndcg(recommendations_set, ground_truth_set)

    return {
        "recommendation_set": recommendations_set,
        "ground_truth_set": ground_truth_set,
        "hit": hit,
        "precision": precision,
        "recall": recall,
        "ndcg": ndcg
    }

def calculate_hit(query, relevants):
    """
    Calcula o Hit Rate (HR@K).
    
    query: Lista de itens recomendados para o usuário.
    relevants: Lista de itens relevantes para o usuário.
    
    Retorna 1 se pelo menos um item relevante estiver na lista de recomendações, senão retorna 0.
    """
    return int(bool(set(query) & set(relevants)))  # Retorna 1 se houver interseção, senão 0


def calculate_hitrate_old(data):
    """
    Calcula a eficácia do modelo com base na métrica 'hit'.
    """

    # Filtra apenas as entradas numéricas (os testes)
    recomendacoes = [v for k, v in data.items() if isinstance(k, int)]
    
    # Conta os hits
    hits = sum(1 for recomendacao in recomendacoes if recomendacao.get("hit", False))
    
    # Número total de testes
    total_recomendacoes = len(recomendacoes)
    
    # Evita divisão por zero
    if total_recomendacoes == 0:
        return 0.0
    
    # Calcula a eficácia (acurácia)
    eficacia = hits / total_recomendacoes
    
    return eficacia


def calculate_precision(query, relevants):
    """
    Essa função calcula a precisão (Precision@K), que mede a proporção dos itens recomendados que são realmente relevantes.

    Como funciona:

    1 - Transforma query (itens recomendados) e relevants (itens realmente relevantes) em conjuntos.

    2 - Calcula a interseção entre os dois conjuntos (os itens que são relevantes e foram recomendados).

    3 -Divide pelo total de itens recomendados para obter a precisão.
    """

    query_set = set(query)
    rel_set = set(relevants)

    return len(query_set.intersection(rel_set)) / len(query_set)

def calculate_recall(query, relevants):
    """
    Essa função calcula a revocação (Recall@K), que mede a proporção dos itens relevantes que foram recuperados.
    
    Como funciona:

    1 - Transforma query e relevants em conjuntos.

    2 - Calcula a interseção entre os dois conjuntos.

    3 - Divide pelo total de itens relevantes.
    """

    query_set = set(query)
    rel_set = set(relevants)

    return len(query_set.intersection(rel_set)) / len(rel_set)

def calculate_dcg(gain, pos):
    """
    Essa função calcula o Discounted Cumulative Gain (DCG), que mede a qualidade da ordenação das recomendações, penalizando itens relevantes que aparecem em posições mais baixas da lista.
    
    Como funciona:

    1 - Recebe o ganho de relevância (gain, geralmente 1 para itens relevantes).

    2 - Divide pelo logaritmo da posição do item na lista (log2(1+pos)).

    3 - Quanto menor a posição (pos mais próximo do topo da lista), maior o impacto na pontuação.
    """
    return gain / math.log2(1+pos)  # DCG is accumulated of 'relevance / log2(pos + 1)'


def calculate_ndcg(query, relevants):
    """
    Essa função calcula o Normalized Discounted Cumulative Gain (nDCG), que é a versão normalizada do DCG para comparar listas de recomendações de diferentes tamanhos.
    
    Como funciona:

    1 - Calcula o DCG, que mede a qualidade da ordenação das recomendações.

    2 - Calcula o IDCG (Ideal DCG), que é o DCG da melhor ordenação possível (todos os itens relevantes no topo).

    3 - Retorna a normalização nDCG = DCG / IDCG.
    """

    dcg = 0
    idcg = 0

    for i,item in enumerate(query):
        idcg += calculate_dcg(1,i+1) if i < len(relevants) else 0 # Calcula o IDCG se houver relevantes, senão, apenas não muda o IDCG já calculado -- a relevância dos itens corretos (ground-truths) é 1 quando existir. 
        dcg += calculate_dcg(1,i+1) if item in relevants else 0 # Calcula o DCG se o item recomendado está na lista de relevantes (ground-truths), senão, não muda o DCG -- a relevância dos itens corretos (GT) é 1
    #print(f'[{i}] - IDCG: {idcg} | DCG: {dcg}')
    return dcg / idcg