import streamlit as st
import requests
# 사이드바에서 API 키 입력
TMDB_API_KEY = st.sidebar.text_input("TMDB API Key", type="password")
import streamlit as st
import datetime

# ----------------------
# 기본 설정
# ----------------------
st.set_page_config(
    page_title="습관 트래커",
    page_icon="📅",
    layout="wide"
)

# ----------------------
# 제목
# ----------------------
st.title("습관 트래커")
st.caption("나의 습관을 기록하고 꾸준함을 시각화해보세요")

# ----------------------
# 사이드바
# ----------------------
with st.sidebar:
    st.header("설정")

    habit_category = st.selectbox(
        "습관 카테고리",
        ["루틴", "학업", "운동", "기타"]
    )

    empathy_style = st.radio(
        "AI 피드백 스타일",
        ["공감도 MAX", "냉정하고 단호한 스타일"]
    )

    st.divider()
    st.info("오늘의 습관을 기록한 후\n피드백을 받아보세요.")

# ----------------------
# 메인 레이아웃
# ----------------------
left_col, right_col = st.columns([2, 1])

# ----------------------
# 왼쪽: 주간 습관 체크
# ----------------------
with left_col:
    st.subheader("이번 주 습관 체크")

    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())

    checked_days = {}

    cols = st.columns(7)
    for i in range(7):
        day = start_of_week + datetime.timedelta(days=i)
        with cols[i]:
            st.markdown(f"**{day.strftime('%a')}**")
            checked_days[day] = st.checkbox(
                day.strftime("%m/%d"),
                key=str(day)
            )

    st.divider()

    habit_text = st.text_input(
        "오늘의 습관 기록",
        placeholder="예: 아침 스트레칭 10분"
    )

    if st.button("기록 완료"):
        if habit_text.strip() == "":
            st.warning("습관 내용을 입력해주세요.")
        else:
            st.success("습관 기록이 저장되었습니다! 🎉")

# ----------------------
# 오른쪽: AI 피드백 영역
# ----------------------
with right_col:
    st.subheader("AI 피드백")

    st.markdown(
        """
        💬 **피드백 예시**
        - 이번 주에 꾸준히 실천하고 있어요!
        - 하루라도 기록한 점이 정말 중요해요.
        """
    )

    if st.button("피드백 열람"):
        st.info(
            f"""
            선택한 스타일: **{empathy_style}**  
            카테고리: **{habit_category}**

            👉 여기에 AI 코치 피드백이 표시됩니다.
            """
        )

# ----------------------
# 하단
# ----------------------
st.divider()
st.caption("© 2026 Habit Tracker Prototype")
