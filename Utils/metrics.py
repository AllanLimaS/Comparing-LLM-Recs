import math
from Utils.utils import clean_movie_name, extract_movie_titles, clean_movie_name_new, extract_movie_list, clean_movie_name_extra_infos

def calculate_average_metrics(results):
    """
    Calcula a média geral das métricas e a média das métricas apenas quando gt_in_candidate_set == True.

    Parâmetros:
        results (dict): Dicionário contendo os resultados das recomendações.

    Retorna:
        dict: Dicionário com a média de cada métrica, geral e filtrada.
    """

    # Inicializa as somas das métricas
    total_metrics = {
    'avg_HitRate@5': 0, 'avg_Precision@5': 0, 'avg_Recall@5': 0, 'avg_NDCG@5': 0,
    'avg_HitRate@10': 0, 'avg_Precision@10': 0, 'avg_Recall@10': 0, 'avg_NDCG@10': 0
    }

    filtered_metrics = {
        'avg_GT_HitRate@5': 0, 'avg_GT_Precision@5': 0, 'avg_GT_Recall@5': 0, 'avg_GT_NDCG@5': 0,
        'avg_GT_HitRate@10': 0, 'avg_GT_Precision@10': 0, 'avg_GT_Recall@10': 0, 'avg_GT_NDCG@10': 0
    }

    count_total = 0
    count_filtered = 0

    for key, value in results.items():
        if isinstance(key, int) and isinstance(value, dict):
            # Soma para total (@5 e @10)
            total_metrics['avg_HitRate@5'] += value.get('rec_HitRate@5', 0)
            total_metrics['avg_Precision@5'] += value.get('rec_Precision@5', 0)
            total_metrics['avg_Recall@5'] += value.get('rec_Recall@5', 0)
            total_metrics['avg_NDCG@5'] += value.get('rec_NDCG@5', 0)

            total_metrics['avg_HitRate@10'] += value.get('rec_HitRate@10', 0)
            total_metrics['avg_Precision@10'] += value.get('rec_Precision@10', 0)
            total_metrics['avg_Recall@10'] += value.get('rec_Recall@10', 0)
            total_metrics['avg_NDCG@10'] += value.get('rec_NDCG@10', 0)

            count_total += 1

            # Soma apenas para os casos filtrados
            if value.get('gt_in_candidate_set') == True:
                filtered_metrics['avg_GT_HitRate@5'] += value.get('rec_HitRate@5', 0)
                filtered_metrics['avg_GT_Precision@5'] += value.get('rec_Precision@5', 0)
                filtered_metrics['avg_GT_Recall@5'] += value.get('rec_Recall@5', 0)
                filtered_metrics['avg_GT_NDCG@5'] += value.get('rec_NDCG@5', 0)

                filtered_metrics['avg_GT_HitRate@10'] += value.get('rec_HitRate@10', 0)
                filtered_metrics['avg_GT_Precision@10'] += value.get('rec_Precision@10', 0)
                filtered_metrics['avg_GT_Recall@10'] += value.get('rec_Recall@10', 0)
                filtered_metrics['avg_GT_NDCG@10'] += value.get('rec_NDCG@10', 0)

                count_filtered += 1

    # Cálculo das médias
    average_total = {
        metric: total / count_total if count_total else 0 for metric, total in total_metrics.items()
    }

    average_filtered = {
        metric: total / count_filtered if count_filtered else 0 for metric, total in filtered_metrics.items()
    }

    # Junta tudo em um único dicionário
    final_result = average_total.copy()
    for key, value in average_filtered.items():
        final_result[key] = value
    return final_result

def calculate_average_metrics_new(results):
    """
    Calcula a média geral das métricas e a média das métricas apenas quando gt_in_candidate_set == True.

    Parâmetros:
        results (dict): Dicionário contendo os resultados das recomendações.

    Retorna:
        dict: Dicionário com a média de cada métrica, geral e filtrada.
    """

    # Inicializa as somas das métricas
    total_metrics = {
    'avg_HitRate@5': 0, 'avg_NDCG@5': 0, 'avg_HitRate@5_safe': 0, 'avg_NDCG@5_safe': 0,
    'avg_HitRate@10': 0, 'avg_NDCG@10': 0., 'avg_HitRate@10_safe': 0, 'avg_NDCG@10_safe': 0.
    }

    filtered_metrics = {
        'avg_GT_HitRate@5': 0, 'avg_GT_NDCG@5': 0, 'avg_GT_HitRate@5_safe': 0, 'avg_GT_NDCG@5_safe': 0,
        'avg_GT_HitRate@10': 0, 'avg_GT_NDCG@10': 0, 'avg_GT_HitRate@10_safe': 0, 'avg_GT_NDCG@10_safe': 0,
        'avg_GT_Hallucination': 0
    }

    count_total = 0
    count_filtered = 0

    for key, value in results.items():
        if isinstance(key, int) and isinstance(value, dict):
            # Soma para total (@5 e @10)
            total_metrics['avg_HitRate@5'] += value.get('rec_HitRate@5', 0)
            total_metrics['avg_NDCG@5'] += value.get('rec_NDCG@5', 0)
            total_metrics['avg_HitRate@5_safe'] += value.get('rec_HitRate@5_safe', 0)
            total_metrics['avg_NDCG@5_safe'] += value.get('rec_NDCG@5_safe', 0)

            total_metrics['avg_HitRate@10'] += value.get('rec_HitRate@10', 0)
            total_metrics['avg_NDCG@10'] += value.get('rec_NDCG@10', 0)
            total_metrics['avg_HitRate@10_safe'] += value.get('rec_HitRate@10_safe', 0)
            total_metrics['avg_NDCG@10_safe'] += value.get('rec_NDCG@10_safe', 0)

            count_total += 1

            # Soma apenas para os casos filtrados
            if value.get('gt_in_candidate_set') == True:
                filtered_metrics['avg_GT_HitRate@5'] += value.get('rec_HitRate@5', 0)
                filtered_metrics['avg_GT_NDCG@5'] += value.get('rec_NDCG@5', 0)
                filtered_metrics['avg_GT_HitRate@5_safe'] += value.get('rec_HitRate@5_safe', 0)
                filtered_metrics['avg_GT_NDCG@5_safe'] += value.get('rec_NDCG@5_safe', 0)

                filtered_metrics['avg_GT_HitRate@10'] += value.get('rec_HitRate@10', 0)
                filtered_metrics['avg_GT_NDCG@10'] += value.get('rec_NDCG@10', 0)
                filtered_metrics['avg_GT_HitRate@10_safe'] += value.get('rec_HitRate@10_safe', 0)
                filtered_metrics['avg_GT_NDCG@10_safe'] += value.get('rec_NDCG@10_safe', 0)

                filtered_metrics['avg_GT_Hallucination'] += value.get('rec_Hallucination', 0)

                count_filtered += 1

    # Cálculo das médias
    average_total = {
        metric: total / count_total if count_total else 0 for metric, total in total_metrics.items()
    }

    average_filtered = {
        metric: total / count_filtered if count_filtered else 0 for metric, total in filtered_metrics.items()
    }

    # Junta tudo em um único dicionário
    final_result = average_total.copy()
    for key, value in average_filtered.items():
        final_result[key] = value
    return final_result

def calculate_metrics(query, relevants):
    """
    Calcula as métricas de precisão, recall, hit e ndcg para @5 e @10.
    
    Args:
    - query (list): Lista de itens recomendados (ordenados por relevância).
    - relevants (list): Lista de itens relevantes.
    
    Returns:
    - dict: Dicionário com as métricas calculadas para @5 e @10.
    """

    metrics = {}

    for k in [5, 10]:

        recommendations_set = {clean_movie_name(movie) for movie in extract_movie_titles(query)}
        ground_truth_set = {clean_movie_name(relevants)}

        recommendations_set = list(recommendations_set)[:k]

        hit = calculate_hit(recommendations_set, ground_truth_set)
        precision = calculate_precision(recommendations_set, ground_truth_set)
        recall = calculate_recall(recommendations_set, ground_truth_set)
        ndcg = calculate_ndcg(recommendations_set, ground_truth_set)

        metrics[f"hit@{k}"] = hit
        metrics[f"precision@{k}"] = precision
        metrics[f"recall@{k}"] = recall
        metrics[f"ndcg@{k}"] = ndcg

    return metrics

def calculate_metrics_new(query, relevants, candidate_set):
    """
    Calcula as métricas de precisão, recall, hit e ndcg para @5 e @10.
    
    Args:
    - query (list): Lista de itens recomendados (ordenados por relevância).
    - relevants (str): String de item relevante.
    
    Returns:
    - dict: Dicionário com as métricas calculadas para @5 e @10.
    """

    metrics = {}

    for k in [5, 10]:
        metrics[f"hit@{k}"] = 0
        metrics[f"ndcg@{k}"] = 0
        metrics[f"hit@{k}_safe"] = 0
        metrics[f"ndcg@{k}_safe"] = 0

    query = clean_movie_name_new(query)
    lista_rec = extract_movie_list(query)

    ground_truth_set = [clean_movie_name_new(relevants)]

 
    for k in [5, 10]:

        recommendations_set = list(lista_rec)[:k]

        hit = calculate_hit_new(recommendations_set, ground_truth_set)
        ndcg = calculate_ndcg_new(recommendations_set, ground_truth_set)

        metrics[f"hit@{k}"] = hit
        metrics[f"ndcg@{k}"] = ndcg
        metrics[f"hit@{k}_safe"] = hit
        metrics[f"ndcg@{k}_safe"] = ndcg

    # Verifica se os itens recomendados estão no conjunto de candidatos

    candidate_set_clean = [clean_movie_name_extra_infos(movie) for movie in candidate_set]
    lista_rec_clean = [clean_movie_name_extra_infos(movie) for movie in lista_rec]
   
    #print(f"Lista de recomendações: {lista_rec_clean}")
    #print(f"Lista de relevantes: {ground_truth_set}")
    #print(f"Lista de candidatos: {candidate_set_clean}")

    hallucination = 0

    for item in lista_rec_clean:
        if item not in candidate_set_clean:
            hallucination = 1
            metrics["hit@5_safe"] = 0
            metrics["ndcg@5_safe"] = 0
            metrics["hit@10_safe"] = 0
            metrics["ndcg@10_safe"] = 0
            break

    metrics["hallucination"] = hallucination

    #print("metrics")
    #print(metrics)

    return metrics

def calculate_metrics_new_real(query, relevants, candidate_set):
    """
    Calcula as métricas de precisão, recall, hit e ndcg para @5 e @10.
    
    Args:
    - query (list): Lista de itens recomendados (ordenados por relevância).
    - relevants (str): String de item relevante.
    
    Returns:
    - dict: Dicionário com as métricas calculadas para @5 e @10.
    """


    #print(f"query: {query}")
    # Remove todo o texto que está antes do '1.'
    indice = query.find("1.")
    if indice != -1:
        query =  query[indice:].strip()
    #print(f"query com texto limpo antes de 1.: {query}")

    metrics = {}

    for k in [5, 10]:
        metrics[f"hit@{k}"] = 0
        metrics[f"ndcg@{k}"] = 0
        metrics[f"hit@{k}_safe"] = 0
        metrics[f"ndcg@{k}_safe"] = 0



    query = clean_movie_name_new(query)
    lista_rec = extract_movie_list(query)

    ground_truth_set = [clean_movie_name_new(relevants)]

 
    for k in [5, 10]:

        recommendations_set = list(lista_rec)[:k]

        hit = calculate_hit_new(recommendations_set, ground_truth_set)
        ndcg = calculate_ndcg_new(recommendations_set, ground_truth_set)

        metrics[f"hit@{k}"] = hit
        metrics[f"ndcg@{k}"] = ndcg
        metrics[f"hit@{k}_safe"] = hit
        metrics[f"ndcg@{k}_safe"] = ndcg

    # Verifica se os itens recomendados estão no conjunto de candidatos

    candidate_set_clean = [clean_movie_name_extra_infos(movie) for movie in candidate_set]
    lista_rec_clean = [clean_movie_name_extra_infos(movie) for movie in lista_rec]
   
    #print(f"Lista de recomendações: {lista_rec_clean}")
    #print(f"Lista de relevantes: {ground_truth_set}")
    #print(f"Lista de candidatos: {candidate_set_clean}")

    hallucination = 0

    for item in lista_rec_clean:
        if item not in candidate_set_clean:
            #print(f"lista recomdendada: {lista_rec_clean}")
            #print(f"Item {item} não está no conjunto de candidatos.{candidate_set_clean}")
            hallucination = 1
            metrics["hit@5_safe"] = 0
            metrics["ndcg@5_safe"] = 0
            metrics["hit@10_safe"] = 0
            metrics["ndcg@10_safe"] = 0
            break

    metrics["hallucination"] = hallucination

    #print("metrics")
    #print(metrics)

    return metrics

def calculate_hit(query, relevants):
    """
    Calcula o Hit Rate (HR@K).
    
    query: Lista de itens recomendados para o usuário.
    relevants: Lista de itens relevantes para o usuário.
    
    Retorna 1 se pelo menos um item relevante estiver na lista de recomendações, senão retorna 0.
    """
    return int(bool(set(query) & set(relevants)))  # Retorna 1 se houver interseção, senão 0

def calculate_hit_new(query, relevants):
    """
    Calcula o Hit Rate (HR@K).
    
    query: Lista de itens recomendados para o usuário.
    relevants: Lista de itens relevantes para o usuário.
    
    Retorna 1 se pelo menos um item relevante estiver na lista de recomendações, senão retorna 0.
    """
    for relevant in relevants:
        for item in query:
            if relevant in item:
                return 1
    return 0


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

def calculate_ndcg_new(query, relevants):
    """
    query = lista de itens recomendados (ordenados por relevância).
    relevants = lista de itens relevantes (ground-truths).
    """
    dcg = 0
    idcg = 0

    relevant = relevants[0]
    for i,item in enumerate(query):
        idcg += calculate_dcg(1,i+1) if i < len(relevants) else 0 # Calcula o IDCG se houver relevantes, senão, apenas não muda o IDCG já calculado -- a relevância dos itens corretos (ground-truths) é 1 quando existir.
        dcg += calculate_dcg(1,i+1) if relevant in item else 0 # Calcula o DCG se o item recomendado está na lista de relevantes (ground-truths), senão, não muda o DCG -- a relevância dos itens corretos (GT) é 1
    return dcg / idcg