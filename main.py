import functions
import streamlit as st

st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        font-family: 'Arial', sans-serif;
    }
    .stTitle {
        color: #333333;
        font-size: 2em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .stTextInput {
        margin-bottom: 20px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stMarkdown h3 {
        color: #333333;
        font-size: 1.5em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .stMarkdown p {
        color: #666666;
        font-size: 1.2em;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Recomendações de Filmes')

movie_name = st.text_input('Digite o nome de um filme que você gosta e nós recomendaremos outros baseados nele:')
if st.button('Gerar recomendações'):
    if movie_name:
        with st.spinner('Aguarde um instante'):
            result = functions.movies(movie_name)
            st.title(f'Resumo do filme {result['movie']}:\n')
            st.text(f'{result['summary']}\n')
            st.title(f'Generos do filme {result['movie']}:\n')
            st.text(f'{result['genre']}\n')
            st.title(f'Outros filmes do mesmo diretor:')
            st.text(f'{result['director_movies']}\n')
            st.title(f'Recomendações de outros filmes parecidos com {result['movie']}:\n')
            st.text(f'{result['similar_movies']}\n')
    else:
        st.warning('Por favor, digite o nome do filme.')