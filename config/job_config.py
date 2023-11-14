en_only_group = {
        "base_model": ['llama-2-7b-hf'],
        "data": ["sharegpt-clean_en", "platypus_en", "alpaca-gpt4_en"],
        "prompt": ["general_prompt_no_sys"]
        }

platypus_group = {
    "base_model": ["llama-2-7b-hf"],
    "data": [
          "platypus_en", 
    "platypus_en+platypus_es",
    "platypus_en+platypus_zh",
    "platypus_en+platypus_vi",
    "platypus_en+platypus_es+platypus_zh+platypus_vi"
    ],
    "prompt": ["general_prompt_no_sys"]
}

sharegpt_clean_group = {
    "base_model": ["llama-2-7b-hf"],
    "data": [
          "sharegpt-clean_en", 
    "sharegpt-clean_en+sharegpt-clean_es",
    "sharegpt-clean_en+sharegpt-clean_zh",
    "sharegpt-clean_en+sharegpt-clean_vi",
    "sharegpt-clean_en+sharegpt-clean_es+sharegpt-clean_zh+sharegpt-clean_vi"
    ],
    "prompt": ["general_prompt_no_sys"]
}

alpaca_gpt4_group = {
    "base_model": ["llama-2-7b-hf"],
    "data": [
    "alpaca-gpt4_en",
    "alpaca-gpt4_vi",
    "alpaca-gpt4_zh",
    "alpaca-gpt4_es", 
    "alpaca-gpt4_en+alpaca-gpt4_es",
    "alpaca-gpt4_en+alpaca-gpt4_zh",
    "alpaca-gpt4_en+alpaca-gpt4_vi",
    "alpaca-gpt4_en+alpaca-gpt4_es+alpaca-gpt4_zh+alpaca-gpt4_vi"
    ],
    "prompt": ["general_prompt_no_sys"]
}

platypus_single_lang_group = {
    "base_model": ["llama-2-7b-hf"],
    "data": [
          "platypus_en", 
    "platypus_es",
    "platypus_zh",
    "platypus_vi",
    ],
    "prompt": ["general_prompt_no_sys"]
}

platypus_multi_lang_group = {
    "base_model": ["llama-2-7b-hf"],
    "data": [
    "platypus_en+platypus_es",
    "platypus_en+platypus_zh",
    "platypus_en+platypus_vi",
    "platypus_en+platypus_es+platypus_zh+platypus_vi"
    ],
    "prompt": ["general_prompt_no_sys"]
}
