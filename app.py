# =========================
# Sticker Reward System 🎖
# =========================
st.subheader("🎖 스티커 보상 시스템")

task_streak = calc_weekday_task_streak(st.session_state.history)

st.metric("요일 체크리스트 올클리어 연속 기록", f"{task_streak}일")

# 3일 단위로 스티커 지급
if task_streak >= 3 and task_streak % 3 == 0:
    sticker_name = f"🏅 올클리어 {task_streak}일 스티커"
    today_str = dt.date.today().isoformat()

    already_given = any(
        s.get("date") == today_str and s.get("name") == sticker_name
        for s in st.session_state.stickers
    )

    if not already_given:
        st.session_state.stickers.append({
            "date": today_str,
            "name": sticker_name,
            "streak": task_streak
        })
        st.balloons()
        st.success(f"🎉 축하합니다! {sticker_name} 획득!")

# 보유 스티커 표시
if st.session_state.stickers:
    st.write("### 🧸 내가 모은 스티커들")
    for s in reversed(st.session_state.stickers):
        st.write(f"- {s['date']} : {s['name']}")
else:
    st.info("아직 받은 스티커가 없어요. 3일 연속 올클리어하면 지급됩니다 😈")
