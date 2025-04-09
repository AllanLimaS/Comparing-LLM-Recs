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
    