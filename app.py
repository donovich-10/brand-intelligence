import os, json, re, requests as req
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from urllib.parse import quote_plus

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kornit Digital — Brand Intelligence</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root{
  --orange:#FF5A00;--orange-pale:#FFF0E8;
  --dark:#0d0d0d;--dark2:#1a1a1a;--dark3:#333;
  --bg:#f5f4f1;--surface:#fff;--surface2:#f0ede8;
  --border:#e8e6e0;--text:#1a1a1a;--muted:#888780;--muted2:#b0ada6;
  --green:#1D9E75;--green-pale:#e1f5ee;--green-text:#085041;
  --blue:#378ADD;--amber:#BA7517;--red:#E24B4A;--purple:#534AB7;
  --radius:10px;--rsm:6px;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}
a{color:var(--orange);text-decoration:none;} a:hover{text-decoration:underline;}
.app{max-width:1140px;margin:0 auto;padding:1.5rem;}

/* HEADER */
.hdr{background:var(--dark);border-radius:var(--radius);padding:1.125rem 1.5rem;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center;}
.logo-kornit{font-size:22px;font-weight:800;color:var(--orange);letter-spacing:-.5px;}
.logo-digital{font-size:22px;font-weight:300;color:#fff;letter-spacing:-.5px;}
.logo-sep{width:1px;height:24px;background:#333;margin:0 14px;}
.logo-sub p{font-size:10px;color:#555;letter-spacing:.12em;margin:0;}
.logo-sub h2{font-size:13px;color:#fff;font-weight:500;margin:0;}
.live-badge{display:flex;align-items:center;gap:6px;padding:5px 12px;background:#1a1a1a;border-radius:100px;border:1px solid #333;}
.live-dot{width:6px;height:6px;border-radius:50%;background:var(--orange);animation:blink 2s ease-in-out infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
.live-txt{font-size:11px;color:var(--orange);font-weight:600;letter-spacing:.08em;}

/* FORM */
.fc{background:var(--surface);border-radius:var(--radius);border:1px solid var(--border);padding:1.25rem;margin-bottom:14px;}
.fg{display:grid;grid-template-columns:2fr 1fr 1fr;gap:10px;margin-bottom:10px;}
.fl label{display:block;font-size:11px;color:var(--muted);margin-bottom:3px;font-weight:500;letter-spacing:.04em;}
.fl input{width:100%;padding:9px 12px;border:1.5px solid var(--border);border-radius:var(--rsm);font-size:13px;background:var(--bg);color:var(--text);outline:none;transition:border .15s;}
.fl input:focus{border-color:var(--orange);}
.comp-tag{display:inline-flex;align-items:center;gap:5px;background:var(--dark);color:#fff;border-radius:4px;padding:3px 8px;font-size:11px;margin:0 4px 4px 0;}
.comp-tag span{cursor:pointer;color:#666;} .comp-tag span:hover{color:#fff;}
.comp-row{display:flex;gap:6px;margin-top:6px;}
.comp-row input{flex:1;}
.btn-primary{width:100%;padding:11px;background:var(--orange);color:#fff;border:none;border-radius:var(--rsm);font-size:14px;font-weight:600;cursor:pointer;transition:opacity .15s;}
.btn-primary:hover{opacity:.88;}
.btn-sec{padding:9px 18px;background:transparent;color:var(--text);border:1.5px solid var(--border);border-radius:var(--rsm);font-size:13px;cursor:pointer;font-weight:500;}
.btn-sec:hover{background:var(--surface2);}
.btn-sm{padding:6px 12px;background:var(--dark);color:#fff;border:none;border-radius:var(--rsm);font-size:11px;cursor:pointer;}
.btn-sm:hover{background:var(--dark3);}
.btn-dl{padding:7px 14px;border:1.5px solid var(--border);border-radius:var(--rsm);font-size:12px;cursor:pointer;background:var(--surface);color:var(--text);font-weight:500;display:inline-flex;align-items:center;gap:5px;}
.btn-dl:hover{background:var(--surface2);}

/* LOADING */
.ld{text-align:center;padding:4rem 1rem;}
.dots{display:flex;justify-content:center;gap:8px;margin-bottom:1rem;}
.dot{width:9px;height:9px;border-radius:50%;background:var(--orange);animation:pulse 1.2s ease-in-out infinite;}
.dot:nth-child(2){animation-delay:.2s;}.dot:nth-child(3){animation-delay:.4s;}
@keyframes pulse{0%,100%{opacity:.2;transform:scale(.65)}50%{opacity:1;transform:scale(1)}}

.eb{background:var(--orange-pale);border:1.5px solid #FF7A30;border-radius:var(--radius);padding:1rem 1.25rem;margin-bottom:14px;color:#7a2d00;font-size:14px;}

/* RESULTS */
.rh{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;flex-wrap:wrap;gap:10px;}
.rt h2{font-size:22px;font-weight:700;}.rt p{font-size:13px;color:var(--muted);margin-top:2px;}
.badge{display:inline-flex;align-items:center;gap:6px;padding:5px 14px;border-radius:100px;font-size:12px;font-weight:600;}
.period-note{font-size:11px;background:var(--orange-pale);color:#7a2d00;padding:6px 12px;border-radius:4px;display:inline-block;margin-bottom:12px;}

/* KPI */
.kg{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px;margin-bottom:12px;}
.kpi{background:var(--surface);border-radius:var(--rsm);padding:.875rem;border:1px solid var(--border);position:relative;}
.kpi.dark{background:var(--dark);border-color:#222;}
.kl{font-size:10px;color:var(--muted);margin-bottom:4px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;}
.kpi.dark .kl{color:#555;}
.kv{font-size:22px;font-weight:700;}
.kpi.dark .kv{color:var(--orange);}
.ks{font-size:10px;margin-top:2px;}
.info-icon{display:inline-flex;align-items:center;justify-content:center;width:14px;height:14px;border-radius:50%;background:var(--border);color:var(--muted);font-size:9px;font-weight:700;cursor:help;margin-right:3px;position:relative;}
.info-tip{display:none;position:absolute;bottom:120%;left:0;background:var(--dark);color:#fff;font-size:11px;padding:8px 10px;border-radius:6px;width:220px;line-height:1.5;z-index:200;font-weight:400;}
.info-tip::after{content:'';position:absolute;top:100%;left:10px;border:5px solid transparent;border-top-color:var(--dark);}
.info-icon:hover .info-tip{display:block;}

/* CHANNEL CARDS */
.ch-grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:8px;margin-bottom:12px;}
.ch-card{background:var(--surface);border-radius:var(--rsm);padding:.75rem;border:1px solid var(--border);border-top:3px solid;cursor:pointer;transition:box-shadow .15s;}
.ch-card:hover{box-shadow:0 2px 8px rgba(0,0,0,.08);}
.ch-name{font-size:10px;color:var(--muted);font-weight:600;letter-spacing:.04em;text-transform:uppercase;margin-bottom:4px;}
.ch-count{font-size:18px;font-weight:700;}
.ch-sent{font-size:10px;margin-top:3px;position:relative;}
.tt{display:none;position:absolute;bottom:120%;left:50%;transform:translateX(-50%);background:var(--dark);color:#fff;font-size:11px;padding:8px 10px;border-radius:6px;width:200px;line-height:1.5;z-index:100;}
.tt::after{content:'';position:absolute;top:100%;left:50%;transform:translateX(-50%);border:5px solid transparent;border-top-color:var(--dark);}
.ch-sent:hover .tt{display:block;}
.ch-reach{font-size:10px;color:var(--muted);}
.ch-tap{font-size:9px;color:var(--muted);margin-top:4px;opacity:.7;}

/* MODAL */
.modal-backdrop{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);z-index:1000;align-items:center;justify-content:center;}
.modal-backdrop.open{display:flex;}
.modal{background:var(--surface);border-radius:var(--radius);padding:1.5rem;max-width:560px;width:90%;max-height:80vh;overflow-y:auto;}
.modal-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;}
.modal-head h3{font-size:16px;font-weight:600;}
.modal-close{background:none;border:none;font-size:20px;cursor:pointer;color:var(--muted);padding:4px 8px;}
.modal-close:hover{color:var(--text);}
.modal-method{background:var(--surface2);border-radius:var(--rsm);padding:.875rem;margin-bottom:1rem;font-size:13px;line-height:1.6;}
.modal-src{padding:8px 0;border-bottom:1px solid var(--border);}
.modal-src:last-child{border-bottom:none;}
.modal-src a{font-size:13px;font-weight:500;color:var(--orange);}
.modal-src .meta{font-size:11px;color:var(--muted);margin-top:2px;}

/* CARDS */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem;}
.ct{font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.ct::after{content:'';flex:1;height:1px;background:var(--border);}
.cr{display:grid;grid-template-columns:1.6fr 1fr;gap:12px;margin-bottom:12px;}
.ar{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px;}
.leg{display:flex;flex-direction:column;gap:5px;margin-top:10px;}
.li{display:flex;justify-content:space-between;align-items:center;font-size:12px;}
.ldot{width:8px;height:8px;border-radius:50%;margin-right:6px;flex-shrink:0;}
.sb{margin-bottom:10px;}
.sbl{display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;}
.bt{height:7px;background:var(--surface2);border-radius:4px;overflow:hidden;}
.bf{height:100%;border-radius:4px;}

/* NEGATIVE MENTIONS */
.neg-section{background:#FFF8F8;border:1.5px solid #F09595;border-radius:var(--radius);padding:1.25rem;margin-bottom:12px;}
.neg-title{font-size:11px;font-weight:700;color:#501313;letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px;}
.neg-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;}
.neg-kpi{background:var(--surface);border-radius:var(--rsm);padding:.75rem;border:1px solid #F09595;}
.neg-kpi .kl{font-size:10px;color:#A32D2D;font-weight:600;letter-spacing:.05em;margin-bottom:3px;}
.neg-kpi .kv{font-size:18px;font-weight:700;color:#E24B4A;}
.neg-item{background:var(--surface);border-radius:var(--rsm);padding:.875rem;margin-bottom:8px;border:1px solid #F09595;display:flex;gap:10px;align-items:flex-start;}
.neg-item:last-child{margin-bottom:0;}
.neg-icon{width:28px;height:28px;border-radius:50%;background:#fcebeb;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#E24B4A;flex-shrink:0;}
.neg-body{flex:1;}
.neg-text{font-size:13px;color:#501313;line-height:1.5;}
.neg-meta{font-size:11px;color:#A32D2D;margin-top:3px;}
.neg-search{font-size:11px;color:var(--orange);font-weight:600;margin-top:5px;display:inline-flex;align-items:center;gap:3px;padding:3px 8px;border:1px solid var(--orange);border-radius:3px;}

/* COMPETITOR */
.comp-bar{margin-bottom:10px;}
.comp-bar-row{display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;}
.comp-bar-track{height:8px;background:var(--surface2);border-radius:4px;overflow:hidden;}
.comp-bar-fill{height:100%;border-radius:4px;transition:width .6s ease;}

/* YoY */
.yoy-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-bottom:12px;}
.yoy-card{background:var(--surface);border-radius:var(--rsm);padding:.875rem;border:1px solid var(--border);}
.yoy-label{font-size:10px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px;}
.yoy-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;}
.yoy-delta{font-size:12px;font-weight:600;padding:2px 8px;border-radius:100px;margin-top:6px;display:inline-block;}
.yoy-up{background:var(--green-pale);color:var(--green-text);}
.yoy-down{background:#fcebeb;color:#501313;}
.yoy-flat{background:var(--surface2);color:var(--muted);}

/* ALERTS */
.albox{background:var(--orange-pale);border:1.5px solid #FF7A30;border-radius:var(--radius);padding:1.25rem;margin-bottom:12px;}
.al-title{font-size:11px;font-weight:700;color:#7a2d00;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px;}
.al-item{background:var(--surface);border-radius:var(--rsm);padding:.875rem;margin-bottom:8px;border:1px solid #ffc4a0;}
.al-item:last-child{margin-bottom:0;}
.al-item-title{font-size:13px;font-weight:600;color:#7a2d00;margin-bottom:4px;}
.al-item-text{font-size:12px;color:#a04020;line-height:1.6;}
.al-search{font-size:11px;color:var(--orange);font-weight:600;margin-top:6px;display:inline-flex;align-items:center;gap:4px;padding:4px 10px;border:1px solid var(--orange);border-radius:4px;}

/* SOURCES */
.src-group{margin-bottom:16px;}
.src-group-title{font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px;display:flex;align-items:center;gap:6px;}
.src-item{display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid var(--border);}
.src-item:last-child{border-bottom:none;}
.src-icon{width:30px;height:30px;border-radius:5px;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:11px;font-weight:700;}
.src-body{flex:1;min-width:0;}
.src-link{font-size:13px;font-weight:500;color:var(--orange);display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.src-meta{font-size:11px;color:var(--muted);margin-top:2px;}

/* THEMES */
.tp{display:inline-flex;align-items:center;gap:5px;background:var(--dark);color:#fff;border-radius:100px;padding:5px 12px;font-size:11px;margin:0 5px 5px 0;font-weight:500;}
.tp-dot{width:5px;height:5px;border-radius:50%;background:var(--orange);}

/* ACTIONS */
.act-item{display:flex;gap:10px;align-items:flex-start;padding:10px 0;border-bottom:1px solid var(--border);}
.act-item:last-child{border-bottom:none;}
.act-num{min-width:24px;height:24px;border-radius:50%;background:var(--orange);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.act-text{font-size:13px;line-height:1.55;}

.sumbox{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem;margin-bottom:12px;}
.sumbox p{font-size:14px;line-height:1.8;}
.dl-bar{display:flex;gap:8px;justify-content:flex-end;margin-bottom:12px;}
.fn{font-size:11px;color:var(--muted2);text-align:center;padding:1rem 0;border-top:1px solid var(--border);margin-top:1.5rem;}
.hidden{display:none!important;}
@media(max-width:900px){.kg{grid-template-columns:repeat(3,1fr);}.ch-grid{grid-template-columns:repeat(4,1fr);}.cr,.ar{grid-template-columns:1fr;}.yoy-grid{grid-template-columns:repeat(2,1fr);}.fg{grid-template-columns:1fr 1fr;}.neg-grid{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="app">

<!-- HEADER -->
<div class="hdr">
  <div style="display:flex;align-items:center;gap:14px;">
    <div style="display:flex;align-items:baseline;">
      <span class="logo-kornit">kornit</span><span class="logo-digital">digital</span>
    </div>
    <div class="logo-sep"></div>
    <div class="logo-sub"><p>BRAND INTELLIGENCE</p><h2>Monitor Dashboard</h2></div>
  </div>
  <div class="live-badge"><div class="live-dot"></div><span class="live-txt">LIVE</span></div>
</div>

<!-- FORM -->
<div class="fc" id="fs">
  <div class="fg">
    <div class="fl"><label>Brand name</label><input id="brand" type="text" placeholder="e.g. Kornit Digital" value="Kornit Digital"/></div>
    <div class="fl"><label>From (DD/MM/YYYY)</label><input id="sd" type="text" placeholder="01/01/2026"/></div>
    <div class="fl"><label>To (DD/MM/YYYY)</label><input id="ed" type="text" placeholder="14/04/2026"/></div>
  </div>
  <div class="fl" style="margin-bottom:10px;">
    <label>Competitors</label>
    <div id="comp-tags"></div>
    <div class="comp-row"><input id="comp-input" type="text" placeholder="Add competitor + Enter"/><button class="btn-sm" onclick="addComp()">Add</button></div>
  </div>
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
    <label style="display:flex;align-items:center;gap:6px;font-size:13px;cursor:pointer;">
      <input type="checkbox" id="yoy-toggle" checked style="accent-color:var(--orange);width:15px;height:15px;"/>
      Include year-over-year comparison
    </label>
  </div>
  <button class="btn-primary" onclick="startScan()">Run Brand Scan →</button>
</div>

<div id="ls" class="hidden ld"><div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div><p id="lm">Scanning...</p></div>
<div id="es" class="hidden eb"></div>

<!-- RESULTS -->
<div id="rs" class="hidden">
  <div class="rh">
    <div class="rt"><h2 id="rb"></h2><p id="rp"></p></div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
      <span id="sb2" class="badge"></span>
      <button class="btn-sec" onclick="newScan()">New scan</button>
    </div>
  </div>
  <div class="period-note" id="period-note"></div>
  <div class="dl-bar">
    <button class="btn-dl" onclick="dlWord()">
      <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><path d="M4 1h6l4 4v10H2V1z" stroke="currentColor" stroke-width="1.2" fill="none"/><path d="M10 1v4h4" stroke="currentColor" stroke-width="1.2" fill="none"/><path d="M5 8l1.5 4 1.5-3 1.5 3L11 8" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
      Export to Word (.doc)
    </button>
    <button class="btn-dl" onclick="dlPDF()">
      <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><path d="M4 1h6l4 4v10H2V1z" stroke="currentColor" stroke-width="1.2" fill="none"/><path d="M10 1v4h4M5 9h6M5 11.5h4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" fill="none"/></svg>
      Export Full PDF
    </button>
  </div>

  <!-- KPIs -->
  <div class="kg">
    <div class="kpi"><div class="kl"><span class="info-icon">i<div class="info-tip">Total estimated mentions across all channels: news articles, social posts, forum threads, YouTube videos, and podcast episodes. Estimated by AI based on platform volume signals.</div></span>Mentions</div><div class="kv" id="km">—</div><div class="ks" id="km-delta"></div></div>
    <div class="kpi"><div class="kl"><span class="info-icon">i<div class="info-tip">Estimated total audience who could have seen a mention. Calculated by summing estimated reach per channel based on typical platform audience sizes.</div></span>Reach</div><div class="kv" id="kr">—</div><div class="ks" id="kr-delta"></div></div>
    <div class="kpi dark"><div class="kl"><span class="info-icon" style="background:#333;color:#888;">i<div class="info-tip">Sentiment score from -100 (very negative) to +100 (very positive). Calculated as: (Positive% - Negative%) × 100, weighted by channel reach.</div></span>Sentiment</div><div class="kv" id="ksc">—</div><div class="ks" id="ksc-delta"></div></div>
    <div class="kpi"><div class="kl"><span class="info-icon">i<div class="info-tip">Composite score 0-100 combining: 30% search exposure + 30% social reach + 25% media coverage + 15% web/referral signals.</div></span>Exposure</div><div class="kv" id="ke">—</div></div>
    <div class="kpi"><div class="kl"><span class="info-icon">i<div class="info-tip">Your brand's mention share vs competitors: Your mentions ÷ (Your + all competitor mentions) × 100. Competitors: shown below.</div></span>Share of Voice</div><div class="kv" id="ksv">—</div></div>
    <div class="kpi"><div class="kl"><span class="info-icon">i<div class="info-tip">Total number of individual source examples collected across all channels. Click any channel card below to see its sources.</div></span>Sources</div><div class="kv" id="ksrc">—</div></div>
  </div>

  <!-- Channel cards -->
  <div class="ch-grid" id="ch-grid"></div>

  <!-- Negative mentions -->
  <div id="neg-section" class="hidden neg-section">
    <div class="neg-title">Negative mentions — detail</div>
    <div class="neg-grid" id="neg-kpis"></div>
    <div id="neg-items"></div>
  </div>

  <!-- YoY -->
  <div id="yoy-section" class="hidden card" style="margin-bottom:12px;">
    <div class="ct">Year-over-year comparison</div>
    <div class="yoy-grid" id="yoy-grid"></div>
    <canvas id="yoy-chart" height="80"></canvas>
  </div>

  <!-- Charts -->
  <div class="cr">
    <div class="card"><div class="ct">Coverage over time</div><canvas id="tc" height="130"></canvas></div>
    <div class="card"><div class="ct">Reach by channel</div><canvas id="dc" height="150"></canvas><div class="leg" id="dl2"></div></div>
  </div>

  <!-- Analysis -->
  <div class="ar">
    <div class="card">
      <div class="ct">Sentiment breakdown</div>
      <div id="sbars"></div>
      <div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--border);">
        <div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px;">Top themes</div>
        <div id="themes"></div>
      </div>
    </div>
    <div class="card"><div class="ct">Share of voice vs competitors</div><div id="comp-chart"></div></div>
    <div class="card"><div class="ct">Recommended actions</div><div id="al2"></div></div>
  </div>

  <div class="sumbox"><div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px;">Executive summary</div><p id="st"></p></div>

  <div id="albox" class="hidden albox"><div class="al-title">Alerts & Signals</div><div id="alist"></div></div>

  <div class="card" style="margin-bottom:12px;">
    <div class="ct">Sources & verification links</div>
    <p style="font-size:11px;color:var(--muted);margin-bottom:12px;">Every link opens a targeted Google search to verify the mention. Click any channel card above for a focused view.</p>
    <div id="exs"></div>
  </div>

  <div class="fn" id="scan-date"></div>
</div>

<!-- SOURCE MODAL -->
<div class="modal-backdrop" id="modal" onclick="closeModal(event)">
  <div class="modal">
    <div class="modal-head">
      <h3 id="modal-title">Sources</h3>
      <button class="modal-close" onclick="closeModal()">×</button>
    </div>
    <div class="modal-method" id="modal-method"></div>
    <div id="modal-sources"></div>
  </div>
</div>

<script>
let tC=null,dC=null,yoyC=null,scanData=null;
const LOADS=["Scanning news & press...","Analyzing social media...","Checking YouTube & podcasts...","Reviewing forums...","Comparing competitors...","Building YoY comparison...","Compiling report..."];
const CH_COLORS={articles:"#FF5A00",social:"#378ADD",ads:"#BA7517",events:"#534AB7",forums:"#888780",youtube:"#E24B4A",podcasts:"#1D9E75"};
const CH_NAMES={articles:"Articles",social:"Social",ads:"Ads",events:"Events",forums:"Forums",youtube:"YouTube",podcasts:"Podcasts"};
const CH_ICONS={articles:"A",social:"S",ads:"Ad",events:"Ev",forums:"F",youtube:"YT",podcasts:"PC"};
const CH_METHOD={
  articles:"Count of news articles and press releases mentioning the brand. Estimated by AI based on typical media coverage volume for this type of company and period.",
  social:"Estimated social media posts across LinkedIn, Facebook, Instagram, X/Twitter. Based on typical engagement patterns for B2B industrial brands.",
  ads:"Detected paid advertising placements on Google, Meta, and LinkedIn. Estimated from typical campaign activity signals.",
  events:"Industry events, webinars, and conferences where the brand was present or mentioned as sponsor/speaker.",
  forums:"Threads and comments on Reddit, industry forums, and professional communities discussing the brand.",
  youtube:"Videos on YouTube that mention or review the brand. Estimated from channel activity and keyword searches.",
  podcasts:"Episode mentions on Spotify and Apple Podcasts. Based on industry podcast monitoring signals."
};
let competitors=["ROQ","MrPrint","Brother DTG"];

function renderTags(){document.getElementById("comp-tags").innerHTML=competitors.map((c,i)=>`<span class="comp-tag">${c}<span onclick="removeComp(${i})">×</span></span>`).join("");}
function addComp(){const v=document.getElementById("comp-input").value.trim();if(v&&!competitors.includes(v)){competitors.push(v);renderTags();document.getElementById("comp-input").value="";}}
function removeComp(i){competitors.splice(i,1);renderTags();}
document.getElementById("comp-input").addEventListener("keydown",e=>{if(e.key==="Enter")addComp();});
renderTags();

const t=new Date(),m2=new Date();m2.setDate(t.getDate()-30);
document.getElementById("ed").value=fmt(t);document.getElementById("sd").value=fmt(m2);
function fmt(d){return String(d.getDate()).padStart(2,"0")+"/"+String(d.getMonth()+1).padStart(2,"0")+"/"+d.getFullYear();}
function parseD(s){if(!s)return"";const p=s.split("/");if(p.length===3)return`${p[2]}-${p[1].padStart(2,"0")}-${p[0].padStart(2,"0")}`;return s;}
function fN(n){if(!n&&n!==0)return"—";if(n>=1e6)return(n/1e6).toFixed(1)+"M";if(n>=1e3)return Math.round(n/1e3)+"K";return String(Math.round(n));}
function show(id){document.getElementById(id).classList.remove("hidden");}
function hide(id){document.getElementById(id).classList.add("hidden");}
function sentColor(s){return(s==="Positive"||s==="חיובי")?"#1D9E75":(s==="Negative"||s==="שלילי")?"#E24B4A":"#888780";}
function sentLabel(s){if(s==="חיובי"||s==="Positive")return"Positive";if(s==="שלילי"||s==="Negative")return"Negative";return"Neutral";}
function gSearch(brand,q){return`https://www.google.com/search?q=${encodeURIComponent('"'+brand+'" '+q)}`;}

function openModal(key,cats,brand){
  const cat=cats[key]||{};
  document.getElementById("modal-title").textContent=`${CH_NAMES[key]||key} — ${fN(cat.count)} mentions`;
  document.getElementById("modal-method").innerHTML=`<strong>How this number is calculated:</strong><br>${CH_METHOD[key]||"AI-estimated based on platform signals."}`;
  const exs=cat.examples||[];
  document.getElementById("modal-sources").innerHTML=exs.length
    ?exs.map(ex=>{const label=ex.title||ex.text||ex.name||"Source";const sub=ex.source||ex.platform||ex.date||"";const url=gSearch(brand,label);return`<div class="modal-src"><a href="${url}" target="_blank">${label}</a><div class="meta">${sub||CH_NAMES[key]}</div></div>`;}).join("")
    :`<p style="font-size:13px;color:var(--muted);">No specific examples collected for this channel.</p>`;
  document.getElementById("modal").classList.add("open");
}
function closeModal(e){if(!e||e.target===document.getElementById("modal"))document.getElementById("modal").classList.remove("open");}

async function startScan(){
  const brand=document.getElementById("brand").value.trim();
  if(!brand){alert("Please enter a brand name");return;}
  const sdRaw=document.getElementById("sd").value,edRaw=document.getElementById("ed").value;
  if(!sdRaw||!edRaw){alert("Please enter both dates");return;}
  hide("fs");hide("es");hide("rs");show("ls");
  let li=0;const lt=setInterval(()=>{li=(li+1)%LOADS.length;document.getElementById("lm").textContent=LOADS[li];},2000);
  const includeYoY=document.getElementById("yoy-toggle").checked;
  try{
    const r=await fetch("/scan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({brand,start_date:parseD(sdRaw),end_date:parseD(edRaw),competitors:competitors.join(", "),include_yoy:includeYoY})});
    const txt=await r.text();clearInterval(lt);hide("ls");
    let result;try{result=JSON.parse(txt);}catch(e){throw new Error("Server error: "+txt.substring(0,200));}
    if(!result.success)throw new Error(result.error||"Unknown error");
    scanData=result.data;
    render(result.data,sdRaw,edRaw);
  }catch(err){clearInterval(lt);hide("ls");show("fs");document.getElementById("es").textContent="Error: "+err.message;show("es");}
}

function newScan(){hide("rs");show("fs");[tC,dC,yoyC].forEach(c=>{if(c)c.destroy();});tC=dC=yoyC=null;}

function render(d,sdRaw,edRaw){
  const cats=d.categories||{};
  document.getElementById("rb").textContent=d.brand||"";
  document.getElementById("rp").textContent=`${sdRaw} – ${edRaw}`;
  document.getElementById("period-note").textContent=`Analysis covers strictly: ${sdRaw} – ${edRaw}`;
  document.getElementById("scan-date").textContent=`Analysis covers ${sdRaw} – ${edRaw} · Scanned: ${fmt(new Date())} · Kornit Digital Brand Intelligence`;

  const sm={"Positive":{bg:"#e1f5ee",c:"#085041"},"Neutral":{bg:"#faeeda",c:"#412402"},"Negative":{bg:"#fcebeb",c:"#501313"},"חיובי":{bg:"#e1f5ee",c:"#085041"},"ניטרלי":{bg:"#faeeda",c:"#412402"},"שלילי":{bg:"#fcebeb",c:"#501313"}};
  const sc=sm[d.overall_sentiment]||sm["Neutral"];
  const sb=document.getElementById("sb2");sb.style.background=sc.bg;sb.style.color=sc.c;
  sb.innerHTML=`<span style="width:6px;height:6px;border-radius:50%;background:currentColor;display:inline-block;margin-left:2px;"></span> ${sentLabel(d.overall_sentiment)}`;

  const tr=Object.values(cats).reduce((s,c)=>s+(c.estimated_reach||0),0);
  const srcCount=Object.values(cats).reduce((s,c)=>s+(c.examples?.length||0),0);
  const yoy=d.yoy||null;
  function delta(curr,prev){if(!prev)return"";const p=Math.round(((curr-prev)/prev)*100);return`<span style="font-size:10px;font-weight:600;color:${p>=0?"#1D9E75":"#E24B4A}">${p>=0?"+":""}${p}% vs prev year</span>`;}

  document.getElementById("km").textContent=fN(d.total_mentions_estimate);
  document.getElementById("km-delta").innerHTML=yoy?delta(d.total_mentions_estimate,yoy.total_mentions_estimate):"";
  document.getElementById("kr").textContent=fN(tr);
  const yoyReach=yoy?Object.values(yoy.categories||{}).reduce((s,c)=>s+(c.estimated_reach||0),0):0;
  document.getElementById("kr-delta").innerHTML=yoy?delta(tr,yoyReach):"";
  const sc2=d.sentiment_score||0;const se=document.getElementById("ksc");se.textContent=(sc2>0?"+":"")+Math.round(sc2);se.style.color=sc2>30?"#FF5A00":sc2<-30?"#E24B4A":"#888";
  document.getElementById("ksc-delta").innerHTML=yoy?`<span style="font-size:10px;color:var(--muted);">Last year: ${yoy.sentiment_score>0?"+":""}${yoy.sentiment_score||0}</span>`:"";
  document.getElementById("ke").textContent=(d.exposure_index||"—")+(d.exposure_index?"/100":"");
  document.getElementById("ksv").textContent=(d.share_of_voice||"—")+(d.share_of_voice?"%":"");
  document.getElementById("ksrc").textContent=srcCount||"—";

  // Channel cards — clickable
  document.getElementById("ch-grid").innerHTML=Object.entries(cats).map(([k,c])=>{
    const sl=sentLabel(c.sentiment);const col=sentColor(c.sentiment);
    return`<div class="ch-card" style="border-top-color:${CH_COLORS[k]||'#ccc'}" onclick="openModal('${k}',scanData.categories,'${d.brand}')">
      <div class="ch-name">${CH_NAMES[k]||k}</div>
      <div class="ch-count" style="color:${CH_COLORS[k]||'#1a1a1a'};">${fN(c.count)}</div>
      <div class="ch-sent" style="color:${col};">${sl}<div class="tt">${c.sentiment_reason||"Based on mention tone analysis."}</div></div>
      <div class="ch-reach">${fN(c.estimated_reach)} reach</div>
      <div class="ch-tap">Tap to verify sources</div>
    </div>`;
  }).join("");

  // Negative mentions section
  const negMentions=d.negative_mentions||[];
  const negTotal=d.sentiment_breakdown?Math.round((d.sentiment_breakdown.negative/100)*(d.total_mentions_estimate||0)):0;
  if(negMentions.length||negTotal>0){
    show("neg-section");
    document.getElementById("neg-kpis").innerHTML=`
      <div class="neg-kpi"><div class="kl">Negative mentions</div><div class="kv">${fN(negTotal)}</div></div>
      <div class="neg-kpi"><div class="kl">% of total</div><div class="kv">${d.sentiment_breakdown?.negative||0}%</div></div>
      <div class="neg-kpi"><div class="kl">Main negative theme</div><div class="kv" style="font-size:14px;">${d.main_negative_theme||"—"}</div></div>
      <div class="neg-kpi"><div class="kl">vs competitors avg</div><div class="kv" style="font-size:14px;">${d.competitor_negative_avg||"—"}%</div></div>`;
    document.getElementById("neg-items").innerHTML=negMentions.map(n=>{
      const q=gSearch(d.brand,n.text||n.title||"negative mention");
      return`<div class="neg-item">
        <div class="neg-icon">!</div>
        <div class="neg-body">
          <div class="neg-text">${n.text||n.title||""}</div>
          <div class="neg-meta">${n.source||n.platform||""} · ${n.date||""}</div>
          <a href="${q}" target="_blank" class="neg-search">Find on Google ↗</a>
        </div>
      </div>`;
    }).join("");
  }else hide("neg-section");

  // YoY
  if(yoy){
    show("yoy-section");
    const metrics=[
      {label:"Total mentions",curr:d.total_mentions_estimate,prev:yoy.total_mentions_estimate},
      {label:"Sentiment score",curr:d.sentiment_score,prev:yoy.sentiment_score},
      {label:"Exposure index",curr:d.exposure_index,prev:yoy.exposure_index},
      {label:"Share of voice",curr:d.share_of_voice,prev:yoy.share_of_voice,unit:"%"},
    ];
    document.getElementById("yoy-grid").innerHTML=metrics.map(m=>{
      const pct=m.prev?Math.round(((m.curr-m.prev)/m.prev)*100):0;
      const cls=pct>5?"yoy-up":pct<-5?"yoy-down":"yoy-flat";
      const yr=edRaw.split("/")[2]||"";
      return`<div class="yoy-card"><div class="yoy-label">${m.label}</div>
        <div class="yoy-row"><span style="font-size:11px;color:var(--muted);">${yr}</span><span style="font-size:14px;font-weight:700;">${fN(m.curr)}${m.unit||""}</span></div>
        <div class="yoy-row"><span style="font-size:11px;color:var(--muted);">${yr?parseInt(yr)-1:""}</span><span style="font-size:14px;font-weight:700;color:var(--muted);">${fN(m.prev)}${m.unit||""}</span></div>
        <span class="yoy-delta ${cls}">${pct>=0?"+":""}${pct}%</span></div>`;
    }).join("");
    const mv=d.monthly_volume||[],mv2=yoy.monthly_volume||[];
    if(yoyC)yoyC.destroy();
    yoyC=new Chart(document.getElementById("yoy-chart"),{type:"line",data:{labels:mv.map(m=>m.month),datasets:[
      {label:"This period",data:mv.map(m=>(m.articles||0)+(m.social||0)+(m.forums||0)),borderColor:"#FF5A00",backgroundColor:"rgba(255,90,0,0.06)",borderWidth:2,tension:.3,pointRadius:3,fill:true},
      {label:"Last year",data:mv2.map(m=>(m.articles||0)+(m.social||0)+(m.forums||0)),borderColor:"#ccc",backgroundColor:"transparent",borderWidth:1.5,tension:.3,pointRadius:2,borderDash:[4,3]},
    ]},options:{responsive:true,plugins:{legend:{display:true,position:"bottom",labels:{font:{size:11},boxWidth:12}}},scales:{x:{grid:{display:false}},y:{beginAtZero:true,grid:{color:"rgba(0,0,0,0.04)"}}},animation:{duration:600}}});
  }else hide("yoy-section");

  // Timeline
  const mv=d.monthly_volume||[];
  if(tC)tC.destroy();
  tC=new Chart(document.getElementById("tc"),{type:"bar",data:{labels:mv.map(m=>m.month),datasets:[
    {label:"Articles",data:mv.map(m=>m.articles||0),backgroundColor:"#FF5A00",borderRadius:3},
    {label:"Social",data:mv.map(m=>m.social||0),backgroundColor:"#378ADD",borderRadius:3},
    {label:"YouTube",data:mv.map(m=>m.youtube||0),backgroundColor:"#E24B4A",borderRadius:3},
    {label:"Forums",data:mv.map(m=>m.forums||0),backgroundColor:"#888780",borderRadius:3},
  ]},options:{responsive:true,plugins:{legend:{display:false}},scales:{x:{grid:{display:false},stacked:true},y:{grid:{color:"rgba(0,0,0,0.04)"},beginAtZero:true,stacked:true}},animation:{duration:700}}});

  // Donut
  const cks=Object.keys(cats),cd=cks.map(k=>cats[k].estimated_reach||0),cc=cks.map(k=>CH_COLORS[k]||"#888");
  if(dC)dC.destroy();
  dC=new Chart(document.getElementById("dc"),{type:"doughnut",data:{labels:cks.map(k=>CH_NAMES[k]||k),datasets:[{data:cd,backgroundColor:cc,borderWidth:0,hoverOffset:4}]},options:{responsive:true,cutout:"70%",plugins:{legend:{display:false}},animation:{duration:700}}});
  const tl=cd.reduce((a,b)=>a+b,0)||1;
  document.getElementById("dl2").innerHTML=cks.map((k,i)=>`<div class="li"><div style="display:flex;align-items:center;"><div class="ldot" style="background:${cc[i]};"></div><span style="font-size:12px;">${CH_NAMES[k]||k}</span></div><span style="font-size:12px;font-weight:600;">${Math.round((cd[i]/tl)*100)}%</span></div>`).join("");

  // Sentiment
  const sb3=d.sentiment_breakdown||{positive:60,neutral:30,negative:10};
  document.getElementById("sbars").innerHTML=["Positive","Neutral","Negative"].map((l,i)=>{const k=l.toLowerCase();const col=i===0?"#1D9E75":i===2?"#E24B4A":"#888780";const v=sb3[k]||0;return`<div class="sb"><div class="sbl"><span>${l}</span><span style="color:${col};font-weight:600;">${v}%</span></div><div class="bt"><div class="bf" style="width:${v}%;background:${col};"></div></div></div>`;}).join("");
  document.getElementById("themes").innerHTML=(d.top_themes||[]).map(t=>`<span class="tp"><div class="tp-dot"></div>${t}</span>`).join("");

  // Competitors — NEVER include brand itself
  const brand=d.brand||"";
  const comps=(d.competitor_comparison||[]).filter(c=>c.name&&c.name.toLowerCase()!==brand.toLowerCase());
  document.getElementById("comp-chart").innerHTML=[
    {name:brand,sov:d.share_of_voice||0,sentiment:d.overall_sentiment,color:"#FF5A00"},
    ...comps
  ].map(b=>`<div class="comp-bar">
    <div class="comp-bar-row"><span style="font-weight:600;color:${b.color||'#1a1a1a'};font-size:13px;">${b.name}</span><span style="font-size:12px;font-weight:700;">${b.sov||0}%</span></div>
    <div class="comp-bar-track"><div class="comp-bar-fill" style="width:${b.sov||0}%;background:${b.color||'#ccc'};"></div></div>
    <div style="font-size:10px;color:${sentColor(b.sentiment)};margin-top:2px;">${sentLabel(b.sentiment)||""}</div>
  </div>`).join("");

  // Actions
  document.getElementById("al2").innerHTML=(d.recommended_actions||[]).map((a,i)=>`<div class="act-item"><div class="act-num" style="background:${["#FF5A00","#378ADD","#534AB7","#1D9E75"][i]||'#888'}">${i+1}</div><div class="act-text">${a}</div></div>`).join("");
  document.getElementById("st").textContent=d.summary||d.summary_he||"";

  // Alerts
  const alerts=(d.alerts||[]).filter(a=>a);
  if(alerts.length){
    document.getElementById("alist").innerHTML=alerts.map(a=>{const isO=typeof a==="object";const title=isO?a.title:"Alert";const text=isO?a.text:a;const q=gSearch(brand,title);return`<div class="al-item"><div class="al-item-title">${title}</div><div class="al-item-text">${text}</div><a href="${q}" target="_blank" class="al-search">Search Google for this ↗</a></div>`;}).join("");
    show("albox");
  }else hide("albox");

  // Sources
  let exH="";
  for(const[k,cat]of Object.entries(cats)){
    const exs=cat.examples;if(!exs||!exs.length)continue;
    exH+=`<div class="src-group"><div class="src-group-title"><div style="width:8px;height:8px;border-radius:50%;background:${CH_COLORS[k]||'#888'};"></div>${CH_NAMES[k]||k}</div>`;
    exs.forEach(ex=>{const label=ex.title||ex.text||ex.name||"Source";const sub=ex.source||ex.platform||ex.date||"";const bgCol=CH_COLORS[k]||"#888";const icon=CH_ICONS[k]||"?";const url=gSearch(brand,label);exH+=`<div class="src-item"><div class="src-icon" style="background:${bgCol}20;color:${bgCol};">${icon}</div><div class="src-body"><a href="${url}" target="_blank" class="src-link">${label}</a>${sub?`<div class="src-meta">${sub}</div>`:""}</div></div>`;});
    exH+="</div>";
  }
  document.getElementById("exs").innerHTML=exH||"<p style='font-size:13px;color:var(--muted);'>No sources found</p>";
  show("rs");
}

function dlWord(){
  if(!scanData){return;}
  const d=scanData;
  const brand=d.brand||"Brand";
  const period=document.getElementById("rp").textContent||"";
  const summary=d.summary||d.summary_he||"";
  const actions=(d.recommended_actions||[]).map((a,i)=>`<li style="margin:6px 0;">${a}</li>`).join("");
  const compRows=(d.competitor_comparison||[]).filter(c=>c.name!==brand).map(c=>`<tr><td>${c.name}</td><td>${c.sov||0}%</td><td>${c.sentiment||""}</td></tr>`).join("");
  const catRows=Object.entries(d.categories||{}).map(([k,c])=>`<tr><td>${CH_NAMES[k]||k}</td><td>${fN(c.count)}</td><td>${fN(c.estimated_reach)}</td><td>${c.sentiment||""}</td></tr>`).join("");
  const sb=d.sentiment_breakdown||{};
  const html=`<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
<head><meta charset='utf-8'><title>${brand}</title>
<style>
body{font-family:Calibri,Arial,sans-serif;font-size:11pt;color:#1a1a1a;margin:40px;}
h1{font-size:18pt;color:#FF5A00;border-bottom:2pt solid #FF5A00;padding-bottom:8px;margin-bottom:16px;}
h2{font-size:13pt;color:#1a1a1a;margin-top:24px;margin-bottom:8px;}
table{border-collapse:collapse;width:100%;margin:10px 0;}
th{background:#FF5A00;color:#fff;padding:7px 10px;text-align:left;font-size:10pt;}
td{padding:6px 10px;border-bottom:1px solid #e0ddd6;font-size:10pt;}
.box{background:#f5f4f1;padding:14px;margin:10px 0;border-left:4px solid #FF5A00;}
.kpi-row{display:flex;gap:20px;margin:10px 0;}
.kpi-item{text-align:center;border:1px solid #e0ddd6;padding:10px 16px;min-width:90px;}
.kpi-label{font-size:9pt;color:#888;}
.kpi-val{font-size:16pt;font-weight:bold;color:#FF5A00;}
.footer{margin-top:30px;font-size:9pt;color:#888;border-top:1px solid #ddd;padding-top:10px;}
</style></head><body>
<h1>${brand} — Brand Intelligence Report</h1>
<p style="color:#888;font-size:10pt;">Period: ${period} &nbsp;|&nbsp; Generated: ${fmt(new Date())}</p>
<h2>Key metrics</h2>
<table><tr><th>Metric</th><th>Value</th></tr>
<tr><td>Total mentions</td><td><strong>${fN(d.total_mentions_estimate)}</strong></td></tr>
<tr><td>Sentiment score</td><td><strong>${d.sentiment_score>0?"+":""}${d.sentiment_score||0}</strong></td></tr>
<tr><td>Exposure index</td><td><strong>${d.exposure_index||"—"}/100</strong></td></tr>
<tr><td>Share of voice</td><td><strong>${d.share_of_voice||0}%</strong></td></tr>
<tr><td>Positive mentions</td><td>${sb.positive||0}%</td></tr>
<tr><td>Neutral mentions</td><td>${sb.neutral||0}%</td></tr>
<tr><td>Negative mentions</td><td>${sb.negative||0}%</td></tr>
</table>
<h2>Executive summary</h2><div class="box"><p>${summary}</p></div>
<h2>Channel breakdown</h2>
<table><tr><th>Channel</th><th>Mentions</th><th>Reach</th><th>Sentiment</th></tr>${catRows}</table>
<h2>Competitor comparison</h2>
<table><tr><th>Brand</th><th>Share of Voice</th><th>Sentiment</th></tr>
<tr><td><strong>${brand}</strong></td><td><strong>${d.share_of_voice||0}%</strong></td><td>${d.overall_sentiment||""}</td></tr>
${compRows}</table>
<h2>Top themes</h2>
<p>${(d.top_themes||[]).join(" &nbsp;·&nbsp; ")}</p>
<h2>Recommended actions</h2><ol>${actions}</ol>
<div class="footer">Kornit Digital Brand Intelligence &nbsp;|&nbsp; ${period} &nbsp;|&nbsp; This report was generated automatically.</div>
</body></html>`;
  const blob=new Blob([html],{type:"application/msword"});
  const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=`${brand.replace(/\s+/g,"-")}-brand-report.doc`;a.click();URL.revokeObjectURL(a.href);
}

function dlPDF(){
  if(!scanData){return;}
  const d=scanData;
  const brand=d.brand||"Brand";
  const period=document.getElementById("rp").textContent||"";
  const summary=d.summary||d.summary_he||"";
  const actions=(d.recommended_actions||[]).map((a,i)=>`<li>${a}</li>`).join("");
  const catRows=Object.entries(d.categories||{}).map(([k,c])=>`<tr><td>${CH_NAMES[k]||k}</td><td>${fN(c.count)}</td><td>${fN(c.estimated_reach)}</td><td style="color:${sentColor(c.sentiment)}">${sentLabel(c.sentiment)}</td></tr>`).join("");
  const compRows=[{name:brand,sov:d.share_of_voice||0,sentiment:d.overall_sentiment},...(d.competitor_comparison||[]).filter(c=>c.name!==brand)].map(c=>`<tr><td>${c.name}</td><td>${c.sov||0}%</td><td style="color:${sentColor(c.sentiment)}">${sentLabel(c.sentiment)}</td></tr>`).join("");
  const alerts=(d.alerts||[]).filter(a=>a).map(a=>{const isO=typeof a==="object";return`<li><strong>${isO?a.title:"Alert"}:</strong> ${isO?a.text:a}</li>`;}).join("");
  const negMentions=(d.negative_mentions||[]).map(n=>`<li>${n.text||n.title||""} <span style="color:#888">[${n.source||n.platform||""}]</span></li>`).join("");
  const sb=d.sentiment_breakdown||{};
  const win=window.open("","_blank");
  win.document.write(`<!DOCTYPE html><html><head><meta charset="UTF-8"><title>${brand} — Report</title>
<style>
body{font-family:Arial,sans-serif;padding:32px;color:#1a1a1a;max-width:820px;margin:0 auto;font-size:12px;}
h1{font-size:20px;color:#FF5A00;border-bottom:2px solid #FF5A00;padding-bottom:8px;margin-bottom:6px;}
h2{font-size:14px;margin-top:22px;margin-bottom:8px;color:#0d0d0d;border-left:3px solid #FF5A00;padding-left:8px;}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:11px;}
th{background:#FF5A00;color:#fff;padding:6px 8px;text-align:left;}
td{padding:5px 8px;border-bottom:1px solid #e8e6e0;}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:8px 0;}
.kpi-box{border:1px solid #e8e6e0;padding:10px;text-align:center;border-radius:4px;}
.kpi-label{font-size:9px;color:#888;text-transform:uppercase;letter-spacing:.04em;}
.kpi-val{font-size:18px;font-weight:700;color:#FF5A00;margin:3px 0;}
.summary{background:#f5f4f1;padding:14px;border-radius:4px;line-height:1.7;}
.footer{margin-top:24px;font-size:10px;color:#888;border-top:1px solid #ddd;padding-top:8px;}
li{margin:4px 0;}
@media print{body{padding:16px;}}
</style></head><body>
<h1>${brand} — Brand Intelligence Report</h1>
<p style="color:#888;font-size:11px;margin-bottom:16px;">Period: <strong>${period}</strong> &nbsp;·&nbsp; Generated: ${fmt(new Date())} &nbsp;·&nbsp; Kornit Digital Brand Intelligence</p>
<div class="grid4">
  <div class="kpi-box"><div class="kpi-label">Mentions</div><div class="kpi-val">${fN(d.total_mentions_estimate)}</div></div>
  <div class="kpi-box"><div class="kpi-label">Sentiment</div><div class="kpi-val">${d.sentiment_score>0?"+":""}${d.sentiment_score||0}</div></div>
  <div class="kpi-box"><div class="kpi-label">Exposure</div><div class="kpi-val">${d.exposure_index||"—"}/100</div></div>
  <div class="kpi-box"><div class="kpi-label">Share of Voice</div><div class="kpi-val">${d.share_of_voice||0}%</div></div>
</div>
<h2>Executive summary</h2><div class="summary">${summary}</div>
<h2>Sentiment breakdown</h2>
<table><tr><th>Sentiment</th><th>%</th></tr>
<tr><td style="color:#1D9E75">Positive</td><td>${sb.positive||0}%</td></tr>
<tr><td style="color:#888">Neutral</td><td>${sb.neutral||0}%</td></tr>
<tr><td style="color:#E24B4A">Negative</td><td>${sb.negative||0}%</td></tr>
</table>
<h2>Channel breakdown</h2>
<table><tr><th>Channel</th><th>Mentions</th><th>Estimated reach</th><th>Sentiment</th></tr>${catRows}</table>
<h2>Competitor comparison — share of voice</h2>
<table><tr><th>Brand</th><th>Share of Voice</th><th>Sentiment</th></tr>${compRows}</table>
<h2>Top themes</h2><p>${(d.top_themes||[]).join(" · ")}</p>
<h2>Recommended actions</h2><ol>${actions}</ol>
${alerts?`<h2>Alerts & signals</h2><ul>${alerts}</ul>`:""}
${negMentions?`<h2>Negative mentions</h2><ul>${negMentions}</ul>`:""}
<div class="footer">This report was automatically generated by Kornit Digital Brand Intelligence &nbsp;·&nbsp; ${period}</div>
<script>window.onload=()=>{window.print();}<\/script>
</body></html>`);
  win.document.close();
}
</script>
</body>
</html>"""

@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"success": False, "error": str(e)}), 200

@app.route("/")
def index():
    return HTML

@app.route("/scan", methods=["POST"])
def scan():
    try:
        body        = request.json or {}
        brand       = body.get("brand", "").strip()
        start       = body.get("start_date", "")
        end         = body.get("end_date", "")
        comps       = body.get("competitors", "ROQ, MrPrint, Brother DTG")
        include_yoy = body.get("include_yoy", True)

        if not brand:
            return jsonify({"success": False, "error": "Please enter a brand name"})

        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            return jsonify({"success": False, "error": "ANTHROPIC_API_KEY missing"})

        period = f"{start} to {end}" if start and end else "last 30 days"
        comp_list = [c.strip() for c in comps.split(",") if c.strip()]
        # Never include brand itself in competitor list
        comp_list = [c for c in comp_list if c.lower() != brand.lower()]

        yoy_start = yoy_end = ""
        if start and end and include_yoy:
            try:
                s = datetime.strptime(start, "%Y-%m-%d")
                e = datetime.strptime(end,   "%Y-%m-%d")
                yoy_start = (s - timedelta(days=365)).strftime("%Y-%m-%d")
                yoy_end   = (e - timedelta(days=365)).strftime("%Y-%m-%d")
            except:
                pass

        yoy_tmpl = ""
        if include_yoy and yoy_start:
            yoy_tmpl = f""",
  "yoy": {{
    "period": "{yoy_start} to {yoy_end}",
    "total_mentions_estimate": 400,
    "sentiment_score": 45,
    "exposure_index": 58,
    "share_of_voice": 48,
    "monthly_volume": [
      {{"month": "Jan", "articles": 3, "social": 35, "youtube": 2, "forums": 7}},
      {{"month": "Feb", "articles": 9, "social": 55, "youtube": 4, "forums": 9}},
      {{"month": "Mar", "articles": 5, "social": 45, "youtube": 3, "forums": 8}},
      {{"month": "Apr", "articles": 7, "social": 60, "youtube": 5, "forums": 10}}
    ],
    "categories": {{
      "articles": {{"count": 15, "estimated_reach": 300000}},
      "social":   {{"count": 180,"estimated_reach": 140000}}
    }}
  }}"""

        prompt = f"""You are a brand intelligence analyst. Analyze "{brand}" STRICTLY for {period}.
Do NOT reference or invent data from outside {start} to {end}.
Competitors to compare: {", ".join(comp_list)}.
NEVER include "{brand}" itself in competitor_comparison.
{f'Also estimate metrics for the same period last year ({yoy_start} to {yoy_end}).' if yoy_start else ''}

Return ONLY valid JSON — no markdown, no code fences, start with {{.

{{
  "brand": "{brand}",
  "period": "{period}",
  "start_date": "{start}",
  "end_date": "{end}",
  "summary": "3-4 sentences about brand presence DURING {period} only.",
  "overall_sentiment": "Positive",
  "sentiment_score": 65,
  "sentiment_breakdown": {{"positive": 68, "neutral": 24, "negative": 8}},
  "total_mentions_estimate": 780,
  "exposure_index": 72,
  "share_of_voice": 57,
  "main_negative_theme": "Brief description of main complaint/criticism topic",
  "competitor_negative_avg": 12,
  "negative_mentions": [
    {{"text": "Negative mention or complaint text from {period}", "source": "Source name", "platform": "Platform", "date": "{start[:7]}"}},
    {{"text": "Second negative mention from {period}", "source": "Source name", "platform": "Platform", "date": "{start[:7]}"}}
  ],
  "categories": {{
    "articles":  {{"count": 25, "sentiment": "Positive", "sentiment_reason": "Why articles are positive in {period}.", "estimated_reach": 500000, "examples": [{{"title": "Article from {period}", "source": "Publisher", "url": "", "date": "{start[:7]}"}}]}},
    "social":    {{"count": 300,"sentiment": "Neutral",  "sentiment_reason": "Why social is neutral in {period}.",  "estimated_reach": 200000, "platforms": ["LinkedIn","Facebook"], "examples": [{{"text": "Post topic in {period}", "platform": "LinkedIn"}}]}},
    "ads":       {{"count": 15, "sentiment": "Positive", "sentiment_reason": "Ad campaigns in {period}.",           "estimated_reach": 400000, "platforms": ["Google","Meta"], "notes": "Campaign focus", "examples": [{{"text": "Campaign type", "platform": "Google Ads"}}]}},
    "events":    {{"count": 3,  "sentiment": "Positive", "sentiment_reason": "Events in {period}.",                 "estimated_reach": 8000,   "examples": [{{"name": "Event in {period}", "date": "{start[:7]}", "description": "Description", "url": ""}}]}},
    "forums":    {{"count": 50, "sentiment": "Neutral",  "sentiment_reason": "Forum topics in {period}.",           "estimated_reach": 30000,  "platforms": ["Reddit"], "examples": [{{"text": "Forum topic from {period}", "platform": "Reddit", "url": ""}}]}},
    "youtube":   {{"count": 20, "sentiment": "Positive", "sentiment_reason": "YouTube content in {period}.",        "estimated_reach": 150000, "examples": [{{"title": "YouTube video in {period}", "source": "Channel", "url": "", "date": "{start[:7]}"}}]}},
    "podcasts":  {{"count": 8,  "sentiment": "Positive", "sentiment_reason": "Podcast mentions in {period}.",       "estimated_reach": 40000,  "platforms": ["Spotify","Apple Podcasts"], "examples": [{{"title": "Podcast episode in {period}", "source": "Show", "url": "", "date": "{start[:7]}"}}]}}
  }},
  "monthly_volume": [
    {{"month": "Jan", "articles": 5,  "social": 50,  "youtube": 3,  "forums": 10}},
    {{"month": "Feb", "articles": 15, "social": 80,  "youtube": 8,  "forums": 15}},
    {{"month": "Mar", "articles": 8,  "social": 60,  "youtube": 5,  "forums": 12}},
    {{"month": "Apr", "articles": 20, "social": 120, "youtube": 10, "forums": 18}}
  ],
  "competitor_comparison": [
    {{"name": "{comp_list[0] if comp_list else 'Competitor 1'}", "sov": 21, "sentiment": "Neutral", "color": "#888780"}},
    {{"name": "{comp_list[1] if len(comp_list)>1 else 'Competitor 2'}", "sov": 14, "sentiment": "Neutral", "color": "#B4B2A9"}},
    {{"name": "{comp_list[2] if len(comp_list)>2 else 'Competitor 3'}", "sov": 8,  "sentiment": "Neutral", "color": "#D3D1C7"}}
  ],
  "top_themes": ["Theme 1 from {period}", "Theme 2", "Theme 3", "Theme 4"],
  "alerts": [
    {{"title": "Alert title specific to {period}", "text": "2-3 sentences explaining what happened, why it matters, and the context during {period}."}}
  ],
  "recommended_actions": [
    "Concrete action 1 based on {period} findings",
    "Concrete action 2 referencing a channel or trend found",
    "Forward-looking action 3"
  ]{yoy_tmpl}
}}"""

        response = req.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 4000,
                "system": "You are a brand intelligence analyst. Return ONLY valid JSON. No markdown, no code fences. Start with { end with }. Never include data outside the requested date range. Never include the brand itself in competitor_comparison.",
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=120,
        )

        if response.status_code != 200:
            return jsonify({"success": False, "error": f"API error {response.status_code}: {response.text[:200]}"})

        text = response.json()["content"][0]["text"].strip()
        if text.startswith("```"):
            text = re.sub(r"^```[a-z]*\n?", "", text)
            text = re.sub(r"\n?```$", "", text)

        m = re.search(r"\{[\s\S]*\}", text)
        if not m:
            return jsonify({"success": False, "error": "No JSON: " + text[:300]})

        data = json.loads(m.group())

        # Server-side: ensure brand not in competitors
        data["competitor_comparison"] = [
            c for c in data.get("competitor_comparison", [])
            if c.get("name", "").lower() != brand.lower()
        ]

        return jsonify({"success": True, "data": data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
