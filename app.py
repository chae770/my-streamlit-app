import streamlit as st
import datetime
import calendar

# ----------------------
# 기본 설정
# ----------------------
st.set_page_config(page_title="습관 트래커", page_icon="📅", layout="wide")

st.title("습관 트래커")
st.caption("2월 달력에서 날짜별로 습관을 기록하고 피드백을 받아보세요.")

# ----------------------
# 유틸: 2월 달력 생성 (Sunday 시작)
# ----------------------
today = datetime.date.today()
year = today.year
month = 2  # 2월 고정

cal = calendar.Calendar(firstweekday=6)  # 🔥 Sunday 시작
month_days = list(cal.itermonthdates(year, month))

# 주 단위로 자르기 (7일씩)
weeks = [month_days[i:i + 7] for i in range(0, len(month_days), 7)]

# ----------------------
# 세션 상태: 날짜별 기록 저장
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
    st.header("설정")

    habit_category = st.selectbox(
        "습관 카테고리", ["루틴", "학업", "운동", "기타"]
    )

    empathy_style = st.radio(
        "AI 피드백 스타일",
        ["공감도 Max", "객관적인 단호박"]
    )

    st.divider()
    st.info("📅 2월 달력에서 날짜를 클릭해 습관을 기록하세요.")

# ----------------------
# 메인 레이아웃
# ----------------------
left_col, right_col = st.columns([2.2, 1])

# ----------------------
# 왼쪽: 2월 달력 (Sunday → Saturday)
# ----------------------
with left_col:
    st.subheader(f"{year}년 2월")

    # 요일 헤더
    headers = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    header_cols = st.columns(7)
    for i, h in enumerate(headers):
        header_cols[i].markdown(f"**{h}**")

    selected_date = None

    # 달력 그리드
    for week in weeks:
        row_cols = st.columns(7)
        for i, day in enumerate(week):
            if day.month != month:
                row_cols[i].markdown(" ")
                continue

            key = day.isoformat()
            record = st.session_state.records.get(key, {})
            has_text = record.get("text", "").strip() != ""
            done = record.get("done", False)

            label = f"{day.day}"
            if has_text:
                label += " 📝"
            if done:
                label += " ✅"

            if row_cols[i].button(label, key=f"btn_{key}"):
                selected_date = day

    if selected_date:
        st.session_state.selected_date = selected_date

    st.divider()

    sel = st.session_state.selected_date
    sel_key = sel.isoformat()

    st.markdown(f"### 📌 {sel.strftime('%Y-%m-%d')} 기록")

    existing = st.session_state.records.get(sel_key, {})
    text = st.text_area(
        "습관 기록",
        value=existing.get("text", ""),
        placeholder="예: 영어 단어 30개 / 스트레칭 10분",
        height=120
    )

    done = st.checkbox("오늘 기록 완료", value=existing.get("done", False))

    c1, c2 = st.columns(2)
    with c1:
        if st.button("저장", use_container_width=True):
            st.session_state.records[sel_key] = {
                "text": text,
                "done": done,
                "category": habit_category
            }
            st.success("저장되었습니다! 🎉")

    with c2:
        if st.button("삭제", use_container_width=True):
            st.session_state.records.pop(sel_key, None)
            st.warning("삭제되었습니다.")

# ----------------------
# 오른쪽: AI 피드백
# ----------------------
with right_col:
    st.subheader("AI 피드백")

    sel = st.session_state.selected_date
    sel_key = sel.isoformat()
    record = st.session_state.records.get(sel_key, {})

    st.markdown(f"**날짜:** {sel.strftime('%Y-%m-%d')}")
    st.markdown(f"**카테고리:** {record.get('category', habit_category)}")
    st.markdown(f"**스타일:** {empathy_style}")
    st.divider()

    if record.get("text", "").strip() == "":
        st.info("이 날짜에는 아직 기록이 없어요.")
    else:
        st.markdown("**기록 내용**")
        st.write(record.get("text"))
        st.markdown(
            f"**완료 여부:** {'✅ 완료' if record.get('done') else '⬜ 미완료'}"
        )

        if st.button("피드백 열람", use_container_width=True):
            if empathy_style == "공감도 Max":
                feedback = (
                    "오늘도 스스로를 챙기려는 선택을 했다는 점이 정말 멋져요 🌱\n\n"
                    "완벽하지 않아도 괜찮아요. 기록을 남겼다는 사실 자체가 이미 성장입니다."
                )
            else:
                feedback = (
                    "기록은 했습니다.\n\n"
                    "하지만 완료 체크가 없다면 실행으로 보지 않습니다.\n"
                    "내일은 목표를 더 작게 설정하고 반드시 완료하세요."
                )

            st.success("AI 피드백 (샘플)")
            st.write(feedback)

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
