
def llama_3_2_3b_instruct_f16():
    return {
    "model_name" :"llama-3.2-3b-instruct-f16",
    "Arch" : "llama",
    "Quantization" : "F16",
    "Temperature": 0.0,
    "max_tokens" : -1,  # Default : 4096
    "GPU Offload": 22,
    "CPU Thread Pool Size": 6,
    "Evaluation Batch Size": 512,
    "Flash Attention": False, # não vi vantagem no uso 
    }


def llama_3_2_1b_instruct_f16():
    return {
    "model_name" :"llama-3.2-1b-instruct-f16",
    "Arch" : "llama",
    "Quantization" : "F16",
    "Temperature": 0.0,
    "max_tokens" : -1,  # Default : 4096
    "GPU Offload": 16,
    "CPU Thread Pool Size": 6,
    "Evaluation Batch Size": 512,
    "Flash Attention": False, # não vi vantagem no uso 
    }

def ministral_8b_instruct_2410():
    return{
    "model_name" :"ministral-8b-instruct-2410",
    "Arch" : "qwen2",
    "Quantization" : "Q4_K_M",
    "Temperature": 0.0,
    "max_tokens" : -1,  # Default : 4096
    "GPU Offload": 36,
    "CPU Thread Pool Size": 6,
    "Evaluation Batch Size": 512,
    "Flash Attention": False, # não vi vantagem no uso 
    }

def qwen_2_5_7b_instruct_1m():
    return{
    "model_name" :"qwen2.5-7b-instruct-1m",
    "Arch" : "qwen2",
    "Quantization" : "Q4_K_M",
    "Temperature": 0.0,
    "max_tokens" : -1,  # Default : 4096
    "GPU Offload": 28,
    "CPU Thread Pool Size": 6,
    "Evaluation Batch Size": 512,
    "Flash Attention": False, # não vi vantagem no uso 
    }

def phi_4():
    return{
    "model_name" :"phi-4",
    "Arch" : "phi3",
    "Quantization" : "Q4_K_M",
    "Temperature": 0.0,
    "max_tokens" : -1,  # Default : 4096
    "GPU Offload": 22,
    "CPU Thread Pool Size": 6,
    "Evaluation Batch Size": 512,
    "Flash Attention": False, # não vi vantagem no uso 
    }

def mistral_7b_instruct_v0_3():
    return{
    "model_name" :"mistral-7b-instruct-v0.3",
    "Arch" : "llama",
    "Quantization" : "Q4_K_M",
    "Temperature": 0.1,
    "max_tokens" : -1,  # Default : 4096
    "GPU Offload": 34,
    "CPU Thread Pool Size": 6,
    "Evaluation Batch Size": 512,
    "Flash Attention": False, # não vi vantagem no uso 
    }

def gemma_3_4b_it():
    return{
    "model_name" :"gemma-3-4b-it",
    "Arch" : "gemma3",
    "Quantization" : "Q4_K_M",
    "Temperature": 0.1,
    "max_tokens" : -1,  # Default : 4096
    "GPU Offload": 34,
    "CPU Thread Pool Size": 6,
    "Evaluation Batch Size": 512,
    "Flash Attention": False, # não vi vantagem no uso 
    }

def meta_llama_3_1_8b_instruct():
    return{
    "model_name" :"meta-llama-3.1-8b-instruct",
    "Arch" : "llama",
    "Quantization" : "Q4_K_M",
    "Temperature": 0.1,
    "max_tokens" : 4096,
    "GPU Offload": 34,
    "CPU Thread Pool Size": 6,
    "Evaluation Batch Size": 512,
    "Flash Attention": False,
    }

def gemma_3_4b_ft_allan():
    return{
    "model_name" :"gemma_3_4b_ft_allan",
    "Arch" : "llama",
    "Quantization" : "Q4_K_M",
    "Temperature": 0.1,
    "max_tokens" : 4096,
    "GPU Offload": 28,
    "CPU Thread Pool Size": 6,
    "Evaluation Batch Size": 512,
    "Flash Attention": False,
    }