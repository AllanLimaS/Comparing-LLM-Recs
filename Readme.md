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

    
## lista de moedelos 

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

        com realação a configuração: 
            1 - diferença entre prompts (entre os usados anteriormente)
            2 - quantidades de itens do histórico do usuário para o prompt
            (??) - ordem dos itens da lista de watched movies

        com relação aos modelos: (evidenciar uma taxa de alucinação)
            3 - diferença de versões de modelos (entre familias)
            4 - diferença de quantiazação (llama 3.2)
            5 - diferença de modelos (entre vencedores das familias acima)

        com relação ao dataset e finetunning: 
            6 - finetuning (definir modelo melhor com base nos exp de cima  "com" e "sem")
            7 - ml100k e ml1M (entre os usados anteriormente)

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

## oque foi feito

    ajustada as funções de calculo de métricas
    primeiro testado o hit utilizando o contains diretamente, diferença foi consideravel (~20% de ganho).
    ajustado regex para que seja possível fazer o calculo com contains com NDCG também.
    resultado bom, porem DUVIDA abaixo

    mais testes com diferentes metodos de mostrar os filmes assistidos. 
    testes com fine tunning 

## duvidas
    analisando as diferenças entre os diferentes calculos 
    situações como essa são resolvidas 

        Candidate_set ['.....  'Shawshank Redemption',.....']

        GT: Shawshank Redemption

        Predição: 1. Lawrence of Arabia (War/Drama)
        2. Glory (War/Drama)
        3. Shawshank Redemption (Drama)  <<----------------------
        4. Patton (Biography/War)
        5. Unforgiven (Western/Drama)
        6. High Noon (Western/Drama)
        7. The Manchurian Candidate (Political Thriller)
        8. Seven (Crime/Mystery)
        9. Alien (Sci-Fi/Horror)
        10. Terminator 2: Judgment Day (Action/Sci-Fi).

        método 1: 0
        método 2:1
        método 3:1

    porem situações como essa começam a ocorrer

        Candidate_set ['.... 'Back to the Future',....]

        GT: Back to the Future

        Predição: 1. Die Hard: With a Vengeance
        2. Independence Day (ID4): Resurgence
        3. Star Wars: The Empire Strikes Back
        4. Speed
        5. Raiders of the Lost Ark
        6. Aliens
        7. Jurassic Park
        8. Terminator 2: Judgment Day
        9. Back to the Future Part II  <<----------------------
        10. Apollo 13

        método 1: 0
        método 2:1
        método 3:1


# orientação 28/04/2025 

## anotações importantes 
    
    considerar os primeiros itens do histórico, e justificar a escolha por causa dos resultados obtidos experimentando diferentes configurações. 


## oque fazer 

    verificar todos os itens da recomendação, se caso algum item recomendado 
    tentar mapear todos os casos de sufixos e prefixos que o llm gera a mais fora do nome dos filmes. 
    e fazer um contains da resposta dentro da lista de candidatos, caso tiver um filme que não esteja na lista de candidatos, desconsiderar a recomendação inteira (alucinação)
    manter a resposta atual, para comparar resultados e então calcular uma taxa de alucinação. 

    fazer um experimento com o modelo finetunado utilizando apenas o dataset de teste. guardar resultado para documentar. 

# Orientação 06/05/2025

## duvidas

    Mostrar o excel que fiz 

    falar sobre o experimento 8 (??)

    falar sobre o experimento com um unico prompt. 

    overleaf 

## oq fazer 

    no exp 2, anotar a quantidade média de filmes assitidos no total pelos usuários, para relatar e ter uma noção de volume. 
    agora com as configurações definidar, rodar os experimentos em todos os modelos antes de rodar os experimentos mais especificos. 
    merge entre os exp 3 e 5. 
    para experimentos especificos, utilizar o top 2 modelos encontrados. 

# Orientação 12/05/2025

## oq fazer 

    leitura geral do tcc2 entregue, antes de continuar a escrita do projeto 
    revisar anotações da banca do tcc2 ( enviado pelo professor e procurar outra tbm, provavelmente email)

    continuar os experimentos 

    fazer um experimento calculando o tamanho médio dos prompts que são utilizados durante o experimento 
    fazer um experimento para identificar o limite de tokens que o hardware disponível aguenta. 

    Adicionar ao texto o relato que foi testado o modelo llama 3.1 1b com uma quantização muito forte de q2, nao foi possível realizar o experimento com esse modelo, pois ele fazia respostas extremamente grandes (mais de 10k de tokens)

# Etapas finais

## anotações importantes
###
    considerar os primeiros itens do histórico, e justificar a escolha por causa dos resultados obtidos experimentando diferentes configurações. 
###
    esparcidade do dataset movielens
    https://www.d2l.ai/chapter_recommender-systems/movielens.html
###
    comentar sobre como alguns modelos são mais sensiveis a troca de prompts 

    experimentos para comparativo

        com realação a configuração: 
            1 - diferença entre prompts (entre os usados anteriormente)
            2 - quantidades de itens do histórico do usuário para o prompt
            (??) - ordem dos itens da lista de watched movies

        com relação aos modelos: (evidenciar uma taxa de alucinação)
            3 - diferença de versões de modelos (entre familias)
            4 - diferença de quantiazação (llama 3.2)
            5 - diferença de modelos (entre vencedores das familias acima)

        com relação ao dataset e finetunning: 
            6 - finetuning (definir modelo melhor com base nos exp de cima  "com" e "sem")
            7 - ml100k e ml1M (entre os usados anteriormente)


# Orientação 19/05/2025

## Oq Fazer 

    continuar os experimentos 

    [ok] fazer um experimento calculando o tamanho médio dos prompts que são utilizados durante o experimento 
    fazer um experimento para identificar o limite de tokens que o hardware disponível aguenta. 

    [ok] Adicionar ao texto o relato que foi testado o modelo llama 3.1 1b com uma quantização muito forte de q2, nao foi possível realizar o experimento com esse modelo, pois ele fazia respostas extremamente grandes (mais de 10k de tokens)

    relatar o teste com qwen 3 

    [ok] comentar no texto sobre a formatação dos prompts feitos pelo LM studio 

    tentar fazer um gráfico de barras empilhadas/layers para juntar o cenario 2 em um gráfico só. 


    tabelão: 
        Fazer um tabelão comparando o resultado com e sem alucinação 
            adicionar nessa comparação inicial os resultados do cenário 1. 
        fazer outro tabelão mostrando só o resultado sem alucinal~çao 


    [ok] arrumar gráfico cenarío 2 que está empilhando as métricasd 


# Orientação xx/05/2025

## duvidas

    chamar o cenário 2: sem alucinção de "cenário 3"??

    focar mais no detalhamento e analise do primeiro experimento. 

tabela 1 
ajustar a nomenclatura 
adicionar @5 
comentar bastante sobre o NDCG 


entre a tabela 1 e 2 
falar um pouco sobre a relação do HR e NDCG

tabelão 2 
talvez não usar o tabelão 2, caso desnecssário 
usar cenário 1 e cenário 2* apenas 
usar apenas HR

combinar gráfico de tempo de execução com alucinação. 

confirmar calculo do NDCG 
investigar pq o NDCG 5 nao altera para o 10 

informações repetidas, como diferença de resultado do HR5 pro HR10, nao precisam ser explicadas mais de 1 vez, caso nao houver nenhum comportamento diferente 


passar a explicação do recorte do dataset (cenários) para dentro da subceção dataset 
