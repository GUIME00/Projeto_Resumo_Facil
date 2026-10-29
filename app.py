import re
import math
from collections import Counter

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer

st.set_page_config(
    page_title="Resumo Fácil | NLP",
    page_icon="📝",
    layout="wide",
)

# Lista compacta de palavras funcionais comuns em português.
# Remover essas palavras ajuda a destacar termos de conteúdo.
STOPWORDS_PT = {
    "a","à","às","agora","ainda","além","algo","algumas","alguns","ali","ampla",
    "amplas","amplo","amplos","ante","antes","ao","aos","apenas","apoio","após",
    "aquela","aquelas","aquele","aqueles","aquilo","as","assim","até","através",
    "cada","certa","certas","certo","certos","com","como","contra","contudo",
    "da","das","de","dela","delas","dele","deles","demais","depois","desde",
    "dessa","dessas","desse","desses","desta","destas","deste","destes","disso",
    "disto","do","dos","durante","e","ela","elas","ele","eles","em","embora",
    "entre","era","eram","essa","essas","esse","esses","esta","está","estão",
    "estas","estava","estavam","este","estes","eu","faz","fazer","foi","for",
    "foram","forma","fosse","fossem","grande","grandes","há","isso","isto","já",
    "lhe","lhes","mais","mas","me","mesma","mesmas","mesmo","mesmos","meu",
    "meus","minha","minhas","muita","muitas","muito","muitos","na","nada","nas",
    "nem","nenhum","nessa","nessas","nesse","nesses","nesta","nestas","neste",
    "nestes","no","nos","nós","nossa","nossas","nosso","nossos","num","numa",
    "nunca","o","os","ou","outra","outras","outro","outros","para","pela",
    "pelas","pelo","pelos","perante","pode","podem","poder","por","porque",
    "porém","posso","pouca","poucas","pouco","poucos","qual","quando","quanto",
    "quantos","que","quem","se","seja","sejam","sem","sempre","ser","será",
    "serão","seu","seus","si","sido","sob","sobre","sua","suas","tal","também",
    "tão","te","tem","têm","tendo","tenha","tenham","tenho","ter","teu","teus",
    "toda","todas","todo","todos","tu","tua","tuas","tudo","um","uma","umas",
    "uns","vai","vais","vão","vários","várias","vem","vêm","ver","vez","você",
    "vocês"
}

def dividir_frases(texto: str):
    """Divide o texto em frases usando pontuação final e quebras de linha."""
    texto = re.sub(r"\s+", " ", texto.strip())
    if not texto:
        return []
    partes = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÀÂÃÉÊÍÓÔÕÚÜÇ0-9“"(\'])', texto)
    frases = [p.strip() for p in partes if p.strip()]
    # Evita frases sem conteúdo útil, mas mantém frases curtas que podem ser importantes.
    return frases

def resumir_texto(texto: str, proporcao: float):
    frases = dividir_frases(texto)
    if len(frases) <= 1:
        return texto.strip(), frases, []

    # Tira apenas espaços extras para a vetorização; as frases originais são preservadas.
    try:
        vectorizer = TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            stop_words=list(STOPWORDS_PT),
            token_pattern=r"(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9_-]+\b"
        )
        matriz = vectorizer.fit_transform(frases)
        # Soma dos pesos TF-IDF por frase.
        scores = matriz.sum(axis=1).A1
    except ValueError:
        # Fallback para textos com apenas palavras muito curtas ou sem termos vetorizáveis.
        scores = [len(re.findall(r"\w+", frase)) for frase in frases]

    # Pequeno ajuste de posição: a primeira frase frequentemente apresenta o tema.
    n = len(frases)
    scores = [
        float(score) * (1.12 if i == 0 else 1.0)
        for i, score in enumerate(scores)
    ]

    quantidade = max(1, min(n - 1, math.ceil(n * proporcao)))
    indices = sorted(range(n), key=lambda i: scores[i], reverse=True)[:quantidade]
    indices_ordenados = sorted(indices)
    resumo = " ".join(frases[i] for i in indices_ordenados)
    return resumo, frases, scores

st.markdown("""
<style>
    .stApp { background: linear-gradient(145deg, #071326 0%, #0b1b31 100%); color: #edf4ff; }
    .block-container { max-width: 1250px; padding-top: 2rem; }
    .hero { padding: 0.5rem 0 1.2rem 0; border-bottom: 1px solid #233b5b; margin-bottom: 1.5rem; }
    .hero h1 { font-size: 2.5rem; margin-bottom: 0.2rem; }
    .hero p { color: #b9cbe5; font-size: 1.05rem; }
    div[data-testid="stTextArea"] textarea { background: #0b1a2d; color: #edf4ff; border: 1px solid #2b4568; border-radius: 12px; }
    div.stButton > button { background: #246bfa; color: white; border: 0; border-radius: 10px; font-weight: 700; min-height: 3rem; width: 100%; }
    div.stButton > button:hover { background: #1557d8; color: white; border: 0; }
    .panel { border: 1px solid #263f61; border-radius: 14px; padding: 1.2rem; background: rgba(10, 27, 47, .75); }
    .result { background: rgba(0, 130, 112, .12); border: 1px solid #087f70; border-radius: 12px; padding: 1.2rem; line-height: 1.75; font-size: 1.05rem; }
    .muted { color: #b9cbe5; }
    .small-note { font-size: .88rem; color: #b9cbe5; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>📝 Resumo <span style="color:#4c91ff">Fácil</span></h1>
  <p>Transforme textos longos em resumos objetivos com Processamento de Linguagem Natural.</p>
</div>
""", unsafe_allow_html=True)

