import json, random, base64
from pathlib import Path
from datetime import date, datetime, timedelta
from html import escape
import streamlit as st
st.set_page_config(page_title="단단이 V0.5.2 아침 알림 설계",page_icon="🌱",layout="centered")
BASE=Path(__file__).resolve().parent
ALL=[]
for f in ('quotes.json','deep_quotes.json','curated_quotes.json'):
    ALL+=json.loads((BASE/f).read_text(encoding='utf-8'))
MORNING=json.loads((BASE/'morning_quotes.json').read_text(encoding='utf-8'))
ALL+=MORNING
BY_ID={q['id']:q for q in ALL}
CATS=list(dict.fromkeys(q['category'] for q in ALL))
STORE=BASE/'my_dandani_v04.json'
DEFAULT={'favorites':[],'promises':[],'notification':{'enabled':False,'time':'08:00','frequency':'매일','days':['월','수','금'],'topics':['희망'],'timezone':'Asia/Seoul'}}
def load():
    try:
        obj=json.loads(STORE.read_text(encoding='utf-8')) if STORE.exists() else {}
        return {**DEFAULT,**obj,'notification':{**DEFAULT['notification'],**obj.get('notification',{})}}
    except (ValueError,OSError):return json.loads(json.dumps(DEFAULT,ensure_ascii=False))
if 'data' not in st.session_state:st.session_state.data=load()
if 'positions' not in st.session_state:st.session_state.positions={}
if 'category' not in st.session_state:st.session_state.category='희망' if '희망' in CATS else CATS[0]
if 'selected_topic' not in st.session_state:st.session_state.selected_topic=None
def save():
    tmp=STORE.with_suffix('.tmp')
    tmp.write_text(json.dumps(st.session_state.data,ensure_ascii=False,indent=2),encoding='utf-8')
    tmp.replace(STORE)
def img(name):
    return base64.b64encode((BASE/'assets'/f'{name}.jpg').read_bytes()).decode()
IMAGES={k:img(k) for k in ['sunset','forest','chapel','sprout','window','mountain','room','lake','sunrise','book','stars']}
def theme(cat):
    if cat in ('신학',):return 'chapel'
    if cat in ('희망','소망'):return 'sunrise'
    if cat in ('철학',):return 'book'
    if cat in ('윤리','자기존중'):return 'forest'
    if cat in ('고독','관계'):return 'window'
    if cat in ('자립','용기','성장'):return 'mountain'
    return 'lake'
