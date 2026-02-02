import streamlit as st
import requests

st.set_page_config(
    page_title="나와 어울리는 영화는?",
    page_icon="🎬",
    layout="wide"
)

POSTER_URL = "https://image.tmdb.org/t/p/w500"

GENRE_IDS = {
    "로맨스": 10749,
    "드라마": 18,
    "액션": 28,
    "코미디": 35,
    "SF": 878,
    "판타지": 14
}

# -------------------- SIDEBAR --------------------
st.sidebar.markdown("## 🔑 API 설정")
API_KEY = st.sidebar.text_input("TMDB API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.markdown("## 🎛️ 관람 조건")

runtime_option = st.sidebar.radio(
    "⏱️ 영화 길이",
    ["상관없음", "2시간 이내", "2~3시간", "3시간 이상"]
)

with_who = st.sidebar.radio(
    "👥 함께 보는 사람",
    ["혼자", "연인", "친구", "부모님"]
)

# -------------------- HERO --------------------
st.markdown("""
<div style="
background: linear-gradient(135deg, #1f1c2c, #928dab);
padding: 40px;
border-radius: 20px;
color: white;
text-align: center;
">
<h1>🎬 나와 어울리는 영화는?</h1>
<p style="font-size:18px;">
MBTI 감성 심리테스트로<br>
지금 상황에 딱 맞는 영화를 추천해드려요 🍿
</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------- QUESTIONS --------------------
st.markdown("## 🧠 성향 분석 테스트")

questions = [
    ("여행 스타일은?", {
        "사람들과 시끌벅적": ["액션", "코미디"],
        "혼자 조용히 힐링": ["로맨스", "드라마"]
    }),
    ("더 끌리는 영화는?", {
        "현실 공감 스토리": ["드라마"],
        "상상력 가득한 세계관": ["SF", "판타지"]
    }),
    ("영화에서 중요한 건?", {
        "메시지와 주제": ["SF", "액션"],
        "감정과 관계": ["로맨스", "드라마"]
    }),
    ("영화 고르는 스타일은?", {
        "계획적으로": ["드라마"],
        "즉흥적으로": ["코미디", "판타지"]
    }),
    ("스트레스 받을 때?", {
        "감동": ["로맨스"],
        "웃음": ["코미디"],
        "몰입": ["SF"],
        "짜릿함": ["액션"]
    })
]

genre_score = {g: 0 for g in GENRE_IDS}

for i, (q, opts) in enumerate(questions):
    choice = st.radio(f"Q{i+1}. {q}", list(opts.keys()), key=i)
    for g in opts[choice]:
        genre_score[g] += 2

# -------------------- 함께 보는 사람 보정 --------------------
if with_who == "혼자":
    genre_score["SF"] += 2
    genre_score["드라마"] += 1
elif with_who == "연인":
    genre_score["로맨스"] += 3
    genre_score["드라마"] += 2
elif with_who == "친구":
    genre_score["액션"] += 3
    genre_score["코미디"] += 3
elif with_who == "부모님":
    genre_score["드라마"] += 3
    genre_score["코미디"] += 1

# -------------------- RESULT --------------------
st.markdown("---")

if st.button("🎯 결과 보기"):
    if not API_KEY:
        st.warning("사이드바에 TMDB API Key를 입력해주세요.")
        st.stop()

    top_genre = max(genre_score, key=genre_score.get)

    st.markdown(f"""
    <div style="
    background-color:#f5f0ff;
    padding:20px;
    border-radius:15px;
    text-align:center;
    font-size:22px;
    ">
    ✨ 당신에게 어울리는 장르는 <b>{top_genre}</b> 입니다!
    </div>
    """, unsafe_allow_html=True)

    genre_id = GENRE_IDS[top_genre]

    runtime_query = ""
    if runtime_option == "2시간 이내":
        runtime_query = "&with_runtime.lte=120"
    elif runtime_option == "2~3시간":
        runtime_query = "&with_runtime.gte=120&with_runtime.lte=180"
    elif runtime_option == "3시간 이상":
        runtime_query = "&with_runtime.gte=180"

    url = (
        f"https://api.themoviedb.org/3/discover/movie"
        f"?api_key={API_KEY}&language=ko-KR"
        f"&with_genres={genre_id}"
        f"&sort_by=popularity.desc"
        f"{runtime_query}"
    )

    data = requests.get(url).json()

    st.markdown("## 🍿 추천 영화 TOP 5")

    for movie in data["results"][:5]:
        col1, col2 = st.columns([1.2, 3.8])

        with col1:
            if movie["poster_path"]:
                st.image(POSTER_URL + movie["poster_path"], use_container_width=True)

        with col2:
            st.markdown(f"### 🎬 {movie['title']}")
            st.markdown(f"⭐ **{movie['vote_average']} / 10**")
            st.markdown(f"📅 개봉일: {movie['release_date']}")
            st.write(movie["overview"][:180] + "...")
            st.success(
                f"이 영화는 **{with_who}와(과) 보기 좋고**, "
                f"당신의 **{top_genre} 성향**과 잘 맞아요!"
            )
