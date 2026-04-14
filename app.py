import os, json, re
from flask import Flask, request, jsonify
import anthropic

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>מנוע ניטור מותג</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {
    --bg:#f8f7f4;--surface:#ffffff;--surface2:#f1efe8;--border:rgba(0,0,0,0.1);
    --text:#1a1a1a;--muted:#6b6b68;--green:#1D9E75;--green-bg:#e1f5ee;--green-text:#085041;
    --blue:#378ADD;--amber:#BA7517;--amber-bg:#faeeda;--amber-text:#412402;
    --red:#E24B4A;--red-bg:#fcebeb;--red-text:#501313;--purple:#534AB7;
    --radius:12px;--radius-sm:8px;
  }
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:-apple-system,'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}
  .app{max-width:1100px;margin:0 auto;padding:2rem 1.5rem;}
  .header{margin-bottom:2rem;}
  .header p.label{font-size:11px;color:var(--muted);letter-spacing:.1em;margin-bottom:4px;}
  .header h1{font-size:24px;font-weight:600;}
  .header .sub{font-size:13px;color:var(--muted);margin-top:2px;}
  .form-card{background:var(--surface);border-radius:var(--radius);border:1px solid var(--border);padding:1.5rem;margin-bottom:1.5rem;}
  .form-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:12px;margin-bottom:12px;}
  .form-group label{display:block;font-size:12px;color:var(--muted);margin-bottom:4px;}
  .form-group input{width:100%;padding:9px 12px;border:1px solid var(--border);border-radius:var(--radius-sm);font-size:14px;background:var(--bg);color:var(--text);outline:none;transition:border .15s;}
  .form-group input:focus{border-color:var(--green);}
  .btn-primary{width:100%;padding:11px;background:var(--green);color:white;border:none;border-radius:var(--radius-sm);font-size:14px;font-weight:500;cursor:pointer;transition:opacity .15s;}
  .btn-primary:hover{opacity:.88;}
  .btn-secondary{padding:9px 20px;background:transparent;color:var(--text);border:1px solid var(--border);border-radius:var(--radius-sm);font-size:14px;cursor:pointer;}
  .btn-secondary:hover{background:var(--surface2);}
  .loading{text-align:center;padding:4rem 1rem;}
  .dots{display:flex;justify-content:center;gap:8px;margin-bottom:1rem;}
  .dot{width:8px;height:8px;border-radius:50%;background:var(--green);animation:pulse 1.2s ease-in-out infinite;}
  .dot:nth-child(2){animation-delay:.2s;} .dot:nth-child(3){animation-delay:.4s;}
  @keyframes pulse{0%,100%{opacity:.25;transform:scale(.7)}50%{opacity:1;transform:scale(1)}}
  .loading p{color:var(--muted);font-size:14px;}
  .error-box{background:var(--red-bg);border:1px solid #f09595;border-radius:var(--radius);padding:1rem 1.25rem;margin-bottom:1rem;color:var(--red-text);font-size:14px;}
  .res-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.25rem;flex-wrap:wrap;gap:8px;}
  .res-title h2{font-size:20px;font-weight:600;}
  .res-title p{font-size:13px;color:var(--muted);margin-top:2px;}
  .badge{display:inline-flex;align-items:center;gap:6px;padding:5px 14px;border-radius:100px;font-size:12px;font-weight:500;}
  .kpi-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-bottom:1.25rem;}
  .kpi{background:var(--surface2);border-radius:var(--radius-sm);padding:.875rem;}
  .kpi .kl{font-size:11px;color:var(--muted);margin-bottom:5px;}
  .kpi .kv{font-size:22px;font-weight:600;}
  .kpi .ks{font-size:11px;color:var(--muted);margin-top:2px;}
  .charts-row{display:grid;grid-template-columns:1.6fr 1fr;gap:12px;margin-bottom:12px;}
  .card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem;}
  .ct{font-size:11px;font-weight:600;color:var(--muted);letter-spacing:.06em;text-transform:uppercase;margin-bottom:1rem;}
  .legend{display:flex;flex-direction:column;gap:6px;margin-top:10px;}
  .legend-item{display:flex;justify-content:space-between;align-items:center;font-size:12px;}
  .ldot{width:8px;height:8px;border-radius:50%;margin-left:6px;}
  .sent-bar{margin-bottom:10px;}
  .sbl{display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;}
  .bt{height:6px;background:var(--surface2);border-radius:3px;overflow:hidden;}
  .bf{height:100%;border-radius:3px;}
  .analysis-row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px;}
  .summary-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem;margin-bottom:12px;}
  .summary-box p{font-size:14px;line-height:1.7;}
  .alert-box{background:var(--amber-bg);border:1px solid #fac775;border-radius:var(--radius);padding:1rem 1.25rem;margin-bottom:12px;}
  .alert-title{font-size:12px;font-weight:600;color:var(--amber-text);margin-bottom:4px;}
  .example-item{padding:8px 0;border-bottom:1px solid var(--border);}
  .example-item:last-child{border-bottom:none;}
  .example-title a{color:var(--blue);text-decoration:none;font-size:13px;}
  .example-title a:hover{text-decoration:underline;}
  .example-title span{font-size:13px;}
  .example-sub{font-size:11px;color:var(--muted);margin-top:2px;}
  .footer-note{font-size:11px;color:var(--muted);text-align:center;padding:1rem 0;border-top:1px solid var(--border);margin-top:1.5rem;}
  .theme-pill{display:inline-flex;align-items:center;gap:5px;background:var(--surface2);border-radius:100px;padding:4px 10px;font-size:12px;margin:0 4px 4px 0;}
  .hidden{display:none!important;}
  @media(max-width:768px){.form-grid{grid-template-columns:1fr 1fr;}.kpi-grid{grid-template-columns:repeat(2,1fr);}.charts-row,.analysis-row{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="app">
  <div class="header">
    <p class="label">BRAND INTELLIGENCE</p>
    <h1>מנוע ניטור מותג</h1>
    <p class="sub">סרוק מה נאמר על המותג שלך — לפי תקופה, לפי ערוץ, לפי סנטימנט</p>
  </div>

  <div class="form-card" id="form-section">
    <div class="form-grid">
      <div class="form-group"><label>שם המותג / חברה</label><input id="brand" type="text" placeholder="לדוג׳: Kornit, אורנג׳, Wolt..." /></div>
      <div class="form-group"><label>מתאריך</label><input id="sd" type="date" /></div>
      <div class="form-group"><label>עד תאריך</label><input id="ed" type="date" /></div>
      <div class="form-group"><label>מתחרים (אופציונלי)</label><input id="comp" type="text" placeholder="לדוג׳: Epson, Brother" /></div>
    </div>
    <button class="btn-primary" onclick="startScan()">הפעל סריקה →</button>
  </div>

  <div id="loading-section" class="hidden loading">
    <div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
    <p id="load-msg">מאתר מידע ברחבי הרשת...</p>
  </div>

  <div id="error-section" class="hidden error-box"></div>

  <div id="results-section" class="hidden">
    <div class="res-header">
      <div class="res-title"><h2 id="res-brand"></h2><p id="res-period"></p></div>
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
        <span id="sent-badge" class="badge"></span>
        <button class="btn-secondary" onclick="newScan()">סריקה חדשה</button>
      </div>
    </div>
    <div class="kpi-grid">
      <div class="kpi"><div class="kl">אזכורים סה"כ</div><div class="kv" id="k-ment">—</div></div>
      <div class="kpi"><div class="kl">חשיפה כוללת</div><div class="kv" id="k-reach">—</div></div>
      <div class="kpi"><div class="kl">ציון סנטימנט</div><div class="kv" id="k-score">—</div></div>
      <div class="kpi"><div class="kl">Exposure Index</div><div class="kv" id="k-exp">—</div></div>
      <div class="kpi"><div class="kl">Share of Voice</div><div class="kv" id="k-sov">—</div></div>
    </div>
    <div class="charts-row">
      <div class="card"><div class="ct">עוצמת כיסוי לאורך הזמן</div><canvas id="timeline-chart" height="140"></canvas></div>
      <div class="card"><div class="ct">התפלגות חשיפה לפי ערוץ</div><canvas id="donut-chart" height="160"></canvas><div class="legend" id="donut-legend"></div></div>
    </div>
    <div class="analysis-row">
      <div class="card">
        <div class="ct">ניתוח סנטימנט</div>
        <div id="sent-bars"></div>
        <div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--border);">
          <div style="font-size:11px;color:var(--muted);margin-bottom:6px;">נושאים מובילים</div>
          <div id="themes"></div>
        </div>
      </div>
      <div class="card"><div class="ct">פירוט לפי ערוץ</div><div id="cat-list"></div></div>
      <div class="card"><div class="ct">פעולות מומלצות</div><div id="actions-list"></div></div>
    </div>
    <div class="summary-box"><div class="ct" style="margin-bottom:.5rem;">סיכום מנהלים</div><p id="summary-text"></p></div>
    <div id="alerts-section" class="hidden alert-box"><div class="alert-title">התראות</div><div id="alerts-list"></div></div>
    <div class="card" style="margin-bottom:12px;"><div class="ct">דוגמאות מובילות</div><div id="examples"></div></div>
    <div class="footer-note">נתונים מבוססים על חיפוש רשת בזמן אמת · Brand Intelligence Engine</div>
  </div>
</div>

<script>
let tChart=null,dChart=null;
const LOADS=["מחפש כתבות ומאמרים...","סורק רשתות חברתיות...","מנתח מודעות ופרסומות...","בודק פורומים וקהילות...","מעריך אירועים רלוונטיים...","מסכם ומנתח נתונים..."];
const CNAMES={articles:"כתבות ופרסום",social:"רשתות חברתיות",ads:"מודעות",events:"אירועים",forums:"פורומים"};
const COLORS={articles:"#1D9E75",social:"#378ADD",ads:"#BA7517",events:"#534AB7",forums:"#888780"};
function fN(n){if(!n&&n!==0)return"—";if(n>=1e6)return(n/1e6).toFixed(1)+"M";if(n>=1e3)return Math.round(n/1e3)+"K";return String(Math.round(n));}
function show(id){document.getElementById(id).classList.remove("hidden");}
function hide(id){document.getElementById(id).classList.add("hidden");}
const today=new Date(),month=new Date();month.setDate(today.getDate()-30);
document.getElementById("ed").value=today.toISOString().split("T")[0];
document.getElementById("sd").value=month.toISOString().split("T")[0];

async function startScan(){
  const brand=document.getElementById("brand").value.trim();
  if(!brand){alert("נא להזין שם מותג");return;}
  hide("form-section");hide("error-section");hide("results-section");show("loading-section");
  let li=0;const lt=setInterval(()=>{li=(li+1)%LOADS.length;document.getElementById("load-msg").textContent=LOADS[li];},2500);
  try{
    const r=await fetch("/scan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({brand,start_date:document.getElementById("sd").value,end_date:document.getElementById("ed").value,competitors:document.getElementById("comp").value.trim()})});
    const result=await r.json();
    clearInterval(lt);hide("loading-section");
    if(!result.success)throw new Error(result.error||"שגיאה לא ידועה");
    render(result.data);
  }catch(err){clearInterval(lt);hide("loading-section");show("form-section");const e=document.getElementById("error-section");e.textContent="שגיאה: "+err.message;show("error-section");}
}

function newScan(){hide("results-section");show("form-section");if(tChart){tChart.destroy();tChart=null;}if(dChart){dChart.destroy();dChart=null;}}

function render(d){
  const cats=d.categories||{};
  document.getElementById("res-brand").textContent=d.brand||"";
  document.getElementById("res-period").textContent=d.period||"";
  const sMap={"חיובי":{bg:"#e1f5ee",col:"#085041"},"ניטרלי":{bg:"#faeeda",col:"#412402"},"שלילי":{bg:"#fcebeb",col:"#501313"}};
  const sc=sMap[d.overall_sentiment]||sMap["ניטרלי"];
  const sb=document.getElementById("sent-badge");sb.style.background=sc.bg;sb.style.color=sc.col;
  sb.innerHTML=`<span style="width:6px;height:6px;border-radius:50%;background:currentColor;display:inline-block;"></span> סנטימנט ${d.overall_sentiment||""}`;
  const tr=Object.values(cats).reduce((s,c)=>s+(c.estimated_reach||0),0);
  document.getElementById("k-ment").textContent=fN(d.total_mentions_estimate);
  document.getElementById("k-reach").textContent=fN(tr);
  const sc2=d.sentiment_score||0;const se=document.getElementById("k-score");se.textContent=(sc2>0?"+":"")+Math.round(sc2);se.style.color=sc2>30?"#1D9E75":sc2<-30?"#E24B4A":"#BA7517";
  document.getElementById("k-exp").textContent=(d.exposure_index||"—")+(d.exposure_index?"/100":"");
  document.getElementById("k-sov").textContent=(d.share_of_voice||"—")+(d.share_of_voice?"%":"");
  const mv=d.monthly_volume||[];
  if(tChart)tChart.destroy();
  tChart=new Chart(document.getElementById("timeline-chart"),{type:"bar",data:{labels:mv.map(m=>m.month),datasets:[{label:"כתבות",data:mv.map(m=>m.articles||0),backgroundColor:"#1D9E75",borderRadius:3},{label:"סושיאל",data:mv.map(m=>m.social||0),backgroundColor:"#378ADD",borderRadius:3},{label:"פורומים",data:mv.map(m=>m.forums||0),backgroundColor:"#BA7517",borderRadius:3}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{grid:{color:"rgba(0,0,0,0.05)"},beginAtZero:true}},animation:{duration:600}}});
  const cks=Object.keys(cats);const cd=cks.map(k=>cats[k].estimated_reach||0);const cc=cks.map(k=>COLORS[k]||"#888");
  if(dChart)dChart.destroy();
  dChart=new Chart(document.getElementById("donut-chart"),{type:"doughnut",data:{labels:cks.map(k=>CNAMES[k]||k),datasets:[{data:cd,backgroundColor:cc,borderWidth:0,hoverOffset:4}]},options:{responsive:true,cutout:"68%",plugins:{legend:{display:false}},animation:{duration:600}}});
  const tl=cd.reduce((a,b)=>a+b,0)||1;
  document.getElementById("donut-legend").innerHTML=cks.map((k,i)=>`<div class="legend-item"><div style="display:flex;align-items:center;"><div class="ldot" style="background:${cc[i]};"></div>${CNAMES[k]||k}</div><span style="font-weight:500;">${Math.round((cd[i]/tl)*100)}%</span></div>`).join("");
  const sb2=d.sentiment_breakdown||{positive:60,neutral:30,negative:10};
  document.getElementById("sent-bars").innerHTML=`<div class="sent-bar"><div class="sbl"><span>חיובי</span><span style="color:#1D9E75;font-weight:500;">${sb2.positive||0}%</span></div><div class="bt"><div class="bf" style="width:${sb2.positive||0}%;background:#1D9E75;"></div></div></div><div class="sent-bar"><div class="sbl"><span>ניטרלי</span><span style="font-weight:500;">${sb2.neutral||0}%</span></div><div class="bt"><div class="bf" style="width:${sb2.neutral||0}%;background:#888780;"></div></div></div><div class="sent-bar"><div class="sbl"><span>שלילי</span><span style="color:#E24B4A;font-weight:500;">${sb2.negative||0}%</span></div><div class="bt"><div class="bf" style="width:${sb2.negative||0}%;background:#E24B4A;"></div></div></div>`;
  document.getElementById("themes").innerHTML=(d.top_themes||[]).map(t=>`<span class="theme-pill"><span style="width:5px;height:5px;border-radius:50%;background:#1D9E75;display:inline-block;"></span>${t}</span>`).join("");
  document.getElementById("cat-list").innerHTML=cks.map(k=>{const c=cats[k];const sc3=c.sentiment==="חיובי"?"#1D9E75":c.sentiment==="שלילי"?"#E24B4A":"#BA7517";return`<div style="display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid var(--border);"><div style="display:flex;align-items:center;gap:7px;"><div style="width:8px;height:8px;border-radius:50%;background:${COLORS[k]||'#888'};"></div><span style="font-size:13px;">${CNAMES[k]||k}</span></div><div><span style="font-size:13px;font-weight:500;">${fN(c.count)}</span><span style="font-size:11px;color:var(--muted);margin-right:6px;"> · ${fN(c.estimated_reach)}</span><span style="font-size:11px;color:${sc3};">${c.sentiment||""}</span></div></div>`;}).join("");
  const ac=["#1D9E75","#378ADD","#534AB7"];
  document.getElementById("actions-list").innerHTML=(d.recommended_actions||[]).map((a,i)=>`<div style="display:flex;gap:8px;align-items:flex-start;margin-bottom:12px;"><div style="min-width:22px;height:22px;border-radius:50%;background:${ac[i]||'#888'};color:white;font-size:11px;font-weight:600;display:flex;align-items:center;justify-content:center;">${i+1}</div><span style="font-size:13px;line-height:1.5;">${a}</span></div>`).join("");
  document.getElementById("summary-text").textContent=d.summary_he||"";
  const alerts=(d.alerts||[]).filter(a=>a);
  if(alerts.length){document.getElementById("alerts-list").innerHTML=alerts.map(a=>`<div style="font-size:13px;color:var(--amber-text);">${a}</div>`).join("");show("alerts-section");}else hide("alerts-section");
  let exH="";
  for(const[k,cat]of Object.entries(cats)){const exs=cat.examples;if(!exs||!exs.length)continue;exH+=`<div style="margin-bottom:1rem;"><div style="font-size:11px;font-weight:600;color:var(--muted);margin-bottom:5px;">${CNAMES[k]||k}</div>`;exs.slice(0,2).forEach(ex=>{const label=ex.title||ex.text||ex.name||"";const sub=ex.source||ex.platform||ex.date||"";const url=ex.url&&ex.url.startsWith("http")?ex.url:null;exH+=`<div class="example-item"><div class="example-title">${url?`<a href="${url}" target="_blank">${label}</a>`:`<span>${label}</span>`}</div>${sub?`<div class="example-sub">${sub}</div>`:""}</div>`;});exH+="</div>";}
  document.getElementById("examples").innerHTML=exH||"<p style='font-size:13px;color:var(--muted);'>לא נמצאו דוגמאות</p>";
  show("results-section");
}
</script>
</body>
</html>"""

@app.route("/")
def index():
    return HTML

@app.route("/scan", methods=["POST"])
def scan():
    try:
        body  = request.json or {}
        brand = body.get("brand","").strip()
        start = body.get("start_date","")
        end   = body.get("end_date","")
        comps = body.get("competitors","")
        if not brand:
            return jsonify({"success":False,"error":"נא להזין שם מותג"})
        period   = f"{start} עד {end}" if start and end else "30 הימים האחרונים"
        comp_ln  = f"\nAlso compare with competitors: {comps}." if comps else ""
        SYSTEM = "You are a brand intelligence analyst. Search the web and return ONLY valid JSON. No markdown, no code fences. Start with { end with }."
        USER = f"""Search the web for all mentions of "{brand}" during: {period}.{comp_ln}
Do at least 5 searches: news, social media, ads, events, forums.
Return ONLY this JSON (start with {{):
{{"brand":"{brand}","period":"{period}","summary_he":"3-4 משפטים בעברית","overall_sentiment":"חיובי","sentiment_score":65,"sentiment_breakdown":{{"positive":68,"neutral":24,"negative":8}},"total_mentions_estimate":500,"exposure_index":72,"share_of_voice":34,"categories":{{"articles":{{"count":25,"sentiment":"חיובי","estimated_reach":500000,"examples":[{{"title":"כותרת","source":"מקור","url":"https://...","date":"2026-01-10"}}]}},"social":{{"count":300,"sentiment":"ניטרלי","estimated_reach":200000,"platforms":["LinkedIn"],"examples":[{{"text":"תוכן","platform":"LinkedIn"}}]}},"ads":{{"count":10,"sentiment":"חיובי","estimated_reach":300000,"platforms":["Google"],"notes":"תיאור"}},"events":{{"count":3,"sentiment":"חיובי","estimated_reach":5000,"examples":[{{"name":"שם","date":"2026-01","description":"תיאור"}}]}},"forums":{{"count":50,"sentiment":"ניטרלי","estimated_reach":30000,"platforms":["Reddit"],"examples":[{{"text":"תוכן","platform":"Reddit"}}]}}}},"monthly_volume":[{{"month":"Jan","articles":5,"social":50,"forums":10}},{{"month":"Feb","articles":8,"social":80,"forums":15}},{{"month":"Mar","articles":6,"social":60,"forums":12}},{{"month":"Apr","articles":12,"social":120,"forums":20}}],"top_themes":["נושא 1","נושא 2","נושא 3"],"alerts":[],"recommended_actions":["פעולה 1","פעולה 2","פעולה 3"]}}"""
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            return jsonify({"success":False,"error":"ANTHROPIC_API_KEY לא מוגדר — ראו הוראות התקנה"})
        client   = anthropic.Anthropic(api_key=key)
        messages = [{"role":"user","content":USER}]
        for _ in range(12):
            resp = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=4000,
                system=SYSTEM,
                tools=[{"type":"web_search_20250305","name":"web_search"}],
                messages=messages
            )
            messages.append({"role":"assistant","content":resp.content})
            if resp.stop_reason == "end_turn":
                text = "".join(b.text for b in resp.content if hasattr(b,"text") and b.type=="text")
                m = re.search(r"\{[\s\S]*\}",text)
                if m:
                    return jsonify({"success":True,"data":json.loads(m.group())})
                return jsonify({"success":False,"error":"לא נמצא JSON בתשובה"})
            if resp.stop_reason == "tool_use":
                trs=[{"type":"tool_result","tool_use_id":b.id,"content":"done"} for b in resp.content if hasattr(b,"type") and b.type=="tool_use"]
                if trs:
                    messages.append({"role":"user","content":trs})
        return jsonify({"success":False,"error":"הסריקה לקחה יותר מדי זמן"})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
