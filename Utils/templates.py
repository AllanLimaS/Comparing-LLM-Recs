

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

PROMPT_TEMPLATE_ESTRUCTURE = {

    "System_prompt": "You are a data extraction assistant. Your task is to extract only the movie titles from the provided text and return them in a structured format, separated by semicolons. Do not include any extra text, explanations, or numbers—only the movie titles.",

    "Prompt": """
    Rewrite the following list of recommendations, extracting only the movie titles and separating them with a semicolon.
    Original text:{}
    """

}