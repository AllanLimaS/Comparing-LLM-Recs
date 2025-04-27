# orientação 24/03/2025

## Json
    limpado os json, retirando o (ano) e também em alguns casos eles tinham um formato estranho do titulo como por exemplo "Matrix, the" 

## templates de prompt
    feito um template com apenas 3 passos em que o ultimo tem como resposta uma lista ordenada e estruturada de recomendações.

## Run times 
    CPU 
    extremamente lento

    ROCM
    tempo ok 
    FLASH ATTENTION não surtiu diferença significativa.

    Vulkan
    tempo levemente melhor que ROCm
    FLASH ATTENTION deixou extremamente lento. 


# orientação 31/03/2025 

## oque fazer 

    [ok] fazer teste sem a filtragem colaborativa ( passando todos os filmes dentro do prompt )
    [ok] implementar a função para executar as recomendações apenas para quem tem gt 
    [ok] Testar com temperatura 0

verificar as possibilidades do finetuning 


## oque foi feito 

    Ajustado o pipeline para mandar para o LLM apenas quando existe o GT no candidate_set

    ajustado os calculos de métricas para calcular os @5 e @10 de cada métrica

    ajustado os logs no wandb -> percebi que nao tenho mais acesso ao wandb -> retirando o uso do wandb 

    pesquisando alternativas para comparar as configurações e resultados

    criando um aplicativo StreamLib 

    comparação de diferentes valores de lenLimit (teste passando todos filmes como candidatos.)

    Comparação de diferentes valores para NSU e NCI  
    
    Comparação de temperaturas diferentes


# orientação 7/04/2025 

## oque fazer 

    fazer um teste passando todos os filmes para mais 95 usuários, para termos 10% da base experimentada nesse cenário 
    fazer teste com diferentes posições na lista de filmes assistidos. [ pegar do final da lista(mais recentes) | mandar no prompt em ordem cronológica]

    para NCI NSU usar os mesmo parametros do Sbbd

    instrução de treinamento 
        prompt com apenas o gt na lista de recomendação final 
        passar apenas a ultima parte do prompt

    fazer a divisão do treinamento sobre apenas os usuários com gt no candidato. 

    fazer teste alterando o prompt, onde é especificado que a lista de filmes assistidos se refere aos mais recentes. 
    nos graficos de métricas, manter a escala do eixo y 

## oque foi feito 

    teste com template indicando questão temporal dos filmes assistidos. 

    feito os datasets de teste e treino 

    Fine tunning 
        Unsloth colab, deu certo, resultado pessimo
        llama factory colab, nao deu certo
        llama factory local, nao deu certo
        llama factory docker, nao deu certo
        guia oficial rocm/amd, pc travou carregando modelo de 1B parametro. 

    
### lista de moedelos 

    apresentado no TCC2: 
        Llama 3,
        Llama 3.1,
        Llama 3.2,
        Ministral,
        Gemma
    
    lista de modelos que podem ser utilizados:
    
        LLama 
            [X] Llama 4     - (muito grande)
            [X] Llama 3.3   - (muito grande)
            Llama 3.2 1B    - unsloth/Llama-3.2-1B-Instruct-GGUF  (F16 \ Q4_K_M \ Q2_L)
            Llama 3.2 3B    - unsloth/Llama-3.2-3B-Instruct-GGUF
            Llama 3.1 8B    - lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF
            Llama 3 8B      - QuantFactory/Meta-Llama-3-8B-Instruct-GGUF
            Llama 2 7B      - TheBloke/Llama-2-7B-GGUF

        mistral 
            [X]Mistral small   - unsloth/Mistral-Small-3.1-24B-Instruct-2503-GGUF (talvez)
            Ministral       - bartowski/Ministral-8B-Instruct-2410-GGUF

        google 
            Gemma 3 12B     - lmstudio-community/gemma-3-12b-it-GGUF    
            Gemma 3 4B      - lmstudio-community/gemma-3-4b-it-GGUF
            Gemma 3 1B      - lmstudio-community/gemma-3-1b-it-GGUF
            Gemma 2 2B      - lmstudio-community/gemma-2-2b-it-GGUF
            Gemma 2 9B      - lmstudio-community/gemma-2-9b-it-GGUF

        outros, populares em benchmarks 
            Qwen 2.5        - lmstudio-community/Qwen2.5-7B-Instruct-1M-GGUF
            phi 4 microsoft - lmstudio-community/phi-4-GGUF (talvez ) 


