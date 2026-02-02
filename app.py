import streamlit as st
from datetime import date

st.set_page_config(page_title="AI 코칭노트")
st.title("🏋️ AI 코칭노트")
st.caption("훈련·컨디션 기록 및 AI 피드백")

# 세션 상태
if "players" not in st.session_state:
    st.session_state.players = []
if "log" not in st.session_state:
    st.session_state.log = None

# 선수 등록
st.sidebar.subheader("👤 선수 등록")
name = st.sidebar.text_input("이름")
condition = st.sidebar.selectbox("컨디션", ["좋음", "보통", "주의"])
if st.sidebar.button("추가") and name:
    st.session_state.players.append((name, condition))

# 훈련 기록
st.subheader("📋 훈련 기록")
training = st.text_area("오늘 훈련 내용")
intensity = st.selectbox("훈련 강도", ["낮음", "중간", "높음"])

if st.button("저장"):
    st.session_state.log = {
        "date": date.today(),
        "training": training,
        "intensity": intensity
    }
    st.success("훈련 기록 저장 완료!")

# AI 피드백 (Mock)
if st.session_state.log:
    st.subheader("🤖 AI 훈련 요약")
    players = ", ".join([f"{n}({c})" for n, c in st.session_state.players])

    st.markdown(f"""
**훈련 요약**
- 강도: {st.session_state.log['intensity']}
- 내용: {st.session_state.log['training']}

**선수 컨디션**
- {players if players else "선수 정보 없음"}

**보호자 공유용**
오늘은 선수 컨디션을 고려한 훈련을 진행했습니다.
""")
