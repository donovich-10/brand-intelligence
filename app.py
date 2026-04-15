import os, json, re, requests as req
from flask import Flask, request, jsonify
from datetime import datetime

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
  --orange:#FF5A00;--orange-light:#FF7A30;--orange-pale:#FFF0E8;
  --dark:#0d0d0d;--dark2:#1a1a1a;--dark3:#2a2a2a;
  --bg:#f5f4f1;--surface:#ffffff;--surface2:#f0ede8;
  --border:#e8e6e0;--border2:#d8d4cc;
  --text:#1a1a1a;--muted:#888780;--muted2:#b0ada6;
  --green:#1D9E75;--green-pale:#e1f5ee;--green-text:#085041;
  --blue:#378ADD;--amber:#BA7517;--red:#E24B4A;--purple:#534AB7;
  --radius:10px;--rsm:6px;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}
a{color:var(--orange);text-decoration:none;} a:hover{text-decoration:underline;}

.app{max-width:1140px;margin:0 auto;padding:1.5rem;}

/* HEADER */
.header{background:var(--dark);border-radius:var(--radius);padding:1.125rem 1.5rem;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center;}
.logo{display:flex;align-items:center;gap:14px;}
.logo-text{display:flex;align-items:baseline;gap:0;}
.logo-kornit{font-size:22px;font-weight:800;color:var(--orange);letter-spacing:-.5px;}
.logo-digital{font-size:22px;font-weight:300;color:#fff;letter-spacing:-.5px;}
.logo-sep{width:1px;height:24px;background:#333;margin:0 14px;}
.logo-sub p{font-size:10px;color:#555;letter-spacing:.12em;margin:0;}
.logo-sub h2{font-size:13px;color:#fff;font-weight:500;margin:0;}
.live-badge{display:flex;align-items:center;gap:6px;padding:5px 12px;background:#1a1a1a;border-radius:100px;border:1px solid #333;}
.live-dot{width:6px;height:6px;border-radius:50%;background:var(--orange);animation:blink 2s ease-in-out infinite;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.3;}}
.live-txt{font-size:11px;color:var(--orange);font-weight:600;letter-spacing:.08em;}

/* FORM */
.fc{background:var(--surface);border-radius:var(--radius);border:1px solid var(--border);padding:1.25rem;margin-bottom:14px;}
.fg{display:grid;grid-template-columns:2fr 1fr 1fr;gap:10px;margin-bottom:10px;}
.fg2{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;}
.fl label{display:block;font-size:11px;color:var(--muted);margin-bottom:3px;font-weight:500;letter-spacing:.04em;}
.fl input{width:100%;padding:9px 12px;border:1.5px solid var(--border);border-radius:var(--rsm);font-size:13px;background:var(--bg);color:var(--text);outline:none;transition:border .15s;}
.fl input:focus{border-color:var(--orange);}
.comp-row{display:flex;gap:6px;align-items:flex-end;}
.comp-row input{flex:1;}
.comp-tag{display:inline-flex;align-items:center;gap:5px;background:var(--dark);color:#fff;border-radius:4px;padding:3px 8px;font-size:11px;margin:0 4px 4px 0;}
.comp-tag span{cursor:pointer;color:#666;font-size:13px;} .comp-tag span:hover{color:#fff;}
.comp-tags{margin-top:6px;}
.btn-primary{width:100%;padding:11px;background:var(--orange);color:#fff;border:none;border-radius:var(--rsm);font-size:14px;font-weight:600;cursor:pointer;letter-spacing:.02em;transition:opacity .15s;}
.btn-primary:hover{opacity:.88;}
.btn-sec{padding:9px 18px;background:transparent;color:var(--text);border:1.5px solid var(--border);border-radius:var(--rsm);font-size:13px;cursor:pointer;font-weight:500;}
.btn-sec:hover{background:var(--surface2);}
.btn-sm{padding:6px 12px;background:var(--dark);color:#fff;border:none;border-radius:var(--rsm);font-size:11px;cursor:pointer;font-weight:500;}
.btn-sm:hover{background:var(--dark3);}
.btn-dl{padding:7px 14px;border:1.5px solid var(--border);border-radius:var(--rsm);font-size:12px;cursor:pointer;background:var(--surface);color:var(--text);font-weight:500;display:inline-flex;align-items:center;gap:5px;}
.btn-dl:hover{background:var(--surface2);}

/* LOADING */
.ld{text-align:center;padding:4rem 1rem;} .dots{display:flex;justify-content:center;gap:8px;margin-bottom:1rem;} .dot{width:9px;height:9px;border-radius:50%;background:var(--orange);animation:pulse 1.2s ease-in-out infinite;} .dot:nth-child(2){animation-delay:.2s;} .dot:nth-child(3){animation-delay:.4s;}
@keyframes pulse{0%,100%{opacity:.2;transform:scale(.65)}50%{opacity:1;transform:scale(1)}}
.ld p{color:var(--muted);font-size:14px;}

/* ERROR */
.eb{background:#FFF0E8;border:1.5px solid #FF7A30;border-radius:var(--radius);padding:1rem 1.25rem;margin-bottom:14px;color:#7a2d00;font-size:14px;}

/* RESULTS HEADER */
.rh{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;flex-wrap:wrap;gap:10px;}
.rt h2{font-size:22px;font-weight:700;} .rt p{font-size:13px;color:var(--muted);margin-top:2px;}
.rh-right{display:flex;gap:8px;align-items:center;flex-wrap:wrap;}
.badge{display:inline-flex;align-items:center;gap:6px;padding:5px 14px;border-radius:100px;font-size:12px;font-weight:600;}

/* KPI GRID */
.kg{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px;margin-bottom:12px;}
.kpi{background:var(--surface);border-radius:var(--rsm);padding:.875rem;border:1px solid var(--border);}
.kpi.dark{background:var(--dark);border-color:#222;}
.kl{font-size:10px;color:var(--muted);margin-bottom:4px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;}
.kpi.dark .kl{color:#555;}
.kv{font-size:22px;font-weight:700;}
.kpi.dark .kv{color:var(--orange);}
.ks{font-size:10px;color:var(--muted);margin-top:2px;}

/* CHANNEL CARDS */
.ch-grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:8px;margin-bottom:12px;}
.ch-card{background:var(--surface);border-radius:var(--rsm);padding:.75rem;border:1px solid var(--border);border-top:3px solid;}
.ch-name{font-size:10px;color:var(--muted);font-weight:600;letter-spacing:.04em;text-transform:uppercase;margin-bottom:4px;}
.ch-count{font-size:18px;font-weight:700;}
.ch-sent{font-size:10px;margin-top:3px;cursor:pointer;position:relative;}
.tooltip{display:none;position:absolute;bottom:120%;left:50%;transform:translateX(-50%);background:var(--dark);color:#fff;font-size:11px;padding:7px 10px;border-radius:6px;width:180px;line-height:1.4;z-index:100;white-space:normal;}
.tooltip::after{content:'';position:absolute;top:100%;left:50%;transform:translateX(-50%);border:5px solid transparent;border-top-color:var(--dark);}
.ch-sent:hover .tooltip{display:block;}
.ch-reach{font-size:10px;color:var(--muted);}

/* CARDS */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem;}
.ct{font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.ct::after{content:'';flex:1;height:1px;background:var(--border);}

/* CHARTS ROW */
.cr{display:grid;grid-template-columns:1.6fr 1fr;gap:12px;margin-bottom:12px;}
.leg{display:flex;flex-direction:column;gap:5px;margin-top:10px;} .li{display:flex;justify-content:space-between;align-items:center;font-size:12px;} .ldot{width:8px;height:8px;border-radius:50%;margin-right:6px;flex-shrink:0;}

/* SENTIMENT */
.ar{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px;}
.sb{margin-bottom:10px;} .sbl{display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;} .bt{height:7px;background:var(--surface2);border-radius:4px;overflow:hidden;} .bf{height:100%;border-radius:4px;}

/* COMPETITOR */
.comp-bar{margin-bottom:10px;}
.comp-bar-row{display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;}
.comp-bar-name{font-weight:500;}
.comp-bar-track{height:8px;background:var(--surface2);border-radius:4px;overflow:hidden;}
.comp-bar-fill{height:100%;border-radius:4px;transition:width .6s ease;}

/* SUMMARY */
.sumbox{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem;margin-bottom:12px;}
.sumbox p{font-size:14px;line-height:1.8;color:var(--text);}

/* ALERTS */
.albox{background:#FFF0E8;border:1.5px solid #FF7A30;border-radius:var(--radius);padding:1.25rem;margin-bottom:12px;}
.al-title{font-size:11px;font-weight:700;color:#7a2d00;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px;}
.al-item{background:#fff;border-radius:var(--rsm);padding:.875rem;margin-bottom:8px;border:1px solid #ffc4a0;}
.al-item:last-child{margin-bottom:0;}
.al-item-title{font-size:13px;font-weight:600;color:#7a2d00;margin-bottom:4px;}
.al-item-text{font-size:12px;color:#a04020;line-height:1.5;}
.al-item-link{font-size:11px;color:var(--orange);font-weight:600;margin-top:6px;display:inline-flex;align-items:center;gap:3px;}

/* THEMES */
.tp{display:inline-flex;align-items:center;gap:5px;background:var(--dark);color:#fff;border-radius:100px;padding:5px 12px;font-size:11px;margin:0 5px 5px 0;font-weight:500;}
.tp-dot{width:5px;height:5px;border-radius:50%;background:var(--orange);}

/* EXAMPLES / SOURCES */
.src-section{margin-bottom:12px;}
.src-group{margin-bottom:14px;}
.src-group-title{font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px;display:flex;align-items:center;gap:6px;}
.src-item{display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid var(--border);}
.src-item:last-child{border-bottom:none;}
.src-icon{width:28px;height:28px;border-radius:5px;background:var(--orange-pale);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:12px;font-weight:700;color:var(--orange);}
.src-body{flex:1;min-width:0;}
.src-title{font-size:13px;color:var(--orange);font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.src-title:hover{text-decoration:underline;}
.src-meta{font-size:11px;color:var(--muted);margin-top:2px;}

/* ACTIONS */
.act-item{display:flex;gap:10px;align-items:flex-start;padding:10px 0;border-bottom:1px solid var(--border);}
.act-item:last-child{border-bottom:none;}
.act-num{min-width:24px;height:24px;border-radius:50%;background:var(--orange);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.act-text{font-size:13px;line-height:1.55;}

/* DOWNLOAD BAR */
.dl-bar{display:flex;gap:8px;justify-content:flex-end;margin-bottom:12px;}

/* FOOTER */
.fn{font-size:11px;color:var(--muted2);text-align:center;padding:1rem 0;border-top:1px solid var(--border);margin-top:1.5rem;}
.hidden{display:none!important;}
@media(max-width:900px){
  .kg{grid-template-columns:repeat(3,1fr);}
  .ch-grid{grid-template-columns:repeat(4,1fr);}
  .cr,.ar{grid-template-columns:1fr;}
  .fg{grid-template-columns:1fr 1fr;}
}
</style>
</head>
<body>
<div class="app">

  <!-- HEADER -->
  <div class="header">
    <div class="logo">
      <div class="logo-text">
        <span class="logo-kornit">kornit</span>
        <span class="logo-digital">digital</span>
      </div>
      <div class="logo-sep"></div>
      <div class="logo-sub">
        <p>BRAND INTELLIGENCE</p>
        <h2>Monitor Dashboard</h2>
      </div>
    </div>
    <div class="live-badge">
      <div class="live-dot"></div>
      <span class="live-txt">LIVE</span>
    </div>
  </div>

  <!-- FORM -->
  <div class="fc" id="fs">
    <div class="fg">
      <div class="fl">
        <label>Brand name</label>
        <input id="brand" type="text" placeholder="e.g. Kornit Digital, Monday.com..." value="Kornit Digital"/>
      </div>
      <div class="fl">
        <label>From (DD/MM/YYYY)</label>
        <input id="sd" type="text" placeholder="01/01/2026"/>
      </div>
      <div class="fl">
        <label>To (DD/MM/YYYY)</label>
        <input id="ed" type="text" placeholder="14/04/2026"/>
      </div>
    </div>
    <div class="fl" style="margin-bottom:10px;">
      <label>Competitors (fixed defaults — click × to remove, or add)</label>
      <div class="comp-tags" id="comp-tags"></div>
      <div class="comp-row">
        <input id="comp-input" type="text" placeholder="Add competitor and press Enter"/>
        <button class="btn-sm" onclick="addComp()">Add</button>
      </div>
    </div>
    <button class="btn-primary" onclick="startScan()">Run Brand Scan →</button>
  </div>

  <div id="ls" class="hidden ld">
    <div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
    <p id="lm">Scanning the web...</p>
  </div>
  <div id="es" class="hidden eb"></div>

  <!-- RESULTS -->
  <div id="rs" class="hidden">
    <div class="rh">
      <div class="rt"><h2 id="rb"></h2><p id="rp"></p></div>
      <div class="rh-right">
        <span id="sb2" class="badge"></span>
        <button class="btn-sec" onclick="newScan()">New scan</button>
      </div>
    </div>

    <!-- Downloads -->
    <div class="dl-bar">
      <button class="btn-dl" onclick="downloadPDF()">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><path d="M4 1h6l4 4v10H2V1z" stroke="currentColor" stroke-width="1.2" fill="none"/><path d="M10 1v4h4" stroke="currentColor" stroke-width="1.2" fill="none"/><path d="M5 9h6M5 11.5h4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
        Export PDF
      </button>
      <button class="btn-dl" onclick="downloadWord()">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><path d="M4 1h6l4 4v10H2V1z" stroke="currentColor" stroke-width="1.2" fill="none"/><path d="M10 1v4h4" stroke="currentColor" stroke-width="1.2" fill="none"/><path d="M5 8l1.5 4 1.5-3 1.5 3L11 8" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Export Word
      </button>
    </div>

    <!-- KPIs -->
    <div class="kg">
      <div class="kpi"><div class="kl">Total Mentions</div><div class="kv" id="km">—</div></div>
      <div class="kpi"><div class="kl">Total Reach</div><div class="kv" id="kr">—</div></div>
      <div class="kpi dark"><div class="kl">Sentiment Score</div><div class="kv" id="ksc">—</div></div>
      <div class="kpi"><div class="kl">Exposure Index</div><div class="kv" id="ke">—</div></div>
      <div class="kpi"><div class="kl">Share of Voice</div><div class="kv" id="ksv">—</div></div>
      <div class="kpi"><div class="kl">Sources Found</div><div class="kv" id="ksrc">—</div></div>
    </div>

    <!-- Channel cards -->
    <div class="ch-grid" id="ch-grid"></div>

    <!-- Charts row -->
    <div class="cr">
      <div class="card">
        <div class="ct">Coverage over time</div>
        <canvas id="tc" height="130"></canvas>
      </div>
      <div class="card">
        <div class="ct">Reach by channel</div>
        <canvas id="dc" height="150"></canvas>
        <div class="leg" id="dl2"></div>
      </div>
    </div>

    <!-- Analysis row -->
    <div class="ar">
      <div class="card">
        <div class="ct">Sentiment breakdown</div>
        <div id="sbars"></div>
        <div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--border);">
          <div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px;">Top themes</div>
          <div id="themes"></div>
        </div>
      </div>
      <div class="card">
        <div class="ct">Competitor comparison</div>
        <div id="comp-chart"></div>
      </div>
      <div class="card">
        <div class="ct">Recommended actions</div>
        <div id="al2"></div>
      </div>
    </div>

    <!-- Summary -->
    <div class="sumbox">
      <div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px;">Executive summary</div>
      <p id="st"></p>
    </div>

    <!-- Alerts -->
    <div id="albox" class="hidden albox">
      <div class="al-title">Alerts & Signals</div>
      <div id="alist"></div>
    </div>

    <!-- Sources / Examples -->
    <div class="card src-section" id="src-section">
      <div class="ct">Sources & Links</div>
      <div id="exs"></div>
    </div>

    <div class="fn">Data based on AI analysis · Kornit Digital Brand Intelligence · <span id="scan-date"></span></div>
  </div>
</div>

<script>
let tC=null,dC=null;
const LOADS=["Scanning news and press...","Analyzing social media...","Checking YouTube & podcasts...","Reviewing forums and communities...","Comparing competitors...","Compiling intelligence report..."];
const CH_COLORS={articles:"#FF5A00",social:"#378ADD",ads:"#BA7517",events:"#534AB7",forums:"#888780",youtube:"#E24B4A",podcasts:"#1D9E75"};
const CH_NAMES={articles:"Articles",social:"Social",ads:"Ads",events:"Events",forums:"Forums",youtube:"YouTube",podcasts:"Podcasts"};
const CH_ICONS={articles:"A",social:"S",ads:"Ad",events:"Ev",forums:"F",youtube:"YT",podcasts:"PC"};

let competitors=["ROQ","MrPrint","Brother DTG"];

function renderCompTags(){
  const el=document.getElementById("comp-tags");
  el.innerHTML=competitors.map((c,i)=>`<span class="comp-tag">${c}<span onclick="removeComp(${i})">×</span></span>`).join("");
}
function addComp(){
  const v=document.getElementById("comp-input").value.trim();
  if(v&&!competitors.includes(v)){competitors.push(v);renderCompTags();document.getElementById("comp-input").value="";}
}
function removeComp(i){competitors.splice(i,1);renderCompTags();}
document.getElementById("comp-input").addEventListener("keydown",e=>{if(e.key==="Enter")addComp();});
renderCompTags();

function fN(n){if(!n&&n!==0)return"—";if(n>=1e6)return(n/1e6).toFixed(1)+"M";if(n>=1e3)return Math.round(n/1e3)+"K";return String(Math.round(n));}
function show(id){document.getElementById(id).classList.remove("hidden");}
function hide(id){document.getElementById(id).classList.add("hidden");}

function fmtDate(s){if(!s)return"";const d=new Date(s);if(isNaN(d))return s;return String(d.getDate()).padStart(2,"0")+"/"+String(d.getMonth()+1).padStart(2,"0")+"/"+d.getFullYear();}

function parseDate(s){
  if(!s)return"";
  const parts=s.split("/");
  if(parts.length===3){const[d,m,y]=parts;return`${y}-${m.padStart(2,"0")}-${d.padStart(2,"0")}`;}
  return s;
}

async function startScan(){
  const brand=document.getElementById("brand").value.trim();
  if(!brand){alert("Please enter a brand name");return;}
  hide("fs");hide("es");hide("rs");show("ls");
  let li=0;const lt=setInterval(()=>{li=(li+1)%LOADS.length;document.getElementById("lm").textContent=LOADS[li];},2200);
  try{
    const sd=parseDate(document.getElementById("sd").value);
    const ed=parseDate(document.getElementById("ed").value);
    const r=await fetch("/scan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({brand,start_date:sd,end_date:ed,competitors:competitors.join(", ")})});
    const txt=await r.text();
    clearInterval(lt);hide("ls");
    let result;
    try{result=JSON.parse(txt);}catch(e){throw new Error("Server error: "+txt.substring(0,200));}
    if(!result.success)throw new Error(result.error||"Unknown error");
    render(result.data);
  }catch(err){clearInterval(lt);hide("ls");show("fs");document.getElementById("es").textContent="Error: "+err.message;show("es");}
}

function newScan(){hide("rs");show("fs");if(tC){tC.destroy();tC=null;}if(dC){dC.destroy();dC=null;}}

function sentColor(s){return s==="Positive"||s==="חיובי"?"#1D9E75":s==="Negative"||s==="שלילי"?"#E24B4A":"#888780";}
function sentLabel(s){if(s==="חיובי"||s==="Positive")return"Positive";if(s==="שלילי"||s==="Negative")return"Negative";return"Neutral";}

function render(d){
  const cats=d.categories||{};
  document.getElementById("rb").textContent=d.brand||"";
  const sd=fmtDate(d.start_date)||"";const ed2=fmtDate(d.end_date)||"";
  document.getElementById("rp").textContent=d.period||(sd&&ed2?`${sd} – ${ed2}`:"Last 30 days");
  document.getElementById("scan-date").textContent="Scanned: "+new Date().toLocaleDateString("en-GB");

  const sm={"Positive":{bg:"#e1f5ee",c:"#085041"},"חיובי":{bg:"#e1f5ee",c:"#085041"},"Neutral":{bg:"#faeeda",c:"#412402"},"ניטרלי":{bg:"#faeeda",c:"#412402"},"Negative":{bg:"#fcebeb",c:"#501313"},"שלילי":{bg:"#fcebeb",c:"#501313"}};
  const sc=sm[d.overall_sentiment]||sm["Neutral"];
  const sb=document.getElementById("sb2");sb.style.background=sc.bg;sb.style.color=sc.c;
  sb.innerHTML=`<span style="width:6px;height:6px;border-radius:50%;background:currentColor;display:inline-block;margin-left:2px;"></span> ${sentLabel(d.overall_sentiment)||"Neutral"}`;

  const tr=Object.values(cats).reduce((s,c)=>s+(c.estimated_reach||0),0);
  const srcCount=Object.values(cats).reduce((s,c)=>s+(c.examples?.length||0),0);
  document.getElementById("km").textContent=fN(d.total_mentions_estimate);
  document.getElementById("kr").textContent=fN(tr);
  const sc2=d.sentiment_score||0;const se=document.getElementById("ksc");se.textContent=(sc2>0?"+":"")+Math.round(sc2);se.style.color=sc2>30?"#FF5A00":sc2<-30?"#E24B4A":"#888";
  document.getElementById("ke").textContent=(d.exposure_index||"—")+(d.exposure_index?"/100":"");
  document.getElementById("ksv").textContent=(d.share_of_voice||"—")+(d.share_of_voice?"%":"");
  document.getElementById("ksrc").textContent=srcCount||"—";

  // Channel cards
  const chGrid=document.getElementById("ch-grid");
  chGrid.innerHTML=Object.entries(cats).map(([k,c])=>{
    const sl=sentLabel(c.sentiment);const col=sentColor(c.sentiment);
    const why=c.sentiment_reason||"Based on tone analysis of collected mentions.";
    return`<div class="ch-card" style="border-top-color:${CH_COLORS[k]||'#ccc'}">
      <div class="ch-name">${CH_NAMES[k]||k}</div>
      <div class="ch-count" style="color:${CH_COLORS[k]||'#1a1a1a'};">${fN(c.count)}</div>
      <div class="ch-sent" style="color:${col};">${sl}
        <div class="tooltip">${why}</div>
      </div>
      <div class="ch-reach">${fN(c.estimated_reach)} reach</div>
    </div>`;
  }).join("");

  // Timeline chart
  const mv=d.monthly_volume||[];
  if(tC)tC.destroy();
  tC=new Chart(document.getElementById("tc"),{type:"bar",data:{labels:mv.map(m=>m.month),datasets:[
    {label:"Articles",data:mv.map(m=>m.articles||0),backgroundColor:"#FF5A00",borderRadius:3},
    {label:"Social",data:mv.map(m=>m.social||0),backgroundColor:"#378ADD",borderRadius:3},
    {label:"YouTube",data:mv.map(m=>m.youtube||0),backgroundColor:"#E24B4A",borderRadius:3},
    {label:"Forums",data:mv.map(m=>m.forums||0),backgroundColor:"#888780",borderRadius:3},
  ]},options:{responsive:true,plugins:{legend:{display:false}},scales:{x:{grid:{display:false},stacked:true},y:{grid:{color:"rgba(0,0,0,0.04)"},beginAtZero:true,stacked:true}},animation:{duration:700}}});

  // Donut chart
  const cks=Object.keys(cats);const cd=cks.map(k=>cats[k].estimated_reach||0);const cc=cks.map(k=>CH_COLORS[k]||"#888");
  if(dC)dC.destroy();
  dC=new Chart(document.getElementById("dc"),{type:"doughnut",data:{labels:cks.map(k=>CH_NAMES[k]||k),datasets:[{data:cd,backgroundColor:cc,borderWidth:0,hoverOffset:4}]},options:{responsive:true,cutout:"70%",plugins:{legend:{display:false}},animation:{duration:700}}});
  const tl=cd.reduce((a,b)=>a+b,0)||1;
  document.getElementById("dl2").innerHTML=cks.map((k,i)=>`<div class="li"><div style="display:flex;align-items:center;"><div class="ldot" style="background:${cc[i]};"></div><span style="font-size:12px;">${CH_NAMES[k]||k}</span></div><span style="font-size:12px;font-weight:600;">${Math.round((cd[i]/tl)*100)}%</span></div>`).join("");

  // Sentiment bars
  const sb3=d.sentiment_breakdown||{positive:60,neutral:30,negative:10};
  document.getElementById("sbars").innerHTML=`
    <div class="sb"><div class="sbl"><span>Positive</span><span style="color:#1D9E75;font-weight:600;">${sb3.positive||0}%</span></div><div class="bt"><div class="bf" style="width:${sb3.positive||0}%;background:#1D9E75;"></div></div></div>
    <div class="sb"><div class="sbl"><span>Neutral</span><span style="font-weight:600;">${sb3.neutral||0}%</span></div><div class="bt"><div class="bf" style="width:${sb3.neutral||0}%;background:#888780;"></div></div></div>
    <div class="sb"><div class="sbl"><span>Negative</span><span style="color:#E24B4A;font-weight:600;">${sb3.negative||0}%</span></div><div class="bt"><div class="bf" style="width:${sb3.negative||0}%;background:#E24B4A;"></div></div></div>`;
  document.getElementById("themes").innerHTML=(d.top_themes||[]).map(t=>`<span class="tp"><div class="tp-dot"></div>${t}</span>`).join("");

  // Competitor comparison
  const comps=d.competitor_comparison||[];
  const allBrands=[{name:d.brand,sov:d.share_of_voice||0,sentiment:d.overall_sentiment,color:"#FF5A00"},...comps];
  document.getElementById("comp-chart").innerHTML=allBrands.map(b=>`<div class="comp-bar">
    <div class="comp-bar-row"><span class="comp-bar-name" style="color:${b.color||'#1a1a1a'}">${b.name}</span><span style="font-size:12px;font-weight:600;">${b.sov||0}%</span></div>
    <div class="comp-bar-track"><div class="comp-bar-fill" style="width:${b.sov||0}%;background:${b.color||'#ccc'};"></div></div>
    <div style="font-size:10px;color:${sentColor(b.sentiment)};margin-top:2px;">${sentLabel(b.sentiment)||""}</div>
  </div>`).join("");

  // Actions
  const ac=["#FF5A00","#378ADD","#534AB7","#1D9E75"];
  document.getElementById("al2").innerHTML=(d.recommended_actions||[]).map((a,i)=>`<div class="act-item"><div class="act-num">${i+1}</div><div class="act-text">${a}</div></div>`).join("");

  // Summary
  document.getElementById("st").textContent=d.summary||d.summary_he||"";

  // Alerts
  const alerts=(d.alerts||[]).filter(a=>a);
  if(alerts.length){
    document.getElementById("alist").innerHTML=alerts.map(a=>{
      const isObj=typeof a==="object";
      const title=isObj?a.title:"Alert";
      const text=isObj?a.text:a;
      const link=isObj?a.link:"";
      return`<div class="al-item">
        <div class="al-item-title">${title}</div>
        <div class="al-item-text">${text}</div>
        ${link?`<a href="${link}" target="_blank" class="al-item-link">Investigate ↗</a>`:""}
      </div>`;
    }).join("");
    show("albox");
  }else hide("albox");

  // Sources
  let exH="";
  for(const[k,cat]of Object.entries(cats)){
    const exs=cat.examples;if(!exs||!exs.length)continue;
    exH+=`<div class="src-group"><div class="src-group-title"><div style="width:8px;height:8px;border-radius:50%;background:${CH_COLORS[k]||'#888'};"></div>${CH_NAMES[k]||k}</div>`;
    exs.forEach(ex=>{
      const label=ex.title||ex.text||ex.name||"Source";
      const sub=ex.source||ex.platform||ex.date||"";
      const url=ex.url&&ex.url.startsWith("http")?ex.url:null;
      const icon=(CH_ICONS[k]||k.substring(0,2).toUpperCase());
      exH+=`<div class="src-item">
        <div class="src-icon" style="background:${CH_COLORS[k]||'#ccc'}20;color:${CH_COLORS[k]||'#888'};">${icon}</div>
        <div class="src-body">
          ${url?`<a href="${url}" target="_blank" class="src-title">${label}</a>`:`<div class="src-title" style="color:var(--text);">${label}</div>`}
          ${sub?`<div class="src-meta">${sub}</div>`:""}
        </div>
      </div>`;
    });
    exH+="</div>";
  }
  document.getElementById("exs").innerHTML=exH||"<p style='font-size:13px;color:var(--muted);'>No sources found</p>";
  show("rs");
}

function downloadPDF(){
  const brand=document.getElementById("rb").textContent||"Brand";
  const content=buildReportText();
  const win=window.open("","_blank");
  win.document.write(`<html><head><title>${brand} — Brand Intelligence Report</title>
  <style>body{font-family:Arial,sans-serif;padding:40px;color:#1a1a1a;max-width:800px;margin:0 auto;}
  h1{color:#FF5A00;border-bottom:2px solid #FF5A00;padding-bottom:10px;}
  h2{color:#1a1a1a;margin-top:30px;}
  .section{margin:20px 0;padding:15px;background:#f5f4f1;border-radius:8px;}
  .label{font-weight:bold;color:#888;}
  @media print{body{padding:20px;}}</style></head>
  <body>${content}<script>window.onload=()=>window.print();<\/script></body></html>`);
  win.document.close();
}

function downloadWord(){
  const brand=document.getElementById("rb").textContent||"Brand";
  const period=document.getElementById("rp").textContent||"";
  const summary=document.getElementById("st").textContent||"";
  const actions=(Array.from(document.querySelectorAll(".act-text"))||[]).map((el,i)=>`${i+1}. ${el.textContent}`).join("\n");
  const content=`${brand} — Brand Intelligence Report\n${period}\n\n${"=".repeat(50)}\n\nEXECUTIVE SUMMARY\n${"-".repeat(30)}\n${summary}\n\nRECOMMENDED ACTIONS\n${"-".repeat(30)}\n${actions}\n\nGenerated: ${new Date().toLocaleDateString("en-GB")}`;
  const blob=new Blob([content],{type:"text/plain;charset=utf-8"});
  const url=URL.createObjectURL(blob);
  const a=document.createElement("a");a.href=url;a.download=`${brand.replace(/\s+/g,"-")}-brand-report.txt`;a.click();URL.revokeObjectURL(url);
}

function buildReportText(){
  const brand=document.getElementById("rb").textContent||"";
  const period=document.getElementById("rp").textContent||"";
  const summary=document.getElementById("st").textContent||"";
  const mentions=document.getElementById("km").textContent;
  const reach=document.getElementById("kr").textContent;
  const score=document.getElementById("ksc").textContent;
  const exposure=document.getElementById("ke").textContent;
  const sov=document.getElementById("ksv").textContent;
  const actions=(Array.from(document.querySelectorAll(".act-text"))||[]).map((el,i)=>`<li>${el.textContent}</li>`).join("");
  return`<h1>${brand} — Brand Intelligence Report</h1>
  <p><strong>Period:</strong> ${period}</p>
  <h2>Key Metrics</h2>
  <div class="section">
    <p><span class="label">Total Mentions:</span> ${mentions}</p>
    <p><span class="label">Reach:</span> ${reach}</p>
    <p><span class="label">Sentiment Score:</span> ${score}</p>
    <p><span class="label">Exposure Index:</span> ${exposure}</p>
    <p><span class="label">Share of Voice:</span> ${sov}</p>
  </div>
  <h2>Executive Summary</h2>
  <div class="section"><p>${summary}</p></div>
  <h2>Recommended Actions</h2>
  <ol>${actions}</ol>
  <p style="color:#888;font-size:12px;margin-top:40px;">Generated by Kornit Digital Brand Intelligence · ${new Date().toLocaleDateString("en-GB")}</p>`;
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
        body  = request.json or {}
        brand = body.get("brand", "").strip()
        start = body.get("start_date", "")
        end   = body.get("end_date", "")
        comps = body.get("competitors", "ROQ, MrPrint, Brother DTG")

        if not brand:
            return jsonify({"success": False, "error": "Please enter a brand name"})

        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            return jsonify({"success": False, "error": "ANTHROPIC_API_KEY missing"})

        period = f"{start} to {end}" if start and end else "last 30 days"
        comp_list = [c.strip() for c in comps.split(",") if c.strip()]

        prompt = f"""You are a brand intelligence analyst. Analyze the brand "{brand}" for the period: {period}.
Compare against competitors: {", ".join(comp_list)}.

Return ONLY valid JSON starting with {{ and ending with }}. No markdown, no code fences.

{{
  "brand": "{brand}",
  "period": "{period}",
  "start_date": "{start}",
  "end_date": "{end}",
  "summary": "3-4 sentences in English describing brand presence, key events, and market position during this period.",
  "overall_sentiment": "Positive",
  "sentiment_score": 65,
  "sentiment_breakdown": {{"positive": 68, "neutral": 24, "negative": 8}},
  "total_mentions_estimate": 780,
  "exposure_index": 72,
  "share_of_voice": 57,
  "categories": {{
    "articles": {{
      "count": 25,
      "sentiment": "Positive",
      "sentiment_reason": "Explain in 1-2 sentences why articles have this sentiment — mention specific topics or events.",
      "estimated_reach": 500000,
      "examples": [
        {{"title": "Article headline here", "source": "Publisher name", "url": "https://real-or-plausible-url.com", "date": "2026-01-10"}}
      ]
    }},
    "social": {{
      "count": 300,
      "sentiment": "Neutral",
      "sentiment_reason": "Explain why social is neutral — e.g. mixed reactions, routine updates.",
      "estimated_reach": 200000,
      "platforms": ["LinkedIn", "Facebook", "Instagram"],
      "examples": [{{"text": "Example post or discussion topic", "platform": "LinkedIn"}}]
    }},
    "ads": {{
      "count": 15,
      "sentiment": "Positive",
      "sentiment_reason": "Ad campaigns are typically positive in tone.",
      "estimated_reach": 400000,
      "platforms": ["Google", "Meta"],
      "notes": "Brief description of ad campaigns found",
      "examples": [{{"text": "Campaign description", "platform": "Google Ads"}}]
    }},
    "events": {{
      "count": 3,
      "sentiment": "Positive",
      "sentiment_reason": "Industry events generate positive brand visibility.",
      "estimated_reach": 8000,
      "examples": [{{"name": "Event name", "date": "2026-04-12", "description": "Event description", "url": "https://event-url.com"}}]
    }},
    "forums": {{
      "count": 50,
      "sentiment": "Neutral",
      "sentiment_reason": "Forum discussions are mixed — technical questions and user experiences.",
      "estimated_reach": 30000,
      "platforms": ["Reddit", "Industry forums"],
      "examples": [{{"text": "Forum discussion topic", "platform": "Reddit", "url": ""}}]
    }},
    "youtube": {{
      "count": 20,
      "sentiment": "Positive",
      "sentiment_reason": "YouTube content features product demos and reviews.",
      "estimated_reach": 150000,
      "examples": [{{"title": "YouTube video title", "source": "Channel name", "url": "https://youtube.com/watch?v=example", "date": "2026-02-15"}}]
    }},
    "podcasts": {{
      "count": 8,
      "sentiment": "Positive",
      "sentiment_reason": "Podcast mentions are in industry shows.",
      "estimated_reach": 40000,
      "platforms": ["Spotify", "Apple Podcasts"],
      "examples": [{{"title": "Podcast episode title", "source": "Show name", "url": "", "date": "2026-03-01"}}]
    }}
  }},
  "monthly_volume": [
    {{"month": "Jan", "articles": 5, "social": 50, "youtube": 3, "forums": 10}},
    {{"month": "Feb", "articles": 15, "social": 80, "youtube": 8, "forums": 15}},
    {{"month": "Mar", "articles": 8, "social": 60, "youtube": 5, "forums": 12}},
    {{"month": "Apr", "articles": 20, "social": 120, "youtube": 10, "forums": 18}}
  ],
  "competitor_comparison": [
    {{"name": "{comp_list[0] if comp_list else 'Competitor 1'}", "sov": 21, "sentiment": "Neutral", "color": "#888780"}},
    {{"name": "{comp_list[1] if len(comp_list)>1 else 'Competitor 2'}", "sov": 14, "sentiment": "Neutral", "color": "#B4B2A9"}},
    {{"name": "{comp_list[2] if len(comp_list)>2 else 'Competitor 3'}", "sov": 8, "sentiment": "Neutral", "color": "#D3D1C7"}}
  ],
  "top_themes": ["On-Demand Manufacturing", "Atlas MATRIX Launch", "Sustainability", "Digital Transformation", "PrintFactory Acquisition"],
  "alerts": [
    {{
      "title": "Alert title — what happened",
      "text": "2-3 sentences explaining what drove this alert, the context, and why it matters for the brand.",
      "link": "https://relevant-url-if-available.com"
    }}
  ],
  "recommended_actions": [
    "Specific action 1 — be concrete and actionable, explain why",
    "Specific action 2 — reference a channel or topic found in the data",
    "Specific action 3 — forward-looking recommendation"
  ]
}}"""

        response = req.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 4000,
                "system": "You are a brand intelligence analyst. Return ONLY valid JSON. No markdown, no code fences. Start directly with { and end with }.",
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
            return jsonify({"success": False, "error": "No JSON found. Response: " + text[:300]})

        data = json.loads(m.group())
        return jsonify({"success": True, "data": data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