# orientação 14/04/2025 


## anotações importantes 

    comentar sobre como alguns modelos são mais sensiveis a troca de prompts 

    experimentos para comparativo
        1 - diferença de versões de modelos
        2 - diferença de modelos
        3 - diferença de quantiazação 
        4 - ml100k e ml1M
        5 - finetuning
        6 - diferença entre prompts
        7 - quantidades de itens do histórico do usuário para o prompt

## oque fazer 

fazer teste com um prompt de 1 etapa apenas com os 3 itens originais. 

fine tuning , com resultados para coletar 

alterar a questão dos filmes assistidos que são passados por prompt 
    pegar: 8 do inicio | 8 aleatorio | 8 do final 
    sempre em ordem de mais antigo para mais novo 

testar o ml1M 
testar modelos PHI e QWEN 

juntar as anotações importantes do notion aqui 

## oque foi feito 

    Fine Tuning
        Ajustado o dataset de treino, antes ele estava passando mais "filmes assistidos" que deveria, agora está passando apenas os 8 ultimos.
        varias tentativas de finetunning, problemas com o uso de GPU do colab expirando e outros problemas.

        consegui treinar um modelo, teve resultados consideraveis, porem precisa verificar oque está especificado ali em "duvidas"

    testes com alteração de onde pegar os 8 filmes assistidos ( inicio, fim e aleatorio )

    teste com ML1M 

    teste de modelos 
        [ok] qwen2.5-7b-instruct-1m
        [ok] phi-4
        [ok] ministral-8b-instruct-2410
        [ok] Llama 3.2 1B F16
        [ok] Llama 3.2 3B F16
        [não] mistral-small-3.1-24b-instruct-2503 - no Q_4_K_M naõ rodou, mas em uma quantização mais forte roda


## Duvidas 

    o ministral teve metricas bem ruins, pois ele nao conseguia seguir o padrão do nome dos filmes passados 

    por exemplo 

    o gt é "Shawshank Redemption", e estava com essa exata nomenclatura na lista de candidatos 
    porem essa foi a lista de recomendações dele, por causa do "the" não foi tido um Hit, sigo nessa linha? ou ajusto a função para considerar isso um Hit

        "1. The Shawshank Redemption
        2. Heathers
        3. Manchurian Candidate
        4. Big Sleep
        5. Cape Fear
        6. Stand by Me
        7. Seven (Se7en)
        8. Terminator 2: Judgment Day
        9. True Lies
        10. Searching for Bobby Fischer"

    ou também ocorre assim

        "1. **Shawshank Redemption** (1997)
        2. **Full Monty** (2000)
        3. **Liar Liar** (1997)
        4. **Evita** (1996)
        5. **In & Out** (1997)
        6. **Dante's Peak** (1997)
        7. **Cop Land** (1997)
        8. **Scream** (1996)
        9. **Jerry Maguire** (1996)
        10. **Contact** (1997)"



# orientação 24/04/2025 

## anotações 

esparcidade do dataset movielens
https://www.d2l.ai/chapter_recommender-systems/movielens.html

## oque fazer 

    fazer o calculo das métricas hitrate utilizando um contains simples. 
    caso de muita difereça, tentar limpar as respostas com regex para trabalhar com ndcg. 

    fazer mais testes com ordem de filmes assistidos 
        utilizando dataset inteiro / com mais modelos

    começar os experimentos para valer, depois desses dois detalhes. 
    iniciar anotações: 
        justificativa de escolhas do experimento
        objetivo do experimento ( oque é esperado descobrir)
        resultado