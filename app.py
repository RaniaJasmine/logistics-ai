import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import requests

st.set_page_config(page_title="Logistics AI", layout="wide", initial_sidebar_state="expanded")

# ==================== MEGA CSS (full design from first code) ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:opsz,wght@9..40,300;400;500;600&display=swap');

*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior: smooth; }
body, .stApp { font-family: 'DM Sans', sans-serif; }

/* ── BACKGROUND ──────────────────────────────────── */
.stApp {
    background:
        radial-gradient(ellipse 80% 60% at 10% 5%,  rgba(30,70,160,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 80%,  rgba(20,50,130,0.14) 0%, transparent 55%),
        radial-gradient(ellipse 70% 70% at 50% 50%,  rgba(5,12,30,1) 0%, #020813 100%);
    background-attachment: fixed;
    overflow-x: hidden;
}

/* ── MOVING GRID ─────────────────────────────────── */
.stApp::after {
    content: "";
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(60,120,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(60,120,255,0.03) 1px, transparent 1px);
    background-size: 55px 55px;
    pointer-events: none;
    animation: gridDrift 45s linear infinite;
    z-index: 0;
}
@keyframes gridDrift {
    0%   { background-position: 0 0; }
    100% { background-position: 55px 55px; }
}

/* ── AMBIENT ORBS ────────────────────────────────── */
.stApp::before {
    content: "";
    position: fixed; top: -120px; left: -150px; width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(35,90,210,0.18), transparent 68%);
    border-radius: 50%; pointer-events: none;
    animation: orbFloat 24s ease-in-out infinite alternate; z-index: 0;
}
@keyframes orbFloat {
    0%   { transform: translate(0,0) scale(1); opacity:0.7; }
    33%  { transform: translate(90px,70px) scale(1.12); opacity:1; }
    66%  { transform: translate(-50px,120px) scale(0.93); opacity:0.8; }
    100% { transform: translate(70px,-50px) scale(1.06); opacity:0.9; }
}

/* secondary orb via JS injection below */
.orb-b {
    position: fixed; bottom: -80px; right: -100px; width: 450px; height: 450px;
    background: radial-gradient(circle, rgba(25,70,190,0.15), transparent 70%);
    border-radius: 50%; pointer-events: none; filter: blur(60px);
    animation: orbFloat2 30s ease-in-out infinite alternate; z-index: 0;
}
@keyframes orbFloat2 {
    0%   { transform: translate(0,0) scale(1); }
    50%  { transform: translate(-80px,-90px) scale(1.18); }
    100% { transform: translate(60px,50px) scale(0.88); }
}
.orb-c {
    position: fixed; top: 48%; left: 38%; width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(50,120,255,0.1), transparent 72%);
    border-radius: 50%; pointer-events: none; filter: blur(70px);
    animation: orbFloat3 20s ease-in-out infinite alternate; z-index: 0;
}
@keyframes orbFloat3 {
    0%   { transform: translate(0,0) scale(1); opacity:0.5; }
    50%  { transform: translate(70px,-60px) scale(1.25); opacity:0.9; }
    100% { transform: translate(-50px,70px) scale(0.82); opacity:0.6; }
}

/* ── SIDEBAR ─────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(3,8,20,0.97) 0%, rgba(5,12,26,0.95) 100%);
    backdrop-filter: blur(40px) saturate(1.7);
    border-right: 1px solid rgba(55,110,230,0.16);
    box-shadow: 14px 0 55px rgba(0,0,0,0.75), inset -1px 0 0 rgba(70,130,255,0.05);
    animation: sideIn 0.75s cubic-bezier(0.22,1,0.36,1) both;
    transition: border-color 0.5s, box-shadow 0.5s;
}
@keyframes sideIn {
    from { transform: translateX(-28px); opacity:0; }
    to   { transform: translateX(0); opacity:1; }
}
[data-testid="stSidebar"]:hover {
    border-right-color: rgba(75,135,255,0.3);
    box-shadow: 18px 0 65px rgba(0,0,0,0.8), inset -1px 0 0 rgba(75,135,255,0.1);
}

/* ── HERO ────────────────────────────────────────── */
.hero-wrap {
    position: relative; padding: 0.4rem 0 0.15rem;
    animation: heroReveal 1s cubic-bezier(0.22,1,0.36,1) 0.05s both;
}
@keyframes heroReveal {
    from { opacity:0; transform: translateY(-22px); }
    to   { opacity:1; transform: translateY(0); }
}
.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem; font-weight: 800;
    background: linear-gradient(115deg, #ffffff 0%, #cce0ff 30%, #7ab0ff 60%, #4a80e8 100%);
    background-size: 300% auto;
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: titleShimmer 4.5s linear infinite;
    letter-spacing: -0.02em; line-height: 1.1; display: inline-block;
}
@keyframes titleShimmer {
    0%   { background-position: 0% center; }
    100% { background-position: 300% center; }
}

.float-icon {
    display: inline-block;
    color: #fff !important; -webkit-text-fill-color: white !important;
    text-shadow: 0 0 22px rgba(100,165,255,0.55) !important;
    animation: truckBounce 5s ease-in-out infinite;
}
@keyframes truckBounce {
    0%,100% { transform: translateY(0) rotate(0deg); }
    18%      { transform: translateY(-9px) rotate(-1.8deg); }
    36%      { transform: translateY(-4px) rotate(0.8deg); }
    54%      { transform: translateY(-11px) rotate(-1.2deg); }
    72%      { transform: translateY(-2px) rotate(1.2deg); }
    88%      { transform: translateY(-7px) rotate(-0.6deg); }
}

/* ── SUBTITLE typewriter ─────────────────────────── */
.subtitle {
    font-size: 0.9rem; font-weight: 300; letter-spacing: 0.09em;
    color: #628ab8; margin-bottom: 2rem; padding-left: 0.2rem;
    white-space: nowrap; overflow: hidden;
    border-right: 2px solid #3a6aaa; width: 0;
    animation: typeIt 2.6s steps(50, end) 0.6s forwards,
               blinkIt 0.9s step-end infinite 0.6s;
}
@keyframes typeIt  { from{width:0;} to{width:100%;} }
@keyframes blinkIt { from,to{border-color:transparent;} 50%{border-color:#3a6aaa;} }

/* ── SECTION LABELS ──────────────────────────────── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.6rem; font-weight: 700; letter-spacing: 3.5px;
    text-transform: uppercase; color: #2e5a9a;
    margin: 1.8rem 0 0.85rem;
    display: flex; align-items: center; gap: 0.9rem;
    animation: labelIn 0.7s ease both;
}
.section-label::after {
    content: "";
    flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(46,90,154,0.55), transparent);
    animation: lineExpand 1s ease both 0.35s;
    transform-origin: left;
}
@keyframes labelIn    { from{opacity:0;transform:translateX(-12px);} to{opacity:1;transform:translateX(0);} }
@keyframes lineExpand { from{transform:scaleX(0);} to{transform:scaleX(1);} }
.sl-1 { animation-delay:0.10s; }
.sl-2 { animation-delay:0.20s; }
.sl-3 { animation-delay:0.30s; }
.sl-4 { animation-delay:0.40s; }

/* ── METRIC CARDS ────────────────────────────────── */
.metric-card {
    position: relative; overflow: hidden;
    background: linear-gradient(148deg, rgba(9,17,34,0.84), rgba(4,10,24,0.92));
    backdrop-filter: blur(26px) saturate(1.5);
    border-radius: 1.5rem;
    padding: 0.85rem 0.5rem;
    text-align: center;
    border: 1px solid rgba(55,105,215,0.2);
    min-height: 100px; display: flex; flex-direction: column; justify-content: center;
    box-shadow:
        0 8px 26px rgba(0,0,0,0.48),
        inset 0 1px 0 rgba(255,255,255,0.045),
        inset 0 -1px 0 rgba(0,0,0,0.25);
    transition:
        transform      0.42s cubic-bezier(0.2,0.9,0.4,1.1),
        box-shadow     0.42s ease,
        border-color   0.42s ease,
        background     0.42s ease;
    animation: cardPop 0.65s cubic-bezier(0.2,0.9,0.4,1.1) both;
    cursor: default;
}
.metric-card:nth-child(1){animation-delay:0.05s;}
.metric-card:nth-child(2){animation-delay:0.11s;}
.metric-card:nth-child(3){animation-delay:0.17s;}
.metric-card:nth-child(4){animation-delay:0.23s;}
.metric-card:nth-child(5){animation-delay:0.29s;}
.metric-card:nth-child(6){animation-delay:0.35s;}
@keyframes cardPop {
    0%   { opacity:0; transform: translateY(42px) scale(0.91); }
    55%  { transform: translateY(-5px) scale(1.02); }
    100% { opacity:1; transform: translateY(0) scale(1); }
}

/* continuous shimmer sweep across card */
.metric-card::before {
    content:"";
    position:absolute; top:0; left:-90%; width:55%; height:100%;
    background: linear-gradient(100deg,
        transparent 0%, rgba(110,170,255,0.065) 50%, transparent 100%);
    transform: skewX(-18deg);
    animation: sweepCard 4.5s ease-in-out infinite;
}
.metric-card:nth-child(2)::before{animation-delay:0.45s;}
.metric-card:nth-child(3)::before{animation-delay:0.9s;}
.metric-card:nth-child(4)::before{animation-delay:1.35s;}
.metric-card:nth-child(5)::before{animation-delay:1.8s;}
.metric-card:nth-child(6)::before{animation-delay:2.25s;}
@keyframes sweepCard{
    0%,100%{ left:-90%; }
    50%    { left:150%; }
}

/* top-edge glow */
.metric-card::after {
    content:"";
    position:absolute; top:0; left:12%; right:12%; height:1px;
    background: linear-gradient(90deg, transparent, rgba(90,155,255,0.55), transparent);
    animation: edgePulse 3.5s ease-in-out infinite alternate;
}
.metric-card:nth-child(2)::after{animation-delay:0.55s;}
.metric-card:nth-child(3)::after{animation-delay:1.1s;}
.metric-card:nth-child(4)::after{animation-delay:1.65s;}
@keyframes edgePulse{
    from{ opacity:0.3; transform:scaleX(0.65); }
    to  { opacity:1;   transform:scaleX(1); }
}

.metric-card:hover {
    transform: translateY(-9px) scale(1.045);
    border-color: rgba(85,148,255,0.52);
    box-shadow:
        0 26px 52px rgba(0,0,0,0.62),
        0 0 0 1px rgba(75,135,255,0.16),
        0 0 32px rgba(55,115,255,0.13),
        inset 0 1px 0 rgba(255,255,255,0.08);
    background: linear-gradient(148deg, rgba(14,26,52,0.9), rgba(7,16,36,0.96));
}

.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.08rem; font-weight: 700;
    background: linear-gradient(128deg, #ffffff, #cce0ff);
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.15rem 0; letter-spacing: -0.3px; line-height: 1.3;
    animation: valBreath 4.5s ease-in-out infinite;
}
@keyframes valBreath{
    0%,100%{ opacity:0.86; }
    50%    { opacity:1; }
}
.metric-label {
    font-size: 0.49rem; text-transform: uppercase; letter-spacing: 2px;
    color: #3e70b8; font-weight: 600; line-height: 1.2; margin-bottom: 0.25rem;
}

/* ── CHART CARDS ─────────────────────────────────── */
.chart-card {
    position: relative; overflow: hidden;
    background: linear-gradient(158deg, rgba(7,14,30,0.9), rgba(3,9,20,0.94));
    backdrop-filter: blur(30px) saturate(1.6);
    border-radius: 2rem; padding: 1.8rem;
    border: 1px solid rgba(45,95,205,0.18);
    box-shadow:
        0 18px 44px rgba(0,0,0,0.52),
        inset 0 1px 0 rgba(255,255,255,0.038);
    margin-bottom: 1.8rem;
    animation: chartUp 0.85s cubic-bezier(0.22,1,0.36,1) both;
    transition: transform 0.38s ease, box-shadow 0.38s ease;
}
@keyframes chartUp {
    from{ opacity:0; transform: translateY(35px) scale(0.965); }
    to  { opacity:1; transform: translateY(0) scale(1); }
}

/* scanning top-line */
.chart-card::before {
    content:"";
    position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg,
        transparent 0%, rgba(65,125,255,0.65) 35%,
        rgba(120,185,255,0.9) 50%,
        rgba(65,125,255,0.65) 65%, transparent 100%);
    background-size: 220% auto;
    animation: scannerLine 3.2s linear infinite;
    border-radius: 2rem 2rem 0 0;
}
@keyframes scannerLine{
    0%  { background-position: -100% center; }
    100%{ background-position: 220% center; }
}
/* inner glow corners */
.chart-card::after {
    content:"";
    position:absolute; inset:0;
    background:
        radial-gradient(circle at 0% 0%, rgba(60,115,255,0.06) 0%, transparent 45%),
        radial-gradient(circle at 100% 100%, rgba(40,95,215,0.05) 0%, transparent 45%);
    border-radius: 2rem; pointer-events:none;
    animation: cornerBreath 6s ease-in-out infinite alternate;
}
@keyframes cornerBreath{
    from{ opacity:0.5; }
    to  { opacity:1; }
}
.chart-card:hover {
    transform: translateY(-5px);
    box-shadow:
        0 30px 65px rgba(0,0,0,0.62),
        0 0 0 1px rgba(65,125,255,0.13),
        0 0 45px rgba(45,105,255,0.09);
}

/* stagger chart cards */
.cc-1{ animation-delay:0.1s; }
.cc-2{ animation-delay:0.2s; }
.cc-3{ animation-delay:0.3s; }
.cc-4{ animation-delay:0.4s; }
.cc-5{ animation-delay:0.5s; }

/* ── BUTTONS ─────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(138deg, #0c1d38 0%, #07101e 100%) !important;
    color: #b0ccf0 !important;
    border: 1px solid rgba(55,105,215,0.32) !important;
    border-radius: 3rem !important;
    padding: 0.72rem 2.2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important; font-size: 0.87rem !important;
    letter-spacing: 0.055em !important;
    transition: all 0.32s cubic-bezier(0.2,0.9,0.4,1.1) !important;
    width: 100% !important;
    animation: btnPulse 2.8s ease-in-out infinite !important;
    position: relative; overflow: hidden !important;
}
@keyframes btnPulse{
    0%,100%{ box-shadow: 0 4px 18px rgba(0,0,0,0.42); }
    50%    { box-shadow: 0 4px 28px rgba(0,0,0,0.42), 0 0 22px 3px rgba(55,110,220,0.32); }
}
.stButton > button:hover {
    transform: translateY(-4px) scale(1.015) !important;
    background: linear-gradient(138deg, #152c52 0%, #0c1d38 100%) !important;
    border-color: rgba(85,150,255,0.62) !important;
    box-shadow: 0 14px 36px rgba(40,88,220,0.32), 0 0 0 1px rgba(80,140,255,0.18) !important;
    color: #d0e6ff !important;
    letter-spacing: 0.07em !important;
}
.stButton > button:active{
    transform: translateY(0) scale(0.97) !important;
    transition: all 0.09s !important;
}

/* ── SLIDERS ─────────────────────────────────────── */
.stSlider label{ color:#6a9ed8 !important; font-size:0.81rem !important; letter-spacing:0.02em; }
.stSlider [role="slider"]{
    background: #4a85e8 !important;
    box-shadow: 0 0 16px rgba(74,133,232,0.75), 0 0 5px rgba(74,133,232,1) !important;
    transition: box-shadow 0.3s, transform 0.2s !important;
}
.stSlider [role="slider"]:hover{
    box-shadow: 0 0 26px rgba(74,133,232,1), 0 0 8px rgba(74,133,232,1) !important;
    transform: scale(1.18) !important;
}

/* ── SELECT / INPUT ──────────────────────────────── */
.stSelectbox label,.stTextInput label{ color:#6a9ed8 !important; font-size:0.81rem !important; }
div[data-baseweb="select"] > div {
    background: rgba(6,12,26,0.85) !important;
    border: 1px solid rgba(50,100,205,0.28) !important;
    border-radius: 0.85rem !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}
div[data-baseweb="select"] > div:hover{
    border-color: rgba(75,140,255,0.52) !important;
    box-shadow: 0 0 14px rgba(55,110,255,0.14) !important;
}
.stTextInput > div > div > input{
    background: rgba(6,12,26,0.85) !important;
    border: 1px solid rgba(50,100,205,0.28) !important;
    border-radius: 0.85rem !important; color:#b8d4f4 !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}
.stTextInput > div > div > input:focus{
    border-color: rgba(75,140,255,0.6) !important;
    box-shadow: 0 0 18px rgba(55,110,255,0.22) !important;
}

/* ── TABS ────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"]{
    background: rgba(4,10,22,0.65) !important;
    border-radius: 1.1rem !important; padding: 0.32rem !important;
    border: 1px solid rgba(45,95,200,0.18) !important; gap:0.2rem;
}
.stTabs [data-baseweb="tab"]{
    border-radius: 0.75rem !important; color:#4a7ec0 !important;
    transition: all 0.3s ease !important;
    font-family:'DM Sans',sans-serif !important; font-weight:500 !important;
}
.stTabs [aria-selected="true"]{
    background: linear-gradient(135deg, #0c1f3e, #081428) !important;
    color:#b8d4f4 !important;
    box-shadow: 0 2px 14px rgba(38,88,200,0.38), inset 0 1px 0 rgba(255,255,255,0.055) !important;
}

/* ── DATAFRAME ───────────────────────────────────── */
.stDataFrame{ animation: chartUp 0.8s ease both; }
.stDataFrame table{
    background: rgba(5,10,22,0.75) !important;
    border-radius: 1.3rem !important; backdrop-filter: blur(14px) !important; overflow:hidden;
}
.stDataFrame th{
    background: rgba(18,42,90,0.65) !important;
    color:#7aaed8 !important;
    font-family:'Syne',sans-serif !important;
    font-size:0.7rem !important; letter-spacing:0.09em !important;
}
.stDataFrame td{ color:#a8c8e4 !important; font-size:0.84rem !important; }
.stDataFrame tr{ transition: background 0.22s !important; }
.stDataFrame tr:hover td{
    background: rgba(28,58,120,0.28) !important;
    color:#ccdffa !important;
}

/* ── ALERTS / SUCCESS ────────────────────────────── */
div[data-baseweb="notification"]{
    background: linear-gradient(135deg, rgba(10,25,60,0.78), rgba(5,14,38,0.88)) !important;
    border: 1px solid rgba(55,105,215,0.32) !important;
    border-left: 3px solid #4a80e0 !important;
    border-radius: 1.2rem !important;
    color:#b8d4f4 !important;
    backdrop-filter: blur(18px) !important;
    box-shadow: 0 8px 26px rgba(0,0,0,0.42) !important;
    animation: alertIn 0.55s cubic-bezier(0.22,1,0.36,1) both !important;
}
@keyframes alertIn{
    from{ opacity:0; transform: translateY(14px) scale(0.97); }
    to  { opacity:1; transform: translateY(0) scale(1); }
}

/* ── AI ADVICE ───────────────────────────────────── */
.ai-advice{
    background: linear-gradient(148deg, rgba(8,20,48,0.55), rgba(4,12,32,0.65));
    backdrop-filter: blur(30px);
    border-radius: 1.85rem; padding: 1.65rem;
    border: 1px solid rgba(55,105,215,0.32);
    box-shadow:
        0 14px 36px rgba(0,0,0,0.48),
        inset 0 1px 0 rgba(255,255,255,0.038);
    margin-top: 1.25rem;
    animation: chartUp 0.8s cubic-bezier(0.22,1,0.36,1) both;
    color:#b0ccee; line-height:1.75;
}

/* ── PERF BOX ────────────────────────────────────── */
.perf-box{
    background: linear-gradient(148deg, rgba(10,24,58,0.52), rgba(5,14,36,0.62));
    border: 1px solid rgba(50,100,210,0.28);
    border-radius: 1.5rem; padding: 1.25rem 1.6rem;
    margin-top: 1.25rem; text-align:center;
    color:#b0ccf0; line-height:1.85;
    box-shadow: 0 10px 28px rgba(0,0,0,0.38);
    animation: chartUp 0.7s ease both 0.35s;
    position:relative; overflow:hidden;
}
.perf-box::before{
    content:"";
    position:absolute; top:0; left:0; right:0; height:1.5px;
    background: linear-gradient(90deg,
        transparent, rgba(85,150,255,0.65), transparent);
    background-size: 200% auto;
    animation: scannerLine 2.8s linear infinite;
}

/* ── LIVE DOT ────────────────────────────────────── */
.live-dot{
    display:inline-block; width:7px; height:7px; border-radius:50%;
    background:#4a9eff; margin-right:5px; vertical-align:middle;
    box-shadow: 0 0 0 0 rgba(74,158,255,0.65);
    animation: livePing 2s ease-in-out infinite;
}
@keyframes livePing{
    0%  { box-shadow: 0 0 0 0 rgba(74,158,255,0.65); }
    65% { box-shadow: 0 0 0 9px rgba(74,158,255,0); }
    100%{ box-shadow: 0 0 0 0 rgba(74,158,255,0); }
}

/* ── SPINNER ─────────────────────────────────────── */
.stSpinner > div{ border-top-color:#4a85e8 !important; }

/* ── SCROLLBAR ───────────────────────────────────── */
::-webkit-scrollbar{ width:4px; background:#03070f; }
::-webkit-scrollbar-thumb{
    background: linear-gradient(180deg, #16325e, #0c1e3c);
    border-radius:10px;
}
::-webkit-scrollbar-thumb:hover{ background:#22468a; }

/* ── SIDEBAR BRAND ───────────────────────────────── */
.sidebar-brand{
    font-family:'Syne',sans-serif;
    font-size:1.18rem; font-weight:800;
    background: linear-gradient(115deg, #ffffff, #88b8e8);
    background-size: 300% auto;
    -webkit-background-clip:text; background-clip:text;
    -webkit-text-fill-color:transparent;
    animation: titleShimmer 5.5s linear infinite; letter-spacing:0.025em;
}
.sidebar-sub{
    font-size:0.63rem; color:#2e5585; letter-spacing:0.18em;
    text-transform:uppercase; margin-top:0.12rem;
    animation: chartUp 0.7s ease both 0.35s;
}

/* ── FOOTER ──────────────────────────────────────── */
.footer{
    text-align:center; margin-top:3.2rem; padding:1.5rem 0;
    border-top: 1px solid rgba(40,90,195,0.1);
    color:#264870; font-size:0.67rem; letter-spacing:0.12em;
    animation: chartUp 1s ease both 0.6s;
}
.footer span{
    background: linear-gradient(90deg, #305888, #4a80b8);
    -webkit-background-clip:text; background-clip:text;
    -webkit-text-fill-color:transparent;
}

/* ── MISC ────────────────────────────────────────── */
hr{ border:none !important; border-top:1px solid rgba(40,90,195,0.12) !important; margin:1rem 0 !important; }
h2,h3,.stSubheader{ font-family:'Syne',sans-serif !important; color:#7aaed8 !important; letter-spacing:0.01em !important; }
.stMarkdown p{ color:#7aacda; line-height:1.72; }
.stMarkdown strong{ color:#b8d4f4; }
.stMarkdown a{ color:#5890d8; transition:color 0.25s; }
.stMarkdown a:hover{ color:#78aaf0; }
.stCaption{ color:#2e5585 !important; font-size:0.72rem !important; }
</style>
""", unsafe_allow_html=True)

# inject extra orbs
st.markdown("""
<div class="orb-b"></div>
<div class="orb-c"></div>
""", unsafe_allow_html=True)

# ==================== CURRENCY & DATA FUNCTIONS ====================
currency_symbols = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹", "JPY": "¥"}
currency_rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "INR": 83.5, "JPY": 149.5}

def convert_currency(amount_usd, currency):
    return amount_usd * currency_rates[currency]

def fmt_currency(amount_usd, currency):
    converted = convert_currency(amount_usd, currency)
    sym = currency_symbols[currency]
    if currency == "JPY":
        return f"{sym}{int(converted):,}"
    elif currency == "INR":
        return f"{sym}{converted:,.0f}"
    else:
        return f"{sym}{converted:,.2f}"

@st.cache_data
def generate_base_demand(region):
    start_date = datetime(2025, 10, 1)
    end_date   = datetime(2026, 3, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    base_demand = {"North America": 500, "Europe": 450, "Asia": 700,
                   "South America": 400, "Africa": 350, "Australia": 300}
    base = base_demand.get(region, 500)
    day_of_year = dates.dayofyear
    if region == "North America":
        season = np.where((day_of_year <= 60) | (day_of_year >= 305), 1.4, 1.0)
    elif region == "Europe":
        season = np.where((day_of_year <= 75) | (day_of_year >= 290), 1.3, 1.0)
    elif region == "Asia":
        season = np.where((day_of_year >= 150) & (day_of_year <= 240), 1.25, 1.0)
        season = np.where((day_of_year >= 274) & (day_of_year <= 365), 1.15, season)
    elif region == "South America":
        season = np.where((day_of_year >= 335) | (day_of_year <= 60), 1.35, 1.0)
    elif region == "Africa":
        season = np.where((day_of_year >= 274) & (day_of_year <= 365), 1.2, 1.0)
    else:
        season = np.where((day_of_year >= 274) & (day_of_year <= 365), 1.3, 1.0)
    weekly = [1.0, 1.0, 1.0, 1.0, 1.25, 1.35, 1.15] * (len(dates) // 7 + 1)
    weekly = weekly[:len(dates)]
    noise  = np.random.normal(1.0, 0.1, len(dates))
    demand = (base * season * weekly * noise).astype(int)
    return pd.DataFrame({"Date": dates, "Original_Demand": demand})

def apply_disruptions(df, port_days, supplier_delay):
    df = df.copy()
    df["Effective_Demand"] = df["Original_Demand"].copy()
    closure_start_idx = len(df) // 2
    closure_end_idx   = min(closure_start_idx + port_days, len(df))
    if port_days > 0:
        affected = df.iloc[closure_start_idx:closure_end_idx]["Original_Demand"] * 0.2
        df.iloc[closure_start_idx:closure_end_idx, df.columns.get_loc("Effective_Demand")] = affected.astype(int)
    delay_start_idx = closure_start_idx + 20
    if supplier_delay > 0:
        spike_start = min(delay_start_idx + supplier_delay, len(df) - 1)
        spike_end   = min(spike_start + 10, len(df))
        if spike_start < len(df):
            spike_vals = df.iloc[spike_start:spike_end]["Original_Demand"] * 2.0
            df.iloc[spike_start:spike_end, df.columns.get_loc("Effective_Demand")] = spike_vals.astype(int)
    df["Effective_Demand"] = df["Effective_Demand"].clip(lower=1)
    return df

def add_forecast(df, window=7):
    df["Forecast"] = df["Effective_Demand"].rolling(window=window, min_periods=1).mean()
    return df

def hierarchical_forecast(df, region):
    np.random.seed(42)
    region_multiplier = {"North America": 3.2, "Europe": 2.8, "Asia": 4.5,
                         "South America": 2.0, "Africa": 1.5, "Australia": 1.0}
    scale       = region_multiplier.get(region, 2.0)
    extra_noise = np.random.normal(1.0, 0.05, len(df))
    national_demand   = (df["Effective_Demand"] * scale * extra_noise).astype(int)
    national_forecast = (df["Forecast"] * scale * extra_noise).astype(int)
    national_df  = pd.DataFrame({"Date": df["Date"], "Demand": national_demand, "Forecast": national_forecast})
    regional_df  = df[["Date", "Effective_Demand", "Forecast"]].rename(columns={"Effective_Demand": "Demand"})
    warehouse_props  = [0.4, 0.35, 0.25]
    warehouse_melted = pd.DataFrame()
    for i, prop in enumerate(warehouse_props):
        wh_demand   = (df["Effective_Demand"] * prop).astype(int)
        wh_forecast = (df["Forecast"] * prop).astype(int)
        temp = pd.DataFrame({"Date": df["Date"], "Demand": wh_demand,
                              "Forecast": wh_forecast, "Warehouse": f"WH-{i+1}"})
        warehouse_melted = pd.concat([warehouse_melted, temp])
    return national_df, regional_df, warehouse_melted

def improved_route_recommendation(port_days, supplier_delay, co2_weight=0.3, cost_weight=0.5, time_weight=0.2):
    routes = [
        {"name": "🚢 Sea Freight",  "cost": 5000,  "co2": 200, "time_days": 12, "base_lead_time": 12},
        {"name": "🚂 Rail Freight", "cost": 6500,  "co2": 80,  "time_days": 8,  "base_lead_time": 8},
        {"name": "✈️ Air Freight",  "cost": 15000, "co2": 500, "time_days": 2,  "base_lead_time": 2},
        {"name": "🚛 Truck+Rail",   "cost": 7200,  "co2": 120, "time_days": 7,  "base_lead_time": 7},
        {"name": "🚢 Express Sea",  "cost": 6800,  "co2": 220, "time_days": 8,  "base_lead_time": 8},
    ]
    if port_days > 0:
        for r in routes:
            if "Sea" in r["name"]:
                r["time_days"] = r["base_lead_time"] + min(port_days, 10)
    if supplier_delay > 0:
        for r in routes:
            r["time_days"] = r["time_days"] + min(supplier_delay // 5, 3)
    max_cost = max(r["cost"]     for r in routes)
    max_co2  = max(r["co2"]      for r in routes)
    max_time = max(r["time_days"] for r in routes)
    for r in routes:
        norm_cost = r["cost"]     / max_cost
        norm_co2  = r["co2"]      / max_co2
        norm_time = r["time_days"] / max_time
        r["score"] = (cost_weight * norm_cost) + (co2_weight * norm_co2) + (time_weight * norm_time)
    if port_days > 3:
        for r in routes:
            if "Sea" in r["name"]:
                r["score"] += 0.3
    best = min(routes, key=lambda x: x["score"])
    return best, routes

def calculate_safety_stock(df, lead_time_days=7):
    avg_daily = df["Effective_Demand"].mean()
    max_daily = df["Effective_Demand"].max()
    safety_stock = (max_daily * lead_time_days) - (avg_daily * lead_time_days)
    return max(0, int(safety_stock))

def calculate_kpis(df):
    total_demand   = df["Effective_Demand"].sum()
    total_forecast = df["Forecast"].sum()
    service_level  = min(100, (total_forecast / total_demand) * 100) if total_demand > 0 else 100
    total_cost     = (total_demand * 10) + 5000
    co2            = total_demand * 0.5
    return round(service_level, 1), int(total_cost), int(co2)

def baseline_reorder_point(df, reorder_point=500):
    inventory   = 1000
    orders      = []
    stockouts   = 0
    daily_demand = df["Effective_Demand"].values
    for demand in daily_demand:
        if inventory < reorder_point:
            order_qty = 800
            orders.append(order_qty)
            inventory += order_qty
        else:
            orders.append(0)
        if demand > inventory:
            stockouts += 1
            inventory  = 0
        else:
            inventory -= demand
    total_baseline_cost = sum(orders) * 10 + 5000
    service_level_baseline = 100 - (stockouts / len(daily_demand)) * 100
    return service_level_baseline, total_baseline_cost

def get_groq_advice(api_key, region, port_days, supplier_delay, safety_stock,
                    service_level, total_cost, co2, best_route):
    url     = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    prompt  = f"""You are a supply chain AI. Given:
Region: {region}
Port closure: {port_days} days
Supplier delay: {supplier_delay} days
Safety stock: {safety_stock} units
Service level: {service_level}%
Total cost (USD): ${total_cost:,}
CO₂: {co2} kg
Optimal route: {best_route['name']} (${best_route['cost']}, {best_route['co2']}kg, {best_route['time_days']} days)

Provide 3-5 bullet points of actionable advice to improve cost, service level, or CO₂."""
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 300,
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ API error: {response.status_code}"
    except Exception as e:
        return f"⚠️ Could not fetch AI advice: {str(e)}"

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">✦ Logistics AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Intelligence Platform v2</div>', unsafe_allow_html=True)
    st.markdown("---")
    region   = st.selectbox("📍 Region", ["North America", "Europe", "Asia", "South America", "Africa", "Australia"])
    currency = st.selectbox("💱 Currency", list(currency_symbols.keys()), index=0)
    st.markdown("### 🌊 Disruption Simulator")
    port_days       = st.slider("🚢 Port Closure (days)", 0, 14, 3)
    supplier_delay  = st.slider("🏭 Supplier Delay (days)", 0, 21, 5)
    st.markdown("---")
    groq_key = st.text_input("🤖 Groq API Key", type="password", help="Free from console.groq.com")

# ==================== MAIN UI ====================
st.markdown("""
<div class="hero-wrap">
  <div class="main-title"><span class="float-icon">🚚</span> AI‑Enhanced Logistics Optimizer</div>
</div>""", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real‑time supply chain intelligence · disruption resilience · global routing</div>', unsafe_allow_html=True)

# data pipeline
df_base = generate_base_demand(region)
df = apply_disruptions(df_base, port_days, supplier_delay)
df = add_forecast(df)

nat_df, reg_df, wh_df = hierarchical_forecast(df, region)
safety_stock = calculate_safety_stock(df)
service_level, total_cost_usd, co2 = calculate_kpis(df)
best_route, all_routes = improved_route_recommendation(port_days, supplier_delay)

# currency helpers
rate = currency_rates[currency]

# ── KPI ROW (custom cards) ──
st.markdown('<div class="section-label sl-1">◆ Live Dashboard</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.markdown('<div class="metric-card"><div class="metric-label">📦 PRODUCT</div><div class="metric-value">Brake Pads</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">📍 REGION</div><div class="metric-value">{region}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">🚢 PORT CLOSURE</div><div class="metric-value">{port_days} days</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">⏱ SUPPLIER DELAY</div><div class="metric-value">{supplier_delay} days</div></div>', unsafe_allow_html=True)
with c5:
    st.markdown(f'<div class="metric-card"><div class="metric-label">🛡 SAFETY STOCK</div><div class="metric-value">{safety_stock:,} units</div></div>', unsafe_allow_html=True)
with c6:
    st.markdown(f'<div class="metric-card"><div class="metric-label">📊 SERVICE LEVEL</div><div class="metric-value">{service_level}%</div></div>', unsafe_allow_html=True)

cA, cB = st.columns(2)
with cA:
    st.markdown(f'<div class="metric-card"><div class="metric-label">💰 TOTAL COST</div><div class="metric-value">{fmt_currency(total_cost_usd, currency)}</div></div>', unsafe_allow_html=True)
with cB:
    st.markdown(f'<div class="metric-card"><div class="metric-label"><span class="live-dot"></span>CO₂ EMISSIONS</div><div class="metric-value">{co2:,} kg</div></div>', unsafe_allow_html=True)

# ── HIERARCHICAL CHARTS ──
st.markdown('<div class="section-label sl-2">◆ Demand Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card cc-1">', unsafe_allow_html=True)
st.subheader("📊 Hierarchical Demand & Forecast")
t1, t2, t3 = st.tabs(["🌎 National", "📍 Regional", "🏭 Warehouses"])
_chart_layout = dict(
    height=430,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#7aacda"),
    xaxis=dict(gridcolor="rgba(45,95,200,0.09)", showline=False, zeroline=False),
    yaxis=dict(gridcolor="rgba(45,95,200,0.09)", showline=False, zeroline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(45,95,200,0.18)"),
    margin=dict(t=42, b=22, l=14, r=14),
    hoverlabel=dict(bgcolor="rgba(8,18,40,0.92)", bordercolor="rgba(65,125,255,0.4)", font_color="#cce0ff")
)
with t1:
    f = px.line(nat_df, x="Date", y=["Demand", "Forecast"], title="National Level", template="plotly_dark",
                color_discrete_sequence=["#4a85e8", "#7ab4f0"])
    f.update_traces(line=dict(width=2.8))
    f.update_layout(**_chart_layout)
    st.plotly_chart(f, use_container_width=True)
with t2:
    f = px.line(reg_df, x="Date", y=["Demand", "Forecast"], title=f"Regional – {region}", template="plotly_dark",
                color_discrete_sequence=["#4a85e8", "#7ab4f0"])
    f.update_traces(line=dict(width=2.8))
    f.update_layout(**_chart_layout)
    st.plotly_chart(f, use_container_width=True)
with t3:
    f = px.line(wh_df, x="Date", y="Demand", color="Warehouse", title="Warehouse Level", template="plotly_dark",
                color_discrete_sequence=["#4a85e8", "#6aaae0", "#8ec4f2"])
    f.update_traces(line=dict(width=2.8))
    f.update_layout(**_chart_layout)
    st.plotly_chart(f, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── ROUTING ──
st.markdown('<div class="section-label sl-3">◆ Route Optimisation</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card cc-2">', unsafe_allow_html=True)
st.subheader("🚛 Intelligent Dynamic Routing")
route_df = pd.DataFrame(all_routes)
route_df["Score (lower better)"] = route_df["score"].round(3)
route_df["Cost"] = route_df["cost"].apply(lambda x: fmt_currency(x, currency))
route_df = route_df[["name", "Cost", "co2", "time_days", "Score (lower better)"]].rename(
    columns={"name": "Route", "co2": "CO₂ (kg)", "time_days": "Time (days)"})
st.dataframe(route_df, use_container_width=True, hide_index=True)
best_cost_fmt = fmt_currency(best_route['cost'], currency)
st.success(f"✅ **Optimal Route:** {best_route['name']} | Cost: {best_cost_fmt} | CO₂: {best_route['co2']} kg | Time: {best_route['time_days']} days")
st.markdown('</div>', unsafe_allow_html=True)

# ── VALIDATION REPORT ──
st.markdown('<div class="section-label sl-4">◆ Strategy Validation</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card cc-3">', unsafe_allow_html=True)
st.subheader("📋 AI Strategy vs. Simple Reorder Point")
baseline_service, baseline_cost_usd = baseline_reorder_point(df)
v1, v2 = st.columns(2)
with v1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📌 BASELINE — SIMPLE REORDER</div>
        <div class="metric-value">Service: {baseline_service:.1f}%</div>
        <div class="metric-value">{fmt_currency(baseline_cost_usd, currency)}</div>
        <div class="metric-label">Order 800 units when stock &lt; 500</div>
    </div>
    """, unsafe_allow_html=True)
with v2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🤖 AI-ENHANCED STRATEGY</div>
        <div class="metric-value">Service: {service_level}%</div>
        <div class="metric-value">{fmt_currency(total_cost_usd, currency)}</div>
        <div class="metric-label">Dynamic forecast · safety stock · smart routing</div>
    </div>
    """, unsafe_allow_html=True)

improvement_service = service_level - baseline_service
improvement_cost_usd = baseline_cost_usd - total_cost_usd
if improvement_cost_usd > 0:
    cost_text = f"✅ AI saves {fmt_currency(improvement_cost_usd, currency)} ({improvement_cost_usd/baseline_cost_usd*100:.1f}%)"
else:
    cost_text = f"⚠️ AI costs {fmt_currency(-improvement_cost_usd, currency)} more"
st.markdown(f"""
<div class="perf-box">
    <b>📈 Performance Gain</b><br><br>
    Service Level <b>{improvement_service:+.1f}%</b> &nbsp;·&nbsp; {cost_text}
</div>
""", unsafe_allow_html=True)

comp_df = pd.DataFrame({
    "Metric": ["Service Level (%)", f"Total Cost ({currency})"],
    "Baseline": [baseline_service, baseline_cost_usd * rate],
    "AI Strategy": [service_level, total_cost_usd * rate]
})
fig_comp = px.bar(comp_df, x="Metric", y=["Baseline", "AI Strategy"], barmode="group",
                  template="plotly_dark", color_discrete_sequence=["#1e3d80", "#4a85e8"])
# Removed invalid marker_corner_radius
fig_comp.update_layout(**_chart_layout)
st.plotly_chart(fig_comp, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── AI PLAYBOOK ──
st.markdown('<div class="section-label">◆ AI Playbook</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card cc-4">', unsafe_allow_html=True)
st.subheader("🤖 AI‑Powered Playbook")
if groq_key and groq_key.strip():
    if st.button("📋 Generate AI Advice", use_container_width=True):
        with st.spinner("Consulting AI supply chain expert..."):
            advice = get_groq_advice(groq_key, region, port_days, supplier_delay,
                                     safety_stock, service_level, total_cost_usd, co2, best_route)
        st.markdown(f'<div class="ai-advice">{advice.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
else:
    st.info("🔑 Enter your **Groq API Key** in the sidebar to unlock AI‑generated logistics playbooks. "
            "Get a free key at [console.groq.com](https://console.groq.com).")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">© 2026 &nbsp;<span>Logistics AI Intelligence Platform</span>&nbsp; · Advanced forecasting · real-time routing · disruption resilience</div>', unsafe_allow_html=True)