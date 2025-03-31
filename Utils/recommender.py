import wandb
import random
import time
from tqdm.notebook import tqdm
from Utils import metrics,utils

def recommendation_workflow(config, wandb_key, dataset, prompt_template, prompt_format, run_wandb):

    if run_wandb: 
        wandb.login(key=wandb_key)

    id_list = list(range(0, len(dataset)))
    #assert(len(id_list) == 943) # aqui é verificado se a lista possue exatamente essa quantidade

    # Building indexes and similarity matrices for users and movies.
    movie_idx = utils.build_moviename_index_dict(dataset)
    user_sim_matrix = utils.build_user_similarity_matrix(dataset, movie_idx)
    pop_dict = utils.build_movie_popularity_dict(dataset)
    item_sim_matrix = utils.build_item_similarity_matrix(dataset)

    results = {'config': config}

    nsu = config["nsu"]
    nci = config["nci"]
    lenlimit = config["lenlimit"]

    results['start_time'] = time.time()

    if run_wandb:
        # inicia a run do wandb
        run = wandb.init(project="test",config=config)

    if config["test_run"]:
        id_list = id_list[:config["test_run"]] # Define a quantiadade que será processado

    try:

        for i in tqdm(id_list, desc="Processando", unit="it"): 

            results[i] = {}

            watched_mv = dataset[i][0].split(' | ')[::-1]
            results[i]['ground_truth'] = dataset[i][-1]

            # Generate candidate items based on user filtering.
            candidate_items = utils.sort_collaborative_user_filtering(target_user_id=i,
                                                                    dataset=dataset,
                                                                    user_similarity_matrix=user_sim_matrix,
                                                                    num_users=nsu,
                                                                    num_items=nci,
                                                                    include_similar_user_GT=False,
                                                                    debug=False)
            random.shuffle(candidate_items)

            results[i]['candidate_set'] = candidate_items

            # verifica se o ground_truth está no candidate_set
            results[i]['gt_in_candidate_set'] = "yes" if any(results[i]['ground_truth'].lower() in candidate.lower() for candidate in results[i]['candidate_set']) else "no"

            # pipeline 

            # STEP 1
            input_1 = prompt_template['Preference'].format(', '.join(watched_mv[-lenlimit:]))
            results[i]['input_1'] = input_1
            response = utils.query_lm_studio(config["model_name"],config["Temperature"],prompt_template['System_prompt'],input_1,config["max_tokens"])
            predictions_1 = response
            results[i]['predictions_1'] = predictions_1

            # STEP 2
            input_2 = prompt_template['Featured_movies'].format(', '.join(watched_mv[-lenlimit:]), predictions_1)
            results[i]['input_2'] = input_2
            response = utils.query_lm_studio(config["model_name"],config["Temperature"],prompt_template['System_prompt'],input_2,config["max_tokens"])
            predictions_2 = response
            results[i]['predictions_2'] = predictions_2

            # STEP 3
            input_3 = prompt_template['Recommendation'].format(', '.join(candidate_items),', '.join(watched_mv[-lenlimit:]), predictions_1, predictions_2)
            results[i]['input_3'] = input_3
            response = utils.query_lm_studio(config["model_name"],config["Temperature"],prompt_template['System_prompt'],input_3,config["max_tokens"])
            predictions_3 = response
            results[i]['predictions_3'] = predictions_3


            # STEP 4 - Formate the response
            if prompt_format:
                input_4 = prompt_format['Prompt'].format(predictions_3)
                response = utils.query_lm_studio(config["model_name"],config["Temperature"],prompt_format['System_prompt'],input_4,config["max_tokens"])
                recommendations = response
                results[i]['recommendations'] = recommendations
                # Calculate metrics
                run_metrics = metrics.calculate_metrics(results[i]['recommendations'], results[i]['ground_truth'])    
            else:
                # Calculate metrics
                run_metrics = metrics.calculate_metrics(results[i]['predictions_3'], results[i]['ground_truth'])    
            
            results[i]['hit'] = run_metrics['hit']
            results[i]['precision'] = run_metrics['precision']
            results[i]['recall'] = run_metrics['recall']
            results[i]['ndcg'] = run_metrics['ndcg']

            if run_wandb:
                # Log do wandb
                run.log({
                    'Hit': results[i].get('hit', 0),  # Usa 0 como valor padrão se a chave não existir
                    'Precision': results[i].get('precision', 0),
                    'Recall': results[i].get('recall', 0),
                    'NDCG': results[i].get('ndcg', 0),
                    'result': "Ground Truth:" +results[i].get('ground_truth','') +"\n\n"+  results[i].get('input_3', '') + results[i].get('predictions_3', ''),
                })

        results['end_time'] = time.time()
        results['runtime'] = results['end_time'] - results['start_time']

        # calculate average metrics
        results['metrics'] = metrics.calculate_average_metrics(results)

        if run_wandb:
            # Atualiza o wandb com os resultados
            run.log({
                'HitRate@10': results['metrics']['hit'],
                'Precision': results['metrics']['precision'],
                'Recall': results['metrics']['recall'],
                'NDCG@10': results['metrics']['ndcg']
            })

        # save dictionary to pickle file
        arq_name = utils.save_result_to_pickle(results, config)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if run_wandb:
            run.finish()
            wandb.finish()

    return arq_name