st.markdown('''<style>
.stApp{background:linear-gradient(165deg,#111a1e,#202b2b 65%,#282a28);color:#f7f3e9}
.block-container{max-width:860px;padding-top:1.25rem;padding-bottom:3rem}
.hero,.photo-card{background-size:cover;background-position:center;border-radius:20px;overflow:hidden;border:1px solid #65736b;box-shadow:0 10px 25px #0004}
.hero{min-height:275px;padding:36px 27px;display:flex;flex-direction:column;justify-content:flex-end}
.photo-card{min-height:235px;padding:25px 22px;display:flex;flex-direction:column;justify-content:flex-end;margin:16px 0}
.photo-tag{color:#f2e9d5;font-size:.9rem;font-weight:600;margin-bottom:12px}
.photo-text{font-size:1.48rem;line-height:1.6;color:#fffaf0;font-weight:750;text-shadow:0 2px 6px #0009}
.hero .photo-text{font-size:1.9rem}
.subline{color:#d7e3d9;font-size:.94rem;margin-top:9px}
.stTabs [data-baseweb="tab"]{font-size:.89rem}
.topic-image{height:135px;background-position:center;background-size:cover;border-radius:15px 15px 0 0;display:flex;align-items:end;padding:14px;border:1px solid #52625b;border-bottom:0}
.topic-image strong{font-size:1.35rem;color:white;text-shadow:0 2px 6px #000}
.topic-caption{font-size:.82rem;color:#c9d7d0;margin:8px 0 12px;min-height:2.3em}
.topic-image{position:relative;isolation:isolate}
.topic-image strong{position:relative;z-index:1;line-height:1.25;letter-spacing:-.02em}
.topic-image:before{content:'';position:absolute;inset:0;background:linear-gradient(0deg,rgba(5,12,15,.72),transparent 75%);z-index:0}
div[data-testid="stColumn"] button[kind="secondary"]{border-radius:0 0 13px 13px;width:100%;min-height:42px}
@media(max-width:600px){.topic-image{height:110px;padding:10px}.topic-image strong{font-size:1.1rem}}
[data-testid="stExpander"]{background:#1e2a2b;border-radius:12px}
@media(max-width:600px){.hero{min-height:230px;padding:20px}.photo-card{min-height:195px;padding:19px}.photo-text{font-size:1.22rem}.hero .photo-text{font-size:1.48rem}}

/* V0.4.1 visual polish: presentation-only changes; original card/expander logic retained */
.block-container{max-width:1000px;padding-left:clamp(1rem,3vw,2.3rem);padding-right:clamp(1rem,3vw,2.3rem)}
.stApp{background:radial-gradient(circle at 80% 0%,#263632 0%,transparent 38%),linear-gradient(165deg,#10191e,#1b2829 62%,#242b28)}
.topic-image{height:176px;border-radius:17px 17px 0 0;padding:17px;background-position:center;box-shadow:inset 0 -24px 36px #0710148c;transition:filter .18s ease}
.topic-image:before{background:linear-gradient(0deg,rgba(4,11,15,.91),rgba(4,11,15,.32) 43%,rgba(4,11,15,.03) 85%)}
.topic-image strong{font-size:1.43rem;line-height:1.3;letter-spacing:-.03em;text-shadow:0 2px 8px #000c}
.topic-caption{font-size:.83rem;color:#cdd9d2;min-height:2.1em;margin:10px 2px 18px;line-height:1.45}
div[data-testid="stColumn"] button[kind="secondary"]{border:1px solid #52635f;border-radius:0 0 14px 14px;min-height:46px;background:#131b22;color:#f8f5ec;font-weight:650;transition:background .18s ease,border-color .18s ease}
div[data-testid="stColumn"] button[kind="secondary"]:hover{background:#263934;border-color:#9ab2a5}
.hero,.photo-card{box-shadow:0 14px 34px #0005;border-color:#52645d}
.hero .photo-text{font-size:clamp(1.5rem,3vw,2rem)}
[data-testid="stExpander"]{border:1px solid #52635c}
@media(max-width:700px){.block-container{padding-left:.8rem;padding-right:.8rem}.topic-image{height:125px;padding:10px}.topic-image strong{font-size:1.1rem}.topic-caption{font-size:.75rem;min-height:2.8em}div[data-testid="stColumn"] button[kind="secondary"]{min-height:44px;font-size:.75rem;padding:5px}}
@media(max-width:430px){.topic-image{height:105px;padding:8px}.topic-image strong{font-size:.95rem}.topic-caption{font-size:.7rem;line-height:1.35}.hero{min-height:235px}}
</style>''',unsafe_allow_html=True)
with st.sidebar:
    st.markdown('### 🌱 단단이')
    st.caption('나의 속도로 시작하는 하루')
    creative_mode=st.toggle('✨ 나만의 하루 창조하기',value=False,help='원하는 사람만 여는 선택형 공간입니다.')
    st.caption('켜지 않아도 모든 기본 기능을 사용할 수 있어요.')

st.title('🌱 단단이')
st.caption('마음의 자립 연구소 · V0.5.2 아침 알림 설계')
st.markdown('**혼자여도, 나의 삶은 단단해진다.**')
if creative_mode:
    st.markdown('### ✨ 나만의 하루 창조하기')
    st.write('오늘을 특별하게 만들 의무는 없어요. 마음이 내킬 때만 작은 축제를 꾸려보세요.')
    choices={
        '한 가지 맛': ['따뜻한 차 한 잔','좋아하는 음식','간단한 간식','오늘은 건너뛰기'],
        '한 가지 분위기': ['좋아하는 음악','창문 열고 바람 느끼기','작은 조명','오늘은 건너뛰기'],
        '한 가지 활동': ['짧은 글쓰기','영화 한 편','산책','오늘은 건너뛰기']
    }
    with st.form('creative_day'):
        picked={name:st.selectbox(name,items) for name,items in choices.items()}
        make=st.form_submit_button('나의 하루 계획 보기')
    if make:
        st.success('오늘은 이렇게 시작해도 좋아요. ' + ' · '.join(picked.values()))
        st.caption('실천하지 못해도 괜찮아요. 계획은 언제든 바꿀 수 있어요.')
    st.divider()
