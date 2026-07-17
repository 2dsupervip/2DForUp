import streamlit as st
import pandas as pd
from collections import Counter
import random

# ==========================================
# 1. PAGE CONFIG & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="2D Master AI Scanner", page_icon="🎯", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0B031A; color: #E0D5FA; }
    h1, h2, h3, h4, h5 { color: #00FFCC !important; }
    .stNumberInput>div>div>input, .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #170E2B !important; color: #00FFCC !important; border: 1px solid #4A3B69 !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #A078FF 0%, #00FFCC 100%);
        color: #000000 !important; font-weight: bold !important; border: none !important; border-radius: 8px !important;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #170E2B; border-radius: 8px 8px 0px 0px; border: 1px solid #4A3B69; border-bottom: none;
    }
    .stTabs [aria-selected="true"] { background-color: #3498db; color: #FFFFFF !important; }
    .success-box { background-color: #170E2B; padding: 15px; border-radius: 10px; border-left: 5px solid #00FFCC; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA SETUP (Dummy Data Generation)
# ==========================================
if 'full_draws' not in st.session_state:
    dummy_data = []
    # ဖန်တီးထားသော Dummy အချက်အလက် (နောက်ဆုံး ပွဲ ၁၀၀)
    for i in range(100):
        num = f"{random.randint(0, 99):02d}"
        dummy_data.append({"index": i, "draw": num, "time": "12 PM" if i%2==0 else "4 PM"})
    st.session_state.full_draws = dummy_data
    st.session_state.day_pairs = dummy_data 

# 2D Patterns (Master Formulas)
PATTERNS = {
    "ညီအစ်ကို": ['01', '10', '12', '21', '23', '32', '34', '43', '45', '54', '56', '65', '67', '76', '78', '87', '89', '98', '90', '09'],
    "ပါဝါ": ['05', '50', '16', '61', '27', '72', '38', '83', '49', '94'],
    "နက္ခတ်": ['07', '70', '18', '81', '24', '42', '35', '53', '69', '96']
}

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def get_custom_target_hits(trigger_val, session_scope, draws, day_pairs=None):
    hits = []
    for i, d in enumerate(draws):
        match = False
        if trigger_val in d['draw']:
            if session_scope == "All": match = True
            elif session_scope == "AM သီးသန့်" and d['time'] == "12 PM": match = True
            elif session_scope == "PM သီးသန့်" and d['time'] == "4 PM": match = True
        if match:
            hits.append(d)
    return hits, []

def detect_active_patterns(day_pairs, recent_count=10):
    return [("12", "12 AM သီးသန့်"), ("34", "34 PM သီးသန့်")]

# ==========================================
# 4. MAIN UI & TABS
# ==========================================
st.title("🎯 2D Master AI Scanner (Pro Edition)")
tab_vip, tab_pattern, tab_chain = st.tabs(["💎 Tab 1: VIP Tracker", "🧬 Tab 2: Pattern Scanner", "🔗 Tab 3: Accumulation System"])

# ------------------------------------------
# TAB 1: VIP TRACKER (Fully Functional Logic)
# ------------------------------------------
with tab_vip:
    st.markdown("##### 💎 VIP Tracker (Dual Scanner)")
    with st.form("vip_scanner_form"):
        c_set1, c_set2 = st.columns(2)
        with c_set1:
            max_anchor_t1 = st.number_input("⏳ သမိုင်းကြောင်း ရှာဖွေမည့် ပွဲစဉ် (Max Anchor):", min_value=10, max_value=200, value=50, key="ma_t1")
        with c_set2:
            min_win_rate_t1 = st.number_input("🎯 လိုချင်သော မှန်ကန်မှု (Win Rate %):", min_value=80, max_value=100, value=100, key="wr_t1")
            
        scanner_mode = st.radio("🔍 Scanner စနစ် ရွေးချယ်ရန်:", [
            "⚡ 1. Quick Scanner (အလွယ်ရှာမည်)", 
            "🎯 2. Deep Sniper Scanner (သတ်မှတ် Win Rate % အတိုင်းတိကျစွာရှာမည်)"
        ])
        check_span = st.number_input("စောင့်ကြည့်မည့် ပွဲစဉ် အရေအတွက် (Span):", min_value=1, max_value=20, value=5)
        submit_vip = st.form_submit_button("🚀 VIP မူများ ရှာဖွေပါ")

    if submit_vip:
        st.info(f"ရှာဖွေနေပါသည်... (Max Anchor: {max_anchor_t1} ပွဲ | Target Win Rate: {min_win_rate_t1}%)")
        search_pool = st.session_state.full_draws[-max_anchor_t1:] if max_anchor_t1 < len(st.session_state.full_draws) else st.session_state.full_draws
        
        found_signals = []
        # Logic: 00 မှ 99 ထိ A ဂဏန်းများကို ရှာဖွေခြင်း
        for i in range(100):
            target_a = f"{i:02d}"
            a_indices = [idx for idx, val in enumerate(search_pool) if val['draw'] == target_a]
            
            if len(a_indices) >= 3: # အနည်းဆုံး ၃ ကြိမ်ထွက်ဖူးမှ တွက်မည်
                all_b_draws = []
                for a_idx in a_indices:
                    # နောက်ထပ် Span အတွင်း ထွက်ခဲ့သော ဂဏန်းများ (B) ကို ရှာမည်
                    end_idx = min(a_idx + 1 + check_span, len(search_pool))
                    b_window = [search_pool[k]['draw'] for k in range(a_idx + 1, end_idx)]
                    all_b_draws.append(set(b_window))
                
                if all_b_draws:
                    # အမြဲတမ်းပါဝင်သော ဂဏန်းများ (Common Elements)
                    common_b = set.intersection(*all_b_draws) if scanner_mode == "🎯 2. Deep Sniper Scanner (သတ်မှတ် Win Rate % အတိုင်းတိကျစွာရှာမည်)" else set.union(*all_b_draws)
                    
                    if common_b:
                        for target_b in common_b:
                            hit_count = sum(1 for window in all_b_draws if target_b in window)
                            win_rate = (hit_count / len(a_indices)) * 100
                            
                            # 🔴 90% Leak Error ကို ဤနေရာတွင် User ရွေးချယ်မှုဖြင့် စစ်ထုတ်သည်
                            if win_rate >= min_win_rate_t1:
                                found_signals.append({
                                    "A": target_a, "B": target_b, 
                                    "Hits": f"{hit_count}/{len(a_indices)}", 
                                    "WinRate": win_rate
                                })
        
        if found_signals:
            st.success(f"✅ VIP မူများ တွေ့ရှိပါသည် ({len(found_signals)} ခု)")
            for sig in sorted(found_signals, key=lambda x: x['WinRate'], reverse=True)[:10]: # အကောင်းဆုံး ၁၀ ခုပြမည်
                st.markdown(f"""
                <div class="success-box">
                    <span style='color:#00FFCC; font-size:18px;'>🎯 [{sig['A']}] ထွက်ပြီးနောက် {check_span} ပွဲအတွင်း </span><br>
                    <span style='color:#E0D5FA;'>👉 <b>[{sig['B']}]</b> ထွက်နှုန်း: {sig['WinRate']:.1f}% (ကြိမ်ရေ: {sig['Hits']})</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ {min_win_rate_t1}% နှင့် ကိုက်ညီသော မူများ မတွေ့ရှိပါ။ Win Rate ကို အနည်းငယ် လျှော့၍ ထပ်ရှာကြည့်ပါ။")

# ------------------------------------------
# TAB 2: PATTERN SCANNER (Fully Functional Logic)
# ------------------------------------------
with tab_pattern:
    st.markdown("##### 🧬 Pattern Scanner (Master Formulas)")
    with st.form("pattern_scanner_form"):
        c_set3, c_set4 = st.columns(2)
        with c_set3:
            max_anchor_t2 = st.number_input("⏳ သမိုင်းကြောင်း ရှာဖွေမည့် ပွဲစဉ် (Max Anchor):", min_value=10, max_value=200, value=50, key="ma_t2")
        with c_set4:
            min_win_rate_t2 = st.number_input("🎯 လိုချင်သော မှန်ကန်မှု (Win Rate %):", min_value=80, max_value=100, value=100, key="wr_t2")
            
        pat_mode = st.selectbox("ရှာဖွေမည့် ပုံစံ (Pattern):", ["ညီအစ်ကို", "ပါဝါ", "နက္ခတ်"])
        check_span_p = st.number_input("စောင့်ကြည့်မည့် ပွဲစဉ် အရေအတွက် (Span):", min_value=1, max_value=20, value=5, key="span_p")
        submit_pattern = st.form_submit_button("🔍 Pattern များ ရှာဖွေပါ")

    if submit_pattern:
        st.info(f"ရှာဖွေနေပါသည်... Pattern: {pat_mode} | Max Anchor: {max_anchor_t2} | Win Rate: {min_win_rate_t2}%")
        search_pool_t2 = st.session_state.full_draws[-max_anchor_t2:] if max_anchor_t2 < len(st.session_state.full_draws) else st.session_state.full_draws
        target_pattern_list = PATTERNS.get(pat_mode, [])
        
        # Logic: Pattern များဝင်ခဲ့သော နေရာများ ရှာဖွေခြင်း
        pat_indices = [idx for idx, val in enumerate(search_pool_t2) if val['draw'] in target_pattern_list]
        
        if len(pat_indices) >= 2:
            all_b_draws = []
            for p_idx in pat_indices:
                end_idx = min(p_idx + 1 + check_span_p, len(search_pool_t2))
                b_window = [search_pool_t2[k]['draw'] for k in range(p_idx + 1, end_idx)]
                all_b_draws.append(set(b_window))
                
            if all_b_draws:
                common_b = set.intersection(*all_b_draws) if all_b_draws else set()
                found_patterns = []
                
                for target_b in common_b:
                    hit_count = sum(1 for window in all_b_draws if target_b in window)
                    win_rate = (hit_count / len(pat_indices)) * 100
                    
                    if win_rate >= min_win_rate_t2:
                        found_patterns.append({"B": target_b, "Hits": f"{hit_count}/{len(pat_indices)}", "WinRate": win_rate})
                
                if found_patterns:
                    st.success(f"✅ {pat_mode} Pattern အတွက် မူများ တွေ့ရှိပါသည်!")
                    for sig in sorted(found_patterns, key=lambda x: x['WinRate'], reverse=True)[:10]:
                        st.markdown(f"""
                        <div class="success-box">
                            <span style='color:#00FFCC; font-size:18px;'>🧬 [{pat_mode}] ထွက်ပြီးနောက် {check_span_p} ပွဲအတွင်း </span><br>
                            <span style='color:#E0D5FA;'>👉 <b>[{sig['B']}]</b> ထွက်နှုန်း: {sig['WinRate']:.1f}% (ကြိမ်ရေ: {sig['Hits']})</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning(f"⚠️ {pat_mode} Pattern အတွက် {min_win_rate_t2}% ပြည့်မီသော မူများ မတွေ့ရှိပါ။")
        else:
            st.warning(f"သမိုင်းကြောင်း {max_anchor_t2} ပွဲအတွင်း {pat_mode} Pattern အလုံအလောက် မထွက်ခဲ့ပါ။")

# ------------------------------------------
# TAB 3: AUTO-TUNED OMNI-CHAIN (Accumulation System)
# ------------------------------------------
with tab_chain:
    st.markdown("##### 🔗 Auto-Tuned Omni-Chain (Accumulation System)")
    with st.form("chain_reaction_form"):
        chain_mode = st.radio("🔍 အစပျိုးစနစ် ရွေးချယ်ရန်:", ["🤖 Auto Mode (AI အလိုအလျောက်ရှာမည်)", "✍️ Custom Mode (မိမိစိတ်ကြိုက် အစပျိုးမည်)"])
        
        c1, c2 = st.columns(2)
        last_val = st.session_state.full_draws[-1]['time'] if st.session_state.full_draws else "12 PM"
        with c1: 
            chain_anchor_count = st.number_input("📌 (Auto) နောက်ကြောင်းပြန်မည့် ပွဲစဉ် (Anchor):", min_value=1, max_value=50, value=10)
            chain_trigger_custom = st.text_input("🎯 (Custom) အစပျိုး မူ (Primary Trigger A):", value=f"{last_val} သီးသန့်")
        with c2: 
            chain_span1 = st.number_input("၂။ B အတွက် စောင့်ကြည့်မည့် ပွဲစဉ် (Span 1):", min_value=1, max_value=30, value=10)
            chain_max_target_step = st.number_input("၃။ C အတွက် ရှာမည့် အများဆုံး ပွဲစဉ် (Target Step):", min_value=1, max_value=20, value=5)

        c3, c4 = st.columns(2)
        with c3: 
            target_accumulation_size = st.number_input("၄။ လိုချင်သော စုစုပေါင်း ကွက်ရေ (Target Coverage):", min_value=1, max_value=30, value=12)
        with c4: 
            st.info("💡 AI သည် အကောင်းဆုံး Rank မှစ၍ အောက်သို့ဆင်းကာ၊ ဤကွက်ရေပြည့်သည်အထိ ဂဏန်းများကို အလိုအလျောက် စုပေါင်း (Accumulate) လုပ်ပေးသွားပါမည်။")
        
        submit_chain = st.form_submit_button("🔥 ယခုပွဲစဉ် Live Signal များကို ရှာမည် 🚀")

    if submit_chain:
        with st.spinner(f"🧠 ကွက်ရေ ({target_accumulation_size}) ကွက် ပြည့်သည်အထိ အကောင်းဆုံး ကွင်းဆက်များကို အဆင့်လိုက် စုပေါင်းရှာဖွေနေပါသည်..."):
            trigger_list = []
            if "Auto Mode" in chain_mode:
                active_pats = detect_active_patterns(st.session_state.day_pairs, chain_anchor_count)
                for pat_search, pat_display in active_pats:
                    sess = "All"
                    if "မနက်ပိုင်း" in pat_display: sess = "AM သီးသန့်"
                    elif "ညနေပိုင်း" in pat_display: sess = "PM သီးသန့်"
                    trigger_list.append((pat_search, pat_display, sess))
                
                recent_draws = st.session_state.full_draws[-chain_anchor_count:]
                for d in recent_draws:
                    d_val, d_time = d['draw'], d['time']
                    trigger_list.append((d_val, f"လတ်တလော အမာခံဂဏန်း ({d_val} {d_time})", f"{d_time} သီးသန့်"))
                trigger_list = list(set(trigger_list))
            else:
                raw_trig = chain_trigger_custom.strip()
                sess = "All"
                if "AM သီးသန့်" in raw_trig: 
                    sess, raw_trig = "AM သီးသန့်", raw_trig.replace("AM သီးသန့်", "").strip()
                elif "PM သီးသန့်" in raw_trig: 
                    sess, raw_trig = "PM သီးသန့်", raw_trig.replace("PM သီးသန့်", "").strip()
                trigger_list = [(raw_trig, chain_trigger_custom.strip(), sess)]

            priorities = sorted([{'trend': t, 'size': s, 'score': (t * 10) - (s * 2)} for t in range(15, 4, -1) for s in range(1, 13)], key=lambda x: x['score'], reverse=True)

            live_signals_results, top_summary_pool, used_signatures = [], set(), set()

            for trig_search, trig_display, session_scope in trigger_list:
                if len(top_summary_pool) >= target_accumulation_size: break
                t_hits, _ = get_custom_target_hits(trig_search, session_scope, st.session_state.full_draws, st.session_state.day_pairs)
                
                for p in priorities:
                    if len(top_summary_pool) >= target_accumulation_size: break
                    trend_req, size_req = p['trend'], p['size']
                    if len(t_hits) < trend_req: continue 
                    
                    recent_A = t_hits[-trend_req:]
                    b_sets = [set([d['draw'] for d in st.session_state.full_draws[h['index'] + 1 : min(h['index'] + 1 + chain_span1, len(st.session_state.full_draws))]]) for h in recent_A]
                    common_b = set.intersection(*b_sets) if b_sets else set()
                    
                    if common_b:
                        b_flat = [d['draw'] for h in recent_A for d in st.session_state.full_draws[h['index'] + 1 : min(h['index'] + 1 + chain_span1, len(st.session_state.full_draws))] if d['draw'] in common_b]
                        top_b = [x[0] for x in Counter(b_flat).most_common(size_req)]
                        
                        last_a_idx = recent_A[-1]['index']
                        elapsed_b = (len(st.session_state.full_draws) - 1) - last_a_idx
                        
                        if 0 < elapsed_b <= chain_span1:
                            already_hit_b = any(d['draw'] in top_b for d in st.session_state.full_draws[last_a_idx + 1 : len(st.session_state.full_draws)])
                            if not already_hit_b:
                                b_str = " ".join(top_b)
                                sig_key = f"T1_{trig_search}_{b_str}"
                                new_nums = set(top_b) - top_summary_pool
                                
                                if sig_key not in used_signatures and new_nums:
                                    used_signatures.add(sig_key)
                                    top_summary_pool.update(top_b)
                                    msg = f"""
<div style="background-color: #170E2B; padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 6px solid #3498db; border: 1px solid #2D1B4E;">
<div style="color:#00FFCC; font-size:16px; font-weight:bold; margin-bottom:12px;">💎 100% Strict Chain [Rank Score: {p['score']}] | Trend: {trend_req} ကြိမ် | Size: {len(top_b)} ကွက်</div>
<div style="color:#E0D5FA; margin-bottom:12px; font-size:15px; border-bottom: 1px dashed #4A3B69; padding-bottom: 10px;">
    <b>A ➡️ B:</b> [{trig_display}] ထွက်ပြီးတိုင်း ({chain_span1}) ပွဲအတွင်း <span style="color:#FFD700; font-weight:bold;">{b_str}</span> ဒဲ့ 100%
</div>
<div style="color:#e74c3c; font-weight:bold; margin-bottom:8px; font-size:15px;">🔥 LIVE SIGNAL</div>
<div style="color:#A294C7; font-size:14px;">လတ်တလော A ဝင်ထား၍ ယခုပွဲစဉ်တွင် အထက်ပါ {len(top_b)} ကွက်အား ထိုးပါ။</div>
</div>
"""
                                    live_signals_results.append(msg)
                                    if len(top_summary_pool) >= target_accumulation_size: break

            if top_summary_pool:
                st.markdown("### 🎯 ယခုပွဲစဉ်အတွက် ထိုးရမည့် ဂဏန်းများ (Summary)")
                badges_summary = " ".join([f"<span style='background-color:#FFD700; color:#000000; padding:8px 16px; border-radius:8px; font-size:20px; font-weight:bold; margin-right:8px; margin-bottom:8px; display:inline-block;'>{n}</span>" for n in sorted(top_summary_pool)])
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1e0a3c 0%, #0B031A 100%); padding: 20px; border-radius: 12px; margin-bottom: 25px; border: 2px solid #A078FF; text-align: center;">
                    <div style="color:#E0D5FA; font-size:16px; margin-bottom:15px;">စုစုပေါင်း ({len(top_summary_pool)}) ကွက် ထိုးရန်ရှိပါသည်-</div>
                    <div>{badges_summary}</div>
                </div>
                """, unsafe_allow_html=True)
                for html_msg in live_signals_results: st.markdown(html_msg, unsafe_allow_html=True)
            else:
                st.info("⚠️ ယခုအချိန်တွင် သတ်မှတ်စည်းမျဉ်းနှင့် ကိုက်ညီပြီး အသက်ဝင်နေသော ရက်ချိန်းပြည့် (Live Signal) များ မတွေ့ရှိပါ။")