exemplo = (
    "A inteligência artificial tem transformado diferentes áreas da sociedade, incluindo a educação. "
    "Ferramentas digitais podem adaptar atividades ao ritmo de cada estudante e oferecer feedback rápido. "
    "Professores também podem usar sistemas inteligentes para organizar materiais e identificar dificuldades de aprendizagem. "
    "Apesar dos benefícios, a tecnologia não substitui o papel dos educadores. "
    "É necessário garantir privacidade, acesso à infraestrutura e formação adequada para professores. "
    "O uso responsável dessas ferramentas pode ampliar oportunidades de aprendizagem, desde que exista acompanhamento humano."
)

col_input, col_result = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("1. Insira seu texto")
    st.caption("Cole um artigo, notícia, relatório, texto acadêmico ou outro conteúdo em português.")
    if "texto_usuario" not in st.session_state:
        st.session_state.texto_usuario = exemplo
    texto = st.text_area(
        "Texto original",
        key="texto_usuario",
        height=330,
        max_chars=50000,
        placeholder="Cole ou digite aqui o texto que deseja resumir..."
    )
    st.caption(f"{len(texto):,} caracteres")
    st.subheader("Opções do resumo")
    tamanho = st.radio(
        "Tamanho desejado",
        options=["Curto", "Médio", "Longo"],
        index=1,
        horizontal=True
    )
    proporcoes = {"Curto": 0.20, "Médio": 0.40, "Longo": 0.65}
    st.caption({"Curto": "Seleciona poucas frases essenciais.", "Médio": "Mantém uma seleção equilibrada de frases.", "Longo": "Preserva mais detalhes do texto original."}[tamanho])
    gerar = st.button("✨ Gerar resumo", use_container_width=True)

with col_result:
    st.subheader("2. Resumo gerado")
    if gerar:
        if not texto.strip():
            st.warning("Insira um texto antes de gerar o resumo.")
            st.session_state.pop("ultimo_resumo", None)
        elif len(texto.split()) < 20:
            st.warning("Para um resultado mais útil, insira um texto com pelo menos 20 palavras.")
            st.session_state.pop("ultimo_resumo", None)
        else:
            resumo, frases, scores = resumir_texto(texto, proporcoes[tamanho])
            st.session_state.ultimo_resumo = resumo
            st.session_state.texto_original_resumo = texto
            st.session_state.tamanho_resumo = tamanho

    if st.session_state.get("ultimo_resumo"):
        resumo = st.session_state.ultimo_resumo
        original = st.session_state.texto_original_resumo
        palavras_original = len(original.split())
        palavras_resumo = len(resumo.split())
        reducao = max(0, (1 - len(resumo) / max(1, len(original))) * 100)

        st.markdown(f'<div class="result">{resumo}</div>', unsafe_allow_html=True)
        st.write("")
        st.download_button(
            "⬇️ Baixar resumo (.txt)",
            data=resumo,
            file_name="resumo.txt",
            mime="text/plain",
            use_container_width=True
        )
        m1, m2, m3 = st.columns(3)
        m1.metric("Palavras originais", f"{palavras_original:,}")
        m2.metric("Palavras no resumo", f"{palavras_resumo:,}")
        m3.metric("Redução do texto", f"{reducao:.1f}%")
        st.caption(f"Tamanho escolhido: {st.session_state.get('tamanho_resumo', 'Médio')}")
    else:
        st.info("Seu resumo aparecerá aqui. Você pode testar com o texto de exemplo ou colar seu próprio conteúdo.")
        st.markdown("""
        **O que esta aplicação faz**
        - Analisa a importância das palavras com TF-IDF.
        - Seleciona as frases mais relevantes.
        - Mantém as frases na ordem original.
        - Permite baixar o resultado em arquivo `.txt`.
        """)

st.divider()
with st.expander("Como o NLP funciona nesta aplicação"):
    st.markdown("""
    1. **Segmentação:** divide o texto em frases.
    2. **Pré-processamento:** normaliza maiúsculas e acentos para análise.
    3. **TF-IDF:** atribui pesos a termos que ajudam a distinguir as frases.
    4. **Pontuação:** soma os pesos de cada frase e dá um pequeno destaque à primeira.
    5. **Seleção:** escolhe as frases com maiores pontuações e mantém a ordem original.

    Este é um **resumidor extrativo**. Ele não reescreve as frases e pode deixar de fora informações importantes; revise o resultado antes de usá-lo em contextos que exijam precisão.
    """)

st.markdown('<p class="small-note" style="text-align:center;margin-top:1.5rem">Resumo Fácil · Projeto prático de NLP com Python e scikit-learn</p>', unsafe_allow_html=True)