def card(q,tag,hero=False):
    bg=IMAGES['sunset' if hero else theme(q['category'])]
    cls='hero' if hero else 'photo-card'
    st.markdown(f'''<div class="{cls}" style="background-image:linear-gradient(0deg,rgba(9,19,23,.91),rgba(12,24,25,.24)),url(data:image/jpeg;base64,{bg})"><div class="photo-tag">{escape(tag)}</div><div class="photo-text">{escape(q['text'])}</div><div class="subline">단단이 · {escape(q['category'])}</div></div>''',unsafe_allow_html=True)
def detail(q):
    st.markdown('**깊이 있는 해설**');st.write(q.get('reflection','이 문장이 지금 나에게 어떤 의미인지 생각해 보세요.'))
    st.markdown('**사상적 배경**');st.write(q.get('background','단단이의 창작 문장입니다. 특정 철학자의 직접 인용은 아닙니다.'))
    st.markdown('**오늘의 작은 실천**');st.info(q.get('action','오늘 스스로 선택할 수 있는 작은 행동을 적어보세요.'))
    st.caption('단단이 창작 문장 · 사상 설명은 학습용 요약이며 직접 인용이 아닙니다.')
def fav(q,key):
    if st.button('♡ 이 문장 저장',key=key):
        if q['id'] not in st.session_state.data['favorites']:
            st.session_state.data['favorites'].append(q['id']);save();st.success('문장 보관함에 저장했어요.')
        else:st.info('이미 저장한 문장이에요.')
t1,t2,t3,t4,t5=st.tabs(['오늘의 마음','문장 보관함','나의 다짐','알림 설정','연구소 원칙'])
with t1:
    st.subheader('🌅 오늘의 단단이 · 하루의 첫 장면')
    st.caption('서두르지 않아도 괜찮아요. 오늘의 문장을 천천히 읽어보세요.')
    daily=MORNING[random.Random(date.today().isoformat()).randrange(len(MORNING))]
    card(daily,f'{date.today().isoformat()} · 오늘의 한 문장',hero=True)
    with st.expander('📖 오늘의 문장 해설 · 사상적 배경 · 작은 실천',expanded=True):
        detail(daily)
    fav(daily,'daily_fav')
    st.divider()
    st.subheader('🖼️ 마음의 풍경 · 사진형 카테고리')
    st.caption('사진 아래 ‘이 주제 탐색’을 누르면 해당 카드 줄 바로 아래에 해설이 펼쳐집니다.')
    priority=['고독','자립','희망','철학','신학','윤리','용기','관계','성장','자기존중','소망']
    topics=[x for x in priority if x in CATS]+[x for x in CATS if x not in priority]
    descriptions={'고독':'혼자 있는 시간의 의미','자립':'내 삶의 주도권','희망':'내일을 향한 가능성','철학':'생각하고 선택하는 삶','신학':'은혜와 소망의 언어','윤리':'존엄과 서로의 책임','용기':'두려움과 함께 걷기','관계':'연결을 선택하는 마음','성장':'작은 변화의 기록','자기존중':'나를 함부로 대하지 않기','소망':'기다림 속의 빛'}
    for start in range(0,len(topics),3):
        columns=st.columns(3,gap='small')
        for col,topic in zip(columns,topics[start:start+3]):
            with col:
                picture=IMAGES[theme(topic)]
                st.markdown(f"""<div class='topic-image' style='background-image:linear-gradient(0deg,#071014c9,#07101411),url(data:image/jpeg;base64,{picture})'><strong>{escape(topic)}</strong></div>""",unsafe_allow_html=True)
                if st.button('이 주제 탐색 →',key=f'topic_{topic}',use_container_width=True):
                    st.session_state.selected_topic=topic
                    st.session_state.category=topic
                    st.rerun()
                st.markdown(f"<div class='topic-caption'>{escape(descriptions.get(topic,'나의 마음을 들여다보기'))}</div>",unsafe_allow_html=True)
        # 기존 사진형 카드 3열을 유지하면서 선택된 줄 바로 아래 해설을 노출한다.
        row_topics=topics[start:start+3]
        selected=st.session_state.selected_topic
        if selected in row_topics:
            pool_inline=[item for item in ALL if item['category']==selected]
            if pool_inline:
                inline_pos=st.session_state.positions.get(selected,0)%len(pool_inline)
                inline_q=pool_inline[inline_pos]
                st.markdown(f'#### 🌱 {selected} · 문장과 해설')
                st.caption('선택한 사진 카드에 연결된 내용입니다. 아래에서 바로 읽을 수 있어요.')
                card(inline_q,f'{selected} · {inline_pos+1}/{len(pool_inline)}')
                with st.expander('📖 문장의 의미 · 사상적 배경 · 작은 실천',expanded=True):
                    detail(inline_q)
                a,b=st.columns(2)
                with a:
                    if st.button('↻ 이 주제의 다음 문장',key=f'inline_next_{selected}',use_container_width=True):
                        st.session_state.positions[selected]=(inline_pos+1)%len(pool_inline)
                        st.rerun()
                with b:
                    fav(inline_q,f'inline_fav_{selected}')
    st.divider()
    st.subheader('삶의 상황과 사상으로 문장 찾기')
    st.caption('철학·신학·윤리 등 주제를 선택해 문장과 해설을 읽어보세요.')
    cat=st.selectbox('오늘 필요한 마음 또는 사상',CATS,key='category')
    if st.session_state.selected_topic == cat:
        st.success(f'📍 {cat} 카테고리를 선택했어요. 아래 문장과 해설을 살펴보세요.')
    pool=[q for q in ALL if q['category']==cat]
    pos=st.session_state.positions.get(cat,0)%len(pool)
    q=pool[pos]
    card(q,f'{cat} · {pos+1}/{len(pool)}')
    with st.expander('📖 이 문장의 해설 · 사상적 배경 · 작은 실천'):
        detail(q)
    left,right=st.columns(2)
    with left:
        if st.button('↻ 다른 문장 보기',use_container_width=True):
            st.session_state.positions[cat]=(pos+1)%len(pool);st.rerun()
    with right:
        fav(q,'selected_fav')
    st.info('단단이는 혼자서 모든 것을 견디라고 요구하지 않습니다. 도움을 요청하는 것도 자립의 한 방법입니다.')
