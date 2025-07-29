import streamlit as st
import time

st.set_page_config(
    page_title='타이머',
    page_icon='⏱️',
    layout='centered'
)

# st.title('⏱️타이머')
# st.caption('작업 리듬을 만들어주는 음악 타이머')

st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 style="font-size: 3rem; font-weight: bold;">⏱️타이머</h1>
        <p style="color: #888; font-size: 0.8rem;">작업 리듬을 만들어주는 음악 타이머</p>
    </div>
    """, unsafe_allow_html=True)

# 세션 스테이트 초기화
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'timer_paused' not in st.session_state:
    st.session_state.timer_paused = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'pause_start_time' not in st.session_state:  # 수정: 일시정지 시작 시간 추가
    st.session_state.pause_start_time = None
if 'total_pause_time' not in st.session_state:  # 수정: 총 일시정지 시간
    st.session_state.total_pause_time = 0
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 30 * 60  # 타이머 기본 시간
if 'remaining_seconds' not in st.session_state:
    st.session_state.remaining_seconds = 30 * 60
if 'timer_completed' not in st.session_state:
    st.session_state.timer_completed = False
if 'show_celebration' not in st.session_state:
    st.session_state.show_celebration = False
if 'selected_music' not in st.session_state:
    st.session_state.selected_music = "없음"
if 'music_auto_play' not in st.session_state:
    st.session_state.music_auto_play = True

def get_timer_status():
    """현재 타이머 상태 반환"""
    if st.session_state.timer_completed:
        return "completed"
    elif st.session_state.timer_running and not st.session_state.timer_paused:
        return "running"
    elif st.session_state.timer_paused:
        return "paused"
    else:
        return "stopped"

def update_timer():
    """타이머 업데이트 - 수정된 로직"""
    if st.session_state.timer_running and not st.session_state.timer_paused:
        current_time = time.time()
        elapsed = current_time - st.session_state.start_time - st.session_state.total_pause_time
        remaining = st.session_state.total_seconds - int(elapsed)
        
        if remaining <= 0:
            st.session_state.remaining_seconds = 0
            st.session_state.timer_running = False
            st.session_state.timer_completed = True
            st.session_state.show_celebration = True
        else:
            st.session_state.remaining_seconds = remaining

def format_time(seconds):
    """초를 HH:MM:SS 형태로 변환"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def reset_timer():
    """타이머 완전 리셋"""
    st.session_state.timer_running = False
    st.session_state.timer_paused = False
    st.session_state.start_time = None
    st.session_state.pause_start_time = None
    st.session_state.total_pause_time = 0
    st.session_state.remaining_seconds = st.session_state.total_seconds
    st.session_state.timer_completed = False
    st.session_state.show_celebration = False

def set_timer_duration(minutes):
    """타이머 시간 설정 및 슬라이더 동기화"""
    st.session_state.total_seconds = minutes * 60
    st.session_state.remaining_seconds = minutes * 60
    st.session_state.slider_minutes = minutes

update_timer()
current_status = get_timer_status()

col_left, col_right = st.columns(2)

