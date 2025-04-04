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

fazer teste sem a filtragem colaborativa ( passando todos os filmes dentro do prompt )
implementar a função para executar as recomendações apenas para quem tem gt 
verificar as possibilidades do finetuning 

## oque foi feito 

Ajustado o pipeline para mandar para o LLM apenas quando existe o GT no candidate_set
ajustado os calculos de métricas para calcular os @5 e @10 de cada métrica
ajustado os logs no wandb / retirando o uso do wandb pois acabou o tempo free 