with t2:
    st.subheader('내가 간직한 문장')
    favs=st.session_state.data['favorites']
    if not favs:st.info('아직 저장한 문장이 없어요.')
    for i,v in enumerate(favs[:]):
        q=BY_ID.get(v) or next((x for x in ALL if x['text']==v),None)
        st.write('🌱 '+(q['text'] if q else str(v)))
        if q:
            with st.expander('해설 보기',key=f'fav_detail_{i}'):
                detail(q)
        if st.button('삭제',key=f'remove_fav_{i}'):
            favs.pop(i);save();st.rerun()
with t3:
    st.subheader('나의 다짐')
    with st.form('promise',clear_on_submit=True):
        val=st.text_area('오늘 내가 선택할 수 있는 작은 행동',max_chars=300)
        submit=st.form_submit_button('다짐 저장')
    if submit:
        if val.strip():
            st.session_state.data['promises'].append({'date':date.today().isoformat(),'text':val.strip()});save();st.success('저장했어요.')
        else:st.warning('다짐을 입력해 주세요.')
    for i in range(len(st.session_state.data['promises'])-1,-1,-1):
        v=st.session_state.data['promises'][i]
        st.write(f'**{v.get("date","")}** · {v.get("text","")}')
        if st.button('삭제',key=f'remove_promise_{i}'):
            st.session_state.data['promises'].pop(i);save();st.rerun()
