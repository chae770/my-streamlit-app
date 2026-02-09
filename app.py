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
# 유틸: 2월 달력 생성 (현재 연도 기준)
# ----------------------
today = datetime.date.today()
year = today.year
month = 2  # 2월 고정

cal = calendar.Calendar(firstweekday=0)  # 월요일 시작(0=월)
month_days = list(cal.itermonthdates(year, month))

# 2월만 필터 + 주 단위(7개씩)로 자르기
only_month_days = [d for d in month_days if d.month == month]
weeks = [only_month_days[i:i+7] for i in range(0, len(only_month_days), 7)]

# ----------------------
# 세션 상태: 날짜별 기록 저장
# ----------------------
if "records" not in st.session_state:
    st.session_state.records = {}  # { "YYYY-MM-DD": {"text": "...", "done": bool} }

# ----------------------
# 사이드바
# ----------------------
with st.sidebar:
    st.header("설정")

    habit_category = st.selectbox("습관 카테고리", ["루틴", "학업", "운동", "기타"])

    empathy_style = st.radio(
        "AI 피드백 스타일",
        ["공감도 Max", "객관적인 단호박"]
    )

    st.divider()
    st.write("📌 2월 달력에서 날짜를 눌러 기록을 남겨보세요.")

# ----------------------
# 레이아웃
# ----------------------
left_col, right_col = st.columns([2.2, 1])

# ----------------------
# 왼쪽: 2월 달력(메인)
# ----------------------
with left_col:
    st.subheader(f"{year}년 2월 달력")

    # 요일 헤더
    header_cols = st.columns(7)
    for i, wd in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        header_cols[i].markdown(f"**{wd}**")

    # 달력 그리드
    selected_date = None

    for w in weeks:
        row_cols = st.columns(7)
        for i, d in enumerate(w):
            key = d.isoformat()
            has_record = key in st.session_state.records and st.session_state.records[key].get("text", "").strip() != ""
            done = st.session_state.records.get(key, {}).get("done", False)

            label = f"{d.day}"
            if has_record:
                label += " 📝"
            if done:
                label += " ✅"

            # 날짜 버튼
            if row_cols[i].button(label, key=f"btn_{key}"):
                selected_date = d

    st.divider()

    # 기본 선택 날짜: 오늘이 2월이면 오늘, 아니면 2월 1일
    if "selected_date" not in st.session_state:
        if today.month == 2:
            st.session_state.selected_date = today
        else:
            st.session_state.selected_date = datetime.date(year, 2, 1)

    # 버튼 클릭으로 선택된 날짜 반영
    if selected_date is not None:
        st.session_state.selected_date = selected_date

    sel = st.session_state.selected_date
    sel_key = sel.isoformat()

    # 선택 날짜 기록 UI
    st.markdown(f"### 📌 {sel.strftime('%Y-%m-%d')} 기록")

    # 불러오기
    existing_text = st.session_state.records.get(sel_key, {}).get("text", "")
    existing_done = st.session_state.records.get(sel_key, {}).get("done", False)

    text = st.text_area(
        "습관 기록",
        value=existing_text,
        placeholder="예: 아침 스트레칭 10분 / 영어 단어 30개",
        height=120
    )

    done = st.checkbox("오늘 기록 완료(체크)", value=existing_done)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("저장", use_container_width=True):
            st.session_state.records[sel_key] = {"text": text, "done": done, "category": habit_category}
            st.success("저장되었습니다! 🎉")

    with c2:
        if st.button("삭제", use_container_width=True):
            if sel_key in st.session_state.records:
                del st.session_state.records[sel_key]
            st.warning("삭제되었습니다.")

# ----------------------
# 오른쪽: AI 피드백 영역
# ----------------------
with right_col:
    st.subheader("AI 피드백")

    sel = st.session_state.selected_date
    sel_key = sel.isoformat()
    record = st.session_state.records.get(sel_key, {})
    record_text = record.get("text", "").strip()
    record_done = record.get("done", False)
    record_cat = record.get("category", habit_category)

    st.markdown(f"**선택 날짜:** {sel.strftime('%Y-%m-%d')}")
    st.markdown(f"**카테고리:** {record_cat}")
    st.markdown(f"**스타일:** {empathy_style}")
    st.divider()

    if record_text == "":
        st.info("아직 이 날짜에 기록이 없어요. 왼쪽에서 날짜별 기록을 작성해 주세요.")
    else:
        st.markdown("**기록 내용**")
        st.write(record_text)
        st.markdown(f"**완료 체크:** {'✅ 완료' if record_done else '⬜ 미완료'}")

        if st.button("피드백 열람", use_container_width=True):
            # 현재는 UI 프로토타입용 더미 피드백
            if empathy_style == "공감도 Max":
                msg = (
                    "정말 잘하고 있어요! 🌿\n\n"
                    "오늘 기록을 남긴 것 자체가 큰 성취예요.\n"
                    "완료 여부와 상관없이, 꾸준히 돌아오는 습관이 당신을 변화시켜요. "
                    "내일도 부담 없이 한 걸음만 같이 가볼까요?"
                )
            else:  # 객관적인 단호박
                msg = (
                    "기록은 했고, 이제 실행만 남았어요.\n\n"
                    "완료 체크가 비어 있다면 ‘했다’고 말할 근거가 없습니다.\n"
                    "내일은 목표를 더 작게 쪼개서 **반드시 체크**로 끝내세요."
                )

            st.success("AI 피드백(샘플)")
            st.write(msg)

# ----------------------
# 하단: 간단 요약
# ----------------------
st.divider()

total_days = calendar.monthrange(year, month)[1]
done_count = sum(1 for v in st.session_state.records.values() if v.get("done"))
record_count = sum(1 for v in st.session_state.records.values() if v.get("text", "").strip() != "")

st.caption(
    f"2월 기록 현황: 총 {total_days}일 중 기록 {record_count}일 / 완료 {done_count}일"
)