with col_left:
    if st.session_state.total_seconds>0:
        progress = st.session_state.remaining_seconds/st.session_state.total_seconds
        progress = max(0,min(1, progress)) #0부터 1 사이의 값만 출력되도록 설정
    else:
        progress = 0

    st.progress(float(progress))

    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:
        if current_status=='running':
            st.markdown('**⏱️타이머**', help='타이머가 실행중입니다.')
        elif current_status=='paused':
            st.markdown('**⏱️타이머**', help='타이머가 일시정지 되었습니다.')
        elif current_status=='completed':
            st.markdown('**⏱️타이머**', help='타이머가 완료되었습니다.')
        else:
            st.markdown('**⏱️타이머**', help='타이머가 대기중입니다.')

    with status_col3:
        st.markdown(f'<p style="text-align:right;"><strong>{int(progress*100)}%</strong></p>'
        , unsafe_allow_html=True)

    st.subheader('남은 시간')
    st.markdown("""
        <style>
        /* 버튼 컨테이너 가운데 정렬 */
        .stColumns > div {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        </style>
    """, unsafe_allow_html=True)

    time_color = "#ff4444" if st.session_state.remaining_seconds <= 60 else "var(--primary-text-color)"

    st.markdown(f"""
    <div class="timer-time" style="text-align: center; font-size: 4rem; font-weight: bold; 
                color: {time_color}; margin: 2rem 0;">
        {format_time(st.session_state.remaining_seconds)}
    </div>
    """, unsafe_allow_html=True)

    # 통계 섹션
    if st.session_state.total_seconds > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("설정 시간", format_time(st.session_state.total_seconds))
        with col2:
            elapsed = st.session_state.total_seconds - st.session_state.remaining_seconds
            st.metric("경과 시간", format_time(elapsed))

    # 타이머 완료 처리
    if st.session_state.timer_completed and st.session_state.show_celebration:
        st.balloons()
        st.success("타이머가 완료되었습니다.")

    # 남은 시간에 따른 경고
    if st.session_state.timer_running and not st.session_state.timer_paused:
        if st.session_state.remaining_seconds <= 10 and st.session_state.remaining_seconds > 0:
            st.error("🚨 10초 이하 남았습니다!")
        elif st.session_state.remaining_seconds <= 60 and st.session_state.remaining_seconds > 0:
            st.warning("⚠️ 1분 이하 남았습니다!")

    # 컨트롤 버튼
    button_col1, button_col2, button_col3 = st.columns([1, 1, 1])

    with button_col1:
        if not st.session_state.timer_running and not st.session_state.timer_paused:
            if st.button("▶️", key="play_btn", help="시작", type="primary"):
                st.session_state.timer_running = True
                st.session_state.start_time = time.time()
                st.session_state.total_pause_time = 0
                st.session_state.timer_completed = False
                st.toast("타이머가 시작되었습니다.")
                st.rerun()
        elif st.session_state.timer_running and not st.session_state.timer_paused:
            if st.button("⏸️", key="pause_btn", help="일시정지"):
                st.session_state.timer_paused = True
                st.session_state.pause_start_time = time.time()
                st.toast("타이머가 일시정지되었습니다.")
                st.rerun()
        elif st.session_state.timer_paused:
            if st.button("▶️", key="resume_btn", help="재개", type="primary"):
                st.session_state.timer_paused = False
                if st.session_state.pause_start_time:
                    pause_duration = time.time() - st.session_state.pause_start_time
                    st.session_state.total_pause_time += pause_duration
                    st.session_state.pause_start_time = None
                st.toast("타이머가 재개되었습니다.")
                st.rerun()

    with button_col2:
        if st.button("🔁", key="reset_btn", help="리셋"):
            st.session_state.timer_running = False
            st.session_state.timer_paused = False
            st.session_state.start_time = None
            st.session_state.pause_start_time = None
            st.session_state.total_pause_time = 0
            st.session_state.remaining_seconds = st.session_state.total_seconds
            st.session_state.timer_completed = False
            st.session_state.show_celebration = False
            st.toast("타이머가 리셋되었습니다.")
            st.rerun()

    with button_col3:
        if st.button("1분 추가", key="add_minute_btn", help="+1분 추가"):
            # 1분(60초) 추가
            st.session_state.remaining_seconds += 60
            st.session_state.total_seconds += 60
            # 타이머가 완료된 상태였다면 완료 상태 해제
            if st.session_state.timer_completed:
                st.session_state.timer_completed = False
                st.session_state.show_celebration = False
            st.toast("1분이 추가되었습니다!")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # 배경음악 리스트
    background_music = {
        "없음": None,
        "Bubblegum Code-2": "./music/Bubblegum Code-2.mp3",
        "Bubblegum Code": "./music/Bubblegum Code.mp3",
        "Code in the Moonlight": "./music/Code in the Moonlight.mp3",
        "Gentle Streams": "./music/Gentle Streams.mp3",
        "Late Night Thoughts": "./music/Late Night Thoughts.mp3",
        "Soft Light Waves": "./music/Soft Light Waves.mp3"
    }

    # 배경음악 섹션
    st.markdown('<div class="music-container">', unsafe_allow_html=True)
    st.markdown("🎵 **배경 음악**")

    st.markdown("**음악 선택**")
    selected_music = st.selectbox(
        "음악을 선택하세요:",
        options=list(background_music.keys()),
        index=list(background_music.keys()).index(st.session_state.selected_music),
        key="music_select",
        label_visibility="collapsed"
    )
    st.session_state.selected_music = selected_music

    if st.session_state.selected_music!='없음':
        try:
            # music 폴더가 streamlit app과 같은 디렉토리에 있다고 가정
            audio_file_path = f"{background_music[st.session_state.selected_music]}"
            st.audio(audio_file_path, format="audio/mpeg", loop=True, autoplay=st.session_state.music_auto_play)
        except Exception as e:
            st.warning(f"음악 파일을 찾을 수 없습니다: {audio_file_path}")
    
    # 음악 자동재생 설정
    auto_play = st.toggle("음악 자동재생", value=st.session_state.music_auto_play, key="auto_play_toggle")
    st.session_state.music_auto_play = auto_play

    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    pass