with t4:
    st.subheader('🔔 오늘의 단단이 · 나의 아침 알림')
    st.caption('필요할 때만 열어보는 작은 초대. 알림을 켜지 않아도 단단이는 그대로 사용할 수 있어요.')
    st.warning('현재는 알림 **설정 저장 및 미리보기** 단계입니다. 실제 휴대전화·브라우저 푸시, 이메일, 예약 발송은 제공하지 않습니다.')
    n=st.session_state.data['notification']
    times=[f'{h:02d}:{m:02d}' for h in range(24) for m in (0,30)]
    freqs=['매일','주 3회','주 1회']
    days_list=['월','화','수','목','금','토','일']
    with st.form('notification'):
        enabled=st.toggle('🔔 알림을 받고 싶어요 (기본 꺼짐)',value=n.get('enabled',False))
        clock=st.selectbox('원하는 시간 (한국 시간)',times,index=times.index(n.get('time','08:00')) if n.get('time') in times else 16)
        freq=st.radio('희망 빈도',freqs,index=freqs.index(n.get('frequency','매일')) if n.get('frequency') in freqs else 0,horizontal=True)
        days=st.multiselect('희망 요일 (주 3회 또는 주 1회)',days_list,default=[x for x in n.get('days',[]) if x in days_list],disabled=freq=='매일')
        topics=st.multiselect('글귀 주제',CATS,default=[x for x in n.get('topics',[]) if x in CATS])
        submit=st.form_submit_button('💾 나의 알림 취향 저장',use_container_width=True)
    if submit:
        required={'주 3회':3,'주 1회':1}.get(freq)
        if enabled and not topics:
            st.warning('알림을 켜려면 주제를 하나 이상 선택해 주세요.')
        elif enabled and required and len(days)!=required:
            st.warning(f'{freq}를 선택했으므로 요일 {required}개를 골라 주세요.')
        else:
            st.session_state.data['notification']={'enabled':enabled,'time':clock,'frequency':freq,'days':days if freq!='매일' else [],'topics':topics,'timezone':'Asia/Seoul'}
            save()
            st.success('알림 취향을 저장했어요. 실제 발송은 아직 시작되지 않았습니다.')
            st.rerun()
    n=st.session_state.data['notification']
    st.divider()
    st.markdown('#### 📋 저장된 알림 취향')
    if n.get('enabled',False):
        weekdays='매일' if n.get('frequency')=='매일' else ', '.join(n.get('days',[]))+'요일'
        st.write(f"**희망 시각:** {n.get('time','08:00')} (한국 시간) · **빈도:** {n.get('frequency','매일')} ({weekdays})")
        st.write('**선택한 주제:** '+', '.join(n.get('topics',[])))
    else:
        st.info('알림 희망 설정이 꺼져 있어요. 필요한 날에 직접 방문해도 괜찮습니다.')
    st.markdown('#### 💌 알림 문구 미리보기')
    selected_topics=n.get('topics',[])
    sample_pool=[q for q in MORNING if q['category'] in selected_topics] or [q for q in ALL if q['category'] in selected_topics] or MORNING
    preview=sample_pool[random.Random(date.today().isoformat()+'dandani-preview').randrange(len(sample_pool))]
    st.markdown('**🌱 오늘의 단단이 글귀!**')
    st.write('“'+preview['text']+'”')
    st.caption('이 화면은 알림이 실제로 도착한 것이 아니라 앱 안의 미리보기입니다.')
    with st.expander('📖 알림을 눌렀을 때 읽을 내용 미리보기',expanded=False):
        detail(preview)
    if st.button('🔕 알림 희망 설정 끄기',disabled=not n.get('enabled',False),use_container_width=True):
        st.session_state.data['notification']['enabled']=False
        save()
        st.rerun()
    st.caption('향후 실제 푸시 기능을 도입할 때는 별도의 권한 동의와 발송 인프라가 필요합니다. 저장한 설정만으로 알림이 발송되지는 않습니다.')
with t5:
    st.subheader('단단이 연구소의 원칙')
    for p in ['존엄성은 성취·재산·관계의 유무로 결정되지 않습니다.','고독을 부정하지 않으며 자립을 고립과 혼동하지 않습니다.','위로는 출발점이고 자기 결정과 현실적 행동이 목적지입니다.','도움을 요청하는 것도 자립의 한 방법입니다.','신학·철학·윤리학은 강요하지 않고 선택할 수 있게 합니다.','직접 인용과 단단이 창작 문장을 구별합니다.','알림은 사용자의 선택에 따르며 언제든 끌 수 있어야 합니다.']:
        st.write('• '+p)
st.divider()
st.caption('V0.5.2 개인 개발 시제품 · 배경 이미지는 생성형 이미지에서 편집한 창작 비주얼입니다. 실제 사진이 아닙니다. 기록은 로컬 JSON에 저장되며 Colab 초기화 시 소실될 수 있습니다. 여러 사용자가 사용하는 공개 서비스로 배포하지 마세요.')
