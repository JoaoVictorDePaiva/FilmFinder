from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    google_api_key = "",
    model = "gemini-1.5-flash-latest",
    temperature = 0.3,
    topk = 3,
    max_tokens = None
)

from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain_core.runnables import RunnablePassthrough

def movies(movie_name):

    first_prompt = PromptTemplate.from_template(
        "Faça um resumo curto do filme: {movie} "
    )
   
    second_prompt = PromptTemplate.from_template(
        "Cite quais são os gêneros do filme {movie}. Fale apenas quais são so gêneros, sem informações adicionais"
    )
    third_prompt = PromptTemplate.from_template(
        "Cite outros 3 filmes do mesmo diretor do filme{movie}. Cite apenas os nomes dos filmes e o nome do diretor. Faça um breve resumo desses   filmes"
    )

    fourth_prompt = PromptTemplate.from_template(
        "Cite outros 3 filmes do mesmo genêro {genre} predominante  do filme:{movie}. Faça um breve resumo desses filmes" 
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
    
    main_chain = SequentialChain(
        chains=[first_chain, second_chain, third_chain, fourth_chain],
        input_variables=["movie"],
        output_variables=["summary", "genre", "director_movies", "similar_movies"],
        verbose=True
    )

    result = main_chain.invoke({"movie": movie_name})


    return result