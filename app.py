import streamlit as st

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(
    page_title="습관 트래커",
    page_icon="📊",
    layout="centered"
)

st.title("📊 습관 트래커")
st.subheader("당신의 습관 성향을 알아보는 간단한 테스트")

# ---------------------------
# 질문 데이터
# ---------------------------
questions = [
    {
        "question": "1. 새로운 습관을 시작할 때 당신은?",
        "options": [
            "계획을 철저히 세우고 시작한다",
            "일단 해보면서 조정한다",
            "생각만 하다가 미루는 편이다"
        ]
    },
    {
        "question": "2. 하루 일과를 기록하는 편인가요?",
        "options": [
            "매일 꼼꼼히 기록한다",
            "가끔 생각날 때만 한다",
            "거의 기록하지 않는다"
        ]
    },
    {
        "question": "3. 습관을 지키지 못했을 때 당신의 반응은?",
        "options": [
            "원인을 분석하고 다시 도전한다",
            "조금 자책하지만 다시 시도한다",
            "금방 포기해버린다"
        ]
    }
]

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

# ---------------------------
# 질문 화면
# ---------------------------
if st.session_state.current_q < len(questions):
    q = questions[st.session_state.current_q]

    st.progress((st.session_state.current_q + 1) / len(questions))
    st.markdown(f"### {q['question']}")

    answer = st.radio(
        "선택하세요:",
        q["options"],
        key=f"q_{st.session_state.current_q}"
    )

    col1, col2 = st.columns(2)

    with col2:
        if st.button("다음 ▶"):
            st.session_state.answers.append(answer)
            st.session_state.current_q += 1
            st.rerun()

# ---------------------------
# 결과 화면
# ---------------------------
else:
    st.success("🎉 테스트 완료!")

    st.markdown("### 📝 당신의 선택 요약")
    for i, ans in enumerate(st.session_state.answers):
        st.write(f"{i+1}. {ans}")

    st.markdown("---")
    st.markdown("### 💡 습관 성향 분석 (예시)")
    st.write(
        "당신은 자신의 행동을 인식하고 개선하려는 의지가 있는 타입입니다. "
        "작은 습관부터 꾸준히 기록해보세요!"
    )

    if st.button("🔄 다시 테스트하기"):
        st.session_state.current_q = 0
        st.session_state.answers = []
        st.rerun()
