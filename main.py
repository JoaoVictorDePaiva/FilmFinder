import functions
import streamlit as st

st.markdown(
    """
    <style>
    body {
        color: #ffffff !important
    }
    
    .main {
        background-color: #2e3346;
        padding: 20px;
        font-family: 'comic-sans', sans-serif;
    }
    
    .stTitle {
        color: #ffffff !important;
        font-size: 4em;
        text-align: center;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    
    .stTextInput input {
        color: #ffffff !important;
        background-color: #333333 !important;
    }
    
    .stButton button {
        background-color: #1b4854;
        color: white;
        padding: 5px 10px;
        border: solid 2px;
        border-radius: 15px;
        cursor: pointer;
    }
    
    .stButton button:hover {
        background-color: #1b4854;
    }
    
    .stMarkdown h3 {
        color: #ffffff;
        font-size: 1.5em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    .stTextInput > div {
        margin-top: -30px;
    }
    
    .stMarkdown p, .custom-text {
        color: #ffffff;
        font-size: 1.2em;
    }
    
    .centered-image {
        display: flex;
        justify-content: center;
    }
    
    .css-1cpxqw2 .stSpinner > div > div,
    .css-1n543e5 .stTextInput > div > div,
    .css-184tjsw p {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="stTitle">Filmfinder</h1>', unsafe_allow_html=True)

st.markdown('<p class="custom-text">Digite o nome de um filme que você gosta e nós recomendaremos outros baseados nele:</p>', unsafe_allow_html=True)
movie_name = st.text_input('')
if st.button('Gerar recomendações'):
    if movie_name:
        with st.spinner('Aguarde um instante...'):
            result = functions.movies(movie_name)
            image_movie = functions.movie_id(result["original_movie_name"])
            if image_movie:
                st.markdown(
                    f'<div class="centered-image"><img src="{image_movie}" style="max-width: 100%; height: auto;" alt="Poster do filme"></div>',
                    unsafe_allow_html=True
                )
            else:
                st.write("Imagem não disponível.")

            st.markdown(f'<h3>Resumo do filme {result["movie"]}</h3>', unsafe_allow_html=True)
            st.markdown(f'<p>{result["summary"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<h3>Gêneros do filme {result["movie"]}</h3>', unsafe_allow_html=True)
            st.markdown(f'<p>{result["genre"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<h3>Outros filmes do mesmo diretor:</h3>', unsafe_allow_html=True)
            st.markdown(f'<p>{result["director_movies"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<h3>Recomendações de outros filmes parecidos com {result["movie"]}</h3>', unsafe_allow_html=True)
            st.markdown(f'<p>{result["similar_movies"]}</p>', unsafe_allow_html=True)
    else:
        st.warning('Por favor, digite o nome do filme.')
