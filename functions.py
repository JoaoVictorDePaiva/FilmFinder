from langchain_google_genai import ChatGoogleGenerativeAI

try:
    llm = ChatGoogleGenerativeAI(
        google_api_key = "your_api_key",
    model = "gemini-1.5-flash-latest",
    temperature = 0.3,
    topk = 3,
    max_tokens = None
    )
    test_prompt = "Diga 'Olá, mundo!'"
    response = llm(test_prompt)
    if response:
        print("API key está funcionando corretamente.")
    else:
        print("Falha ao verificar a API key.")
except Exception as e:
    print(f"Erro ao verificar a API key: {e}")

from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain_core.runnables import RunnablePassthrough
from datetime import datetime
import requests
import gzip
import json

def movies(movie_name):
    
    first_prompt = PromptTemplate.from_template(
        "Forneça um resumo sucinto do enredo do filme '{movie}', incluindo o nome do diretor."
    )
   
    second_prompt = PromptTemplate.from_template(
        "Liste os gêneros do filme '{movie}', sem adicionar informações adicionais."
    )
    
    third_prompt = PromptTemplate.from_template(
        "Liste três filmes dirigidos pelo mesmo diretor de '{summary}', fornecendo o título, o nome do diretor e um breve resumo para cada."
    )

    fourth_prompt = PromptTemplate.from_template(
        "Liste três filmes do mesmo gênero predominante de '{movie}' ({genre}), fornecendo o título e um breve resumo para cada."
    )

    fifth_prompt = PromptTemplate.from_template(
    "Qual é o nome original do filme '{movie}'? Na resposta, fale apenas o nome original sem asteriscos e nenhuma informação adicional"
)
    
    
    first_chain = LLMChain(
        llm = llm,
        prompt = first_prompt,
        output_key = "summary"
    )
    
    
    second_chain = LLMChain(
        llm = llm,
        prompt = second_prompt,
        output_key = "genre"
    )
    
    
    third_chain = LLMChain(
        llm = llm,
        prompt = third_prompt,
        output_key = "director_movies"
    )
    
    
    fourth_chain = LLMChain(
        llm = llm,
        prompt = fourth_prompt,
        output_key = "similar_movies"
    )

    fifth_chain = LLMChain(
        llm = llm,
        prompt = fifth_prompt,
        output_key = "original_movie_name"
    )
    
    main_chain = SequentialChain(
        chains=[first_chain, second_chain, third_chain, fourth_chain, fifth_chain],
        input_variables=["movie"],
        output_variables=["summary", "genre", "director_movies", "similar_movies", "original_movie_name"],
        verbose=True
    )

    result = main_chain.invoke({"movie": movie_name})

    return result

def movie_id(movie_name):
    now = datetime.now()
    formatted_now = now.strftime("%m_%d_%Y")
    url = f"https://files.tmdb.org/p/exports/movie_ids_07_16_2024.json.gz"
    movie_name_wout_spaces = movie_name.rstrip()
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with gzip.open(response.raw, 'rt', encoding='utf-8') as gz_file:
                for line in gz_file:
                    try:
                        movie_data = json.loads(line.strip())
                        if movie_data.get('original_title') == movie_name_wout_spaces:
                            id_movie = movie_data['id']
                            return get_image(id_movie)
                    except json.JSONDecodeError as e:
                        print(f"Erro ao decodificar JSON na linha: {line}")
                        print(e)
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição HTTP: {e}")
    
    return None

def get_image(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key=428f9a194a4b2f874f76bdbfcc95683f"
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers, stream = True)
    
    if response.status_code == 200:
        data = response.json()
        posters = data.get("posters", [])
        
        for poster in posters:
            if poster.get("iso_639_1") == "en" or poster.get("iso_639_1") == "pt":
                original_poster = poster.get("file_path")
                print(original_poster)
                image = f"https://image.tmdb.org/t/p/w342{original_poster}"
                return image
        
        print("Nenhum poster encontrado com o idioma 'en'.")
        return None
    else:
        print("Erro ao fazer a solicitação:", response.status_code)
        return None