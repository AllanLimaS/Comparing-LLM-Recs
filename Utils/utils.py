import json
import numpy as np
import requests
import json
from datetime import datetime
import pickle
import re

def query_lm_studio(model, temp, sytem_prompt, prompt, max_tokens):

    API_URL = "http://localhost:1234/v1/chat/completions"

    """Envia uma requisição para o LM Studio e retorna a resposta."""
    
    system_role = "assistant" if "mistral" in model else "system"

    payload = {
        "model": model,  # Nome do modelo carregado no LM Studio
        "messages": [
            {"role": system_role, "content": sytem_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": temp,
        "max_tokens": max_tokens, #-1, #512,  # Ajuste conforme necessário
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print("Erro:", response.status_code, response.text)
        return None

def save_result_to_pickle(results,config):
    # Gera um timestamp para garantir nomes únicos
    timestamp = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    arq_name = f'{config["dataset"]}-zs-nir-su{config['nsu']}-ci{config['nci']}-{config["model_name"]}-{timestamp}.pkl'
    arq_name = f'{config["dataset"]}-{config["model_name"]}-{timestamp}.pkl'
    with open(f'Results/{arq_name}', 'wb') as file:
        pickle.dump(results, file)
    return f'Results/{arq_name}'

def clean_movie_name(movie):
    """Remove o ano entre parênteses e converte para uppercase."""
    movie = re.sub(r"\s*\(\d{4}\)$", "", movie)  # Remove '(YYYY)'

    # Corrige títulos que começam com ", The" ou ", A" etc.
    movie = re.sub(r', (The|A|An)$', r'', movie)

    return movie.upper()  # Converte para uppercase

def extract_movie_titles(text):
    """Extrai os títulos dos filmes removendo a numeração"""
    return [re.sub(r"^\d+\.\s*", "", line).strip() for line in text.split("\n") if line.strip()]

def read_json(path: str):
    with open(path) as f:
        return json.load(f)

def build_moviename_index_dict(data):
    """
    Builds a dictionary mapping movie names to their indices.

    Args:
    - data (list): List of tuples where each tuple contains user data.

    Returns:
    - dict: Dictionary mapping movie names to their indices.
    """
    movie_names = set()
    for elem in data:
        seq_list = elem[0].split(' | ')
        movie_names.update(seq_list)
    return {movie: idx for idx, movie in enumerate(movie_names)}

def build_user_similarity_matrix(data, movie_idx):
    """
    Builds a user similarity matrix based on the watched movies data.

    Args:
    - data (list): List of tuples where each tuple contains user data.
    - movie_idx (dict): Dictionary mapping movie names to their indices.

    Returns:
    - numpy.ndarray: User similarity matrix.
    """
    user_matrix = [] # user matrix
    for elem in data:    # iterate over user watched movies
        item_hot_list = np.zeros(len(movie_idx))  # create one hot user-movie vector
        for movie_name in elem[0].split(' | '):  # iterate over each movie and update one hot vector
            item_pos = movie_idx[movie_name]
            item_hot_list[item_pos] = 1
        user_matrix.append(item_hot_list)   # add user vector to user matrix
    user_matrix = np.array(user_matrix)
    return np.dot(user_matrix, user_matrix.transpose()) # compute similarity (dot product)

def build_movie_popularity_dict(data):
    """
    Builds a dictionary mapping movie names to their popularity count.

    Args:
    - data (list): List of tuples where each tuple contains user data.

    Returns:
    - dict: Dictionary mapping movie names to their popularity count.
    """
    pop_dict = {}
    for elem in data:   # iterate over dataset
        seq_list = elem[0].split(' | ')
        for movie in seq_list:  # iterate over each movie
            if movie not in pop_dict:
                pop_dict[movie] = 0
            pop_dict[movie] += 1 # increment movie popularity
    return pop_dict

def build_item_similarity_matrix(data):
    """
    Builds an item similarity matrix based on the watched movies data.

    Args:
    - data (list): List of tuples where each tuple contains user data.

    Returns:
    - numpy.ndarray: Item similarity matrix.
    """
    i_item_dict = {}
    i_item_user_dict = {}
    i_item_p = 0

    for i, elem in enumerate(data):
        seq_list = elem[0].split(' | ') # user watched movie list
        for movie in seq_list:
            if movie not in i_item_user_dict:
                item_hot_list = np.zeros(len(data))
                i_item_user_dict[movie] = item_hot_list
                i_item_dict[movie] = i_item_p
                i_item_p += 1
            i_item_user_dict[movie][i] += 1

    item_matrix = np.array([x for x in i_item_user_dict.values()])
    return np.dot(item_matrix, item_matrix.transpose())

def sort_user_filtering_items(data, watched_movies, user_similarity_array, num_u, num_i):
    """
    Sorts and filters items based on user similarity.

    Args:
    - data (list): List of tuples where each tuple contains user data.
    - watched_movies (set): Set of watched movie names.
    - user_similarity_matrix (numpy.ndarray): User similarity matrix.
    - num_u (int): Number of users to consider.
    - num_i (int): Number of items to recommend.

    Returns:
    - list: List of recommended movie names.
    """
    candidate_movies_dict = {}
    sorted_us = sorted(list(enumerate(user_similarity_array)), key=lambda x: x[-1], reverse=True)[:num_u]
    dvd = sum([e[-1] for e in sorted_us])
    for us_i, us_v in sorted_us:
        us_w = us_v * 1.0 / dvd
        us_elem = data[us_i]
        us_seq_list = us_elem[0].split(' | ')
        for us_m in us_seq_list:
            if us_m not in watched_movies:
                if us_m not in candidate_movies_dict:
                    candidate_movies_dict[us_m] = 0.
                candidate_movies_dict[us_m] += us_w
    candidate_pairs = list(sorted(candidate_movies_dict.items(), key=lambda x:x[-1], reverse=True))
    candidate_items = [e[0] for e in candidate_pairs][:num_i]
    return candidate_items

def sort_collaborative_user_filtering(target_user_id, dataset, user_similarity_matrix, num_users, num_items,include_similar_user_GT=False,debug=False):
    #print(">>> Filtragem Colaborativa de Usuário -> Usuário-alvo: ",target_user_id)
    target_user_history = dataset[target_user_id][0].split(' | ')      # Obter o histórico do usuário-alvo sem o ground-truth
    target_user_similarities = user_similarity_matrix[target_user_id]  # Matriz de similaridade do usuários-alvo com demais usuários, quais usuários possuem mais itens em comum
    ### Método Original: Wang & Lim (2023) - problema de obter o próprio usuário-alvo na lista
    #sorted_similar_users = sorted(list(enumerate(target_user_similarities)), key=lambda x: x[-1], reverse=True)[:num_users] # Problema
    ### Ajuste: leave-one-out user -> solução: o usuário-alvo não estará contido na lista de similares
    sorted_similar_users = sorted(list(enumerate(target_user_similarities)), key=lambda x: x[-1], reverse=True)[:num_users+1]
    sorted_similar_users = list( filter(lambda x: x[0] != target_user_id, sorted_similar_users) )[:num_users] # Remove o "usuário-alvo" da lista similares, se ele aparecer
    ### Fim da mudança
    
    assert len(sorted_similar_users) == num_users # Garantir que o número de usuários similares é o solicitado.
    if debug:
        print("Histórico do usuário-alvo: ",target_user_history)
        print("Alvo / Ground-truth: ", dataset[target_user_id][1])
        print("Lista de usuários similares: ",sorted_similar_users)
    
    total_similar_items = sum([e[-1] for e in sorted_similar_users])

    candidate_items_dict = {}
    for similar_user_id, similar_user_common_items_count in sorted_similar_users:
        similar_user_similarity_score = similar_user_common_items_count / total_similar_items

        # Obter o histórico do usuário similar - SEM o ground-truth do similar (usado pelo Wang)
        similar_user_history = dataset[similar_user_id][0].split(' | ') 
        # Obter o histórico do usuário similar - COM o ground-truth do similar (sugerido, mas comentado no código de Wang)
        #similar_user_history = dataset[similar_user_id][0].split(' | ')+[dataset[similar_user_id][1]]
        if include_similar_user_GT:
            similar_user_history += [dataset[similar_user_id][1]]

        if debug: print(f"Histórico do usuário similar [{similar_user_id}]: ",similar_user_history)

        for similar_user_item in similar_user_history:
            if similar_user_item not in target_user_history:
                if similar_user_item not in candidate_items_dict:
                    candidate_items_dict[similar_user_item] = 0.
                candidate_items_dict[similar_user_item] += similar_user_similarity_score

    # Ordena os itens mais populares (que mais aparecem) entre os usuários mais similares de acordo com seus "scores" de similaridade
    candidate_pairs = list( sorted(candidate_items_dict.items(), key=lambda x: x[-1], reverse=True) )
    if debug: print(f'Candidatos da UF para o usuário `{target_user_id}` com o score de similaridade: ',candidate_pairs)
    candidate_items = [e[0] for e in candidate_pairs][:num_items]
    return candidate_items
