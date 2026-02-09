import streamlit as st
import datetime
import calendar
from openai import OpenAI

# ----------------------
# 기본 설정
# ----------------------
st.set_page_config(page_title="습관 트래커", page_icon="📅", layout="wide")

st.title("습관 트래커")
st.caption("2월 달력에서 날짜별로 습관을 기록하고 AI 피드백을 받아보세요.")

# ----------------------
# 날짜 / 달력 설정
# ----------------------
today = datetime.date.today()
year = today.year
month = 2  # 2월 고정

cal = calendar.Calendar(firstweekday=6)  # Sunday 시작
month_days = list(cal.itermonthdates(year, month))
weeks = [month_days[i:i + 7] for i in range(0, len(month_days), 7)]

# ----------------------
# 세션 상태
# ----------------------
if "records" not in st.session_state:
    st.session_state.records = {}

if "selected_date" not in st.session_state:
    st.session_state.selected_date = (
        today if today.month == 2 else datetime.date(year, 2, 1)
    )

# ----------------------
# 사이드바
# ----------------------
with st.sidebar:
    st.header("🔧 설정")

    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-..."
    )

    habit_category = st.selectbox(
        "습관 카테고리", ["루틴", "학업", "운동", "기타"]
    )

    empathy_style = st.radio(
        "AI 피드백 스타일",
        ["공감도 Max", "객관적인 단호박"]
    )

    st.divider()
    st.caption("🔑 API Key는 로컬에서만 사용됩니다.")

# ----------------------
# 메인 레이아웃
# ----------------------
left_col, right_col = st.columns([2.2, 1])

# ----------------------
# 왼쪽: 달력
# ----------------------
with left_col:
    st.subheader(f"{year}년 2월")

    headers = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    cols = st.columns(7)
    for i, h in enumerate(headers):
        cols[i].markdown(f"**{h}**")

    selected_date = None

    for week in weeks:
        row = st.columns(7)
        for i, day in enumerate(week):
            if day.month != month:
                row[i].markdown(" ")
                continue

            key = day.isoformat()
            record = st.session_state.records.get(key, {})
            label = str(day.day)

            if record.get("text"):
                label += " 📝"
            if record.get("done"):
                label += " ✅"

            if row[i].button(label, key=f"btn_{key}"):
                selected_date = day

    if selected_date:
        st.session_state.selected_date = selected_date

    st.divider()

    sel = st.session_state.selected_date
    sel_key = sel.isoformat()
    existing = st.session_state.records.get(sel_key, {})

    st.markdown(f"### 📌 {sel.strftime('%Y-%m-%d')} 기록")

    text = st.text_area(
        "습관 기록",
        value=existing.get("text", ""),
        placeholder="예: 스트레칭 10분, 영어 단어 30개",
        height=120
    )

    done = st.checkbox(
        "오늘 기록 완료",
        value=existing.get("done", False)
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("저장", use_container_width=True):
            st.session_state.records[sel_key] = {
                "text": text,
                "done": done,
                "category": habit_category
            }
            st.success("저장되었습니다!")

    with c2:
        if st.button("삭제", use_container_width=True):
            st.session_state.records.pop(sel_key, None)
            st.warning("삭제되었습니다.")

# ----------------------
# 오른쪽: AI 피드백
# ----------------------
with right_col:
    st.subheader("🤖 AI 피드백")

    sel = st.session_state.selected_date
    sel_key = sel.isoformat()
    record = st.session_state.records.get(sel_key, {})

    st.markdown(f"**날짜:** {sel.strftime('%Y-%m-%d')}")
    st.markdown(f"**카테고리:** {record.get('category', habit_category)}")
    st.markdown(f"**스타일:** {empathy_style}")
    st.divider()

    if not record.get("text"):
        st.info("이 날짜에는 아직 기록이 없어요.")
    elif not api_key:
        st.warning("사이드바에 OpenAI API Key를 입력해주세요.")
    else:
        if st.button("피드백 생성", use_container_width=True):
            with st.spinner("AI 코치가 피드백을 작성 중입니다..."):
                try:
                    client = OpenAI(api_key=api_key)

                    system_prompt = (
                        "당신은 습관 트래커 앱의 AI 코치입니다. "
                        "사용자의 습관 기록에 대해 피드백을 제공합니다."
                    )

                    style_prompt = (
                        "공감과 위로를 최우선으로 하세요."
                        if empathy_style == "공감도 Max"
                        else "감정은 배제하고 객관적이며 단호하게 피드백하세요."
                    )

                    user_prompt = f"""
                    날짜: {sel}
                    카테고리: {record.get('category')}
                    습관 기록: {record.get('text')}
                    완료 여부: {"완료" if record.get("done") else "미완료"}

                    피드백 스타일: {style_prompt}
                    """

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                        temperature=0.8
                    )

                    st.success("AI 피드백")
                    st.write(response.choices[0].message.content)

                except Exception as e:
                    st.error(f"에러 발생: {e}")

# ----------------------
# 하단 요약
# ----------------------
st.divider()

total_days = calendar.monthrange(year, month)[1]
record_count = sum(1 for v in st.session_state.records.values() if v.get("text"))
done_count = sum(1 for v in st.session_state.records.values() if v.get("done"))

st.caption(
    f"📊 2월 기록 현황 — 기록 {record_count}일 / 완료 {done_count}일 (총 {total_days}일)"
)
