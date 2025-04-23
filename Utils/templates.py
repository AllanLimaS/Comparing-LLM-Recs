
PROMPT_TEMPLATE_ESTRUCTURE = {

    "System_prompt": "You are a data extraction assistant. Your task is to extract only the movie titles from the provided text and return them in a structured format, separated by semicolons. Do not include any extra text, explanations, or numbers—only the movie titles.",

    "Prompt": """
    Rewrite the following list of recommendations, extracting only the movie titles and separating them with a semicolon.
    Original text:{}
    """

}

PROMPT_TEMPLATE_1 = {
    "System_prompt": "You are a movie expert provide the answer for the question based on the given context. If you don't know the answer to a question, please don't share false information.",

    "Preference": """
    ### MY WATCHED MOVIES LIST: {}.

    ### QUESTION: Based on my watched movies list. Tell me what features are most important to me when selecting movies (Summarize my preferences briefly)?

    ### ANSWER:
    """,

    "Featured_movies": """

    ### MY WATCHED MOVIES LIST: {}.

    ### MY MOVIE PREFERENCES: {}.

    ### QUESTION: Create an enumerated list selecting the five most featured movies from the watched movies according to my movie preferences.

    ### ANSWER:
    """,

    "Recommendation": """

    ### CANDIDATE MOVIE SET: {}.

    ### MY WATCHED MOVIES LIST: {}.

    ### MY MOVIE PREFERENCES: {}.

    ### MY FIVE MOST FEATURED MOVIES: {}.

    ### QUESTION: Can you recommend 10 movies from the "Candidate movie set" similar to the "Five most featured movies" I've watched (use format "Recommended movie" # "Similar movie")?

    ### ANSWER:
    """

}



PROMPT_TEMPLATE_2 = {
    "System_prompt": "You are a movie expert provide the answer for the question based on the given context. If you don't know the answer to a question, please don't share false information.",

    "Preference": """
    ### MY WATCHED MOVIES LIST: {}.

    ### QUESTION: Based on my watched movies list. Tell me what features are most important to me when selecting movies (Summarize my preferences briefly)?

    ### ANSWER:
    """,

    "Featured_movies": """

    ### MY WATCHED MOVIES LIST: {}.

    ### MY MOVIE PREFERENCES: {}.

    ### QUESTION: Create an enumerated list selecting the five most featured movies from the watched movies according to my movie preferences.

    ### ANSWER:
    """,

    "Recommendation": """

    ### CANDIDATE MOVIE SET: {}.

    ### MY WATCHED MOVIES LIST: {}.

    ### MY MOVIE PREFERENCES: {}.

    ### MY FIVE MOST FEATURED MOVIES: {}.

    ### INSTRUCTIONS:
    Recommend exactly **10 movies** from the "Candidate Movie Set" that are most similar to my "Five Most Featured Movies".  
    The output must be **STRICTLY formatted** as follows:

    1. Movie Title  
    2. Movie Title  
    3. Movie Title  
    4. Movie Title  
    5. Movie Title  
    6. Movie Title  
    7. Movie Title  
    8. Movie Title  
    9. Movie Title  
    10. Movie Title  

    Do not include any extra text before or after the list 
    
    ### QUESTION:  
    What are your top 10 movie recommendations?  

    ### ANSWER:
"""
}

PROMPT_TEMPLATE_3 = {
    "System_prompt": "You are a movie expert provide the answer for the question based on the given context. If you don't know the answer to a question, please don't share false information.",

    "Preference": """
    ### MY RECENTLY WATCHED MOVIES (FROM OLDEST TO NEWEST): {}.

    ### QUESTION: Based on my watched movies list. Tell me what features are most important to me when selecting movies (Summarize my preferences briefly)?

    ### ANSWER:
    """,

    "Featured_movies": """

    ### MY RECENTLY WATCHED MOVIES (FROM OLDEST TO NEWEST): {}.

    ### MY MOVIE PREFERENCES: {}.

    ### QUESTION: Create an enumerated list selecting the five most featured movies from the watched movies according to my movie preferences.

    ### ANSWER:
    """,

    "Recommendation": """

    ### CANDIDATE MOVIE SET: {}.

    ### MY RECENTLY WATCHED MOVIES (FROM OLDEST TO NEWEST): {}.

    ### MY MOVIE PREFERENCES: {}.

    ### MY FIVE MOST FEATURED MOVIES: {}.

    ### INSTRUCTIONS:
    Recommend exactly **10 movies** from the "Candidate Movie Set" that are most similar to my "Five Most Featured Movies".  
    The output must be **STRICTLY formatted** as follows:

    1. Movie Title  
    2. Movie Title  
    3. Movie Title  
    4. Movie Title  
    5. Movie Title  
    6. Movie Title  
    7. Movie Title  
    8. Movie Title  
    9. Movie Title  
    10. Movie Title  

    Do not include any extra text before or after the list 
    
    ### QUESTION:  
    What are your top 10 movie recommendations?  

    ### ANSWER:
"""
}

TRAIN_TEMPLATE = {
    "INPUT": """

    ### CANDIDATE MOVIE SET: {}.

    ### MY WATCHED MOVIES LIST: {}.

    ### MY MOVIE PREFERENCES: {}.

    ### MY FIVE MOST FEATURED MOVIES: {}.

    ### INSTRUCTIONS:
    Recommend exactly **1 movie** from the "Candidate Movie Set" that are most similar to my "Five Most Featured Movies".
    The output must be **STRICTLY formatted** as follows:

    1. Movie Title

    Do not include any extra text before or after the list

    ### QUESTION:
    What are your top 1 movie recommendations?

    ### ANSWER:
""",

    "OUTPUT": 
    """ 1.{} """
}

TRAIN_TEMPLATE_2 = {
    "INPUT": """

    ### CANDIDATE MOVIE SET: {}.

    ### MY RECENTLY WATCHED MOVIES (FROM OLDEST TO NEWEST): {}.

    ### MY MOVIE PREFERENCES: {}.

    ### MY FIVE MOST FEATURED MOVIES: {}.

    ### INSTRUCTIONS:
    Recommend exactly **1 movie** from the "Candidate Movie Set" that are most similar to my "Five Most Featured Movies".
    The output must be **STRICTLY formatted** as follows:

    1. Movie Title

    Do not include any extra text before or after the list

    ### QUESTION:
    What are your top 1 movie recommendations?

    ### ANSWER:
""",

    "OUTPUT": 
    """ 1.{} """
}