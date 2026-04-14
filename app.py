import os, json, re, requests as req
from flask import Flask, request, jsonify

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>מנוע ניטור מותג</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root{--bg:#f8f7f4;--surface:#fff;--surface2:#f1efe8;--border:rgba(0,0,0,0.1);--text:#1a1a1a;--muted:#6b6b68;--green:#1D9E75;--blue:#378ADD;--amber:#BA7517;--red:#E24B4A;--radius:12px;--rsm:8px;}
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:-apple-system,'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}
  .app{max-width:1100px;margin:0 auto;padding:2rem 1.5rem;}
  .hdr{margin-bottom:2rem;} .hdr p.lbl{font-size:11px;color:var(--muted);letter-spacing:.1em;margin-bottom:4px;} .hdr h1{font-size:24px;font-weight:600;} .hdr .sub{font-size:13px;color:var(--muted);margin-top:2px;}
  .fc{background:var(--surface);border-radius:var(--radius);border:1px solid var(--border);padding:1.5rem;margin-bottom:1.5rem;}
  .fg{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:12px;margin-bottom:12px;}
  .fl label{display:block;font-size:12px;color:var(--muted);margin-bottom:4px;}
  .fl input{width:100%;padding:9px 12px;border:1px solid var(--border);border-radius:var(--rsm);font-size:14px;background:var(--bg);color:var(--text);outline:none;transition:border .15s;}
  .fl input:focus{border-color:var(--green);}
  .bp{width:100%;padding:11px;background:var(--green);color:#fff;border:none;border-radius:var(--rsm);font-size:14px;font-weight:500;cursor:pointer;transition:opacity .15s;}
  .bp:hover{opacity:.88;} .bs{padding:9px 20px;background:transparent;color:var(--text);border:1px solid var(--border);border-radius:var(--rsm);font-size:14px;cursor:pointer;}
  .bs:hover{background:var(--surface2);}
  .ld{text-align:center;padding:4rem 1rem;} .dots{display:flex;justify-content:center;gap:8px;margin-bottom:1rem;} .dot{width:8px;height:8px;border-radius:50%;background:var(--green);animation:pulse 1.2s ease-in-out infinite;} .dot:nth-child(2){animation-delay:.2s;} .dot:nth-child(3){animation-delay:.4s;}
  @keyframes pulse{0%,100%{opacity:.25;transform:scale(.7)}50%{opacity:1;transform:scale(1)}}
  .ld p{color:var(--muted);font-size:14px;}
  .eb{background:#fcebeb;border:1px solid #f09595;border-radius:var(--radius);padding:1rem 1.25rem;margin-bottom:1rem;color:#501313;font-size:14px;}
  .rh{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.25rem;flex-wrap:wrap;gap:8px;}
  .rt h2{font-size:20px;font-weight:600;} .rt p{font-size:13px;color:var(--muted);margin-top:2px;}
  .badge{display:inline-flex;align-items:center;gap:6px;padding:5px 14px;border-radius:100px;font-size:12px;font-weight:500;}
  .kg{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-bottom:1.25rem;}
  .kpi{background:var(--surface2);border-radius:var(--rsm);padding:.875rem;} .kl{font-size:11px;color:var(--muted);margin-bottom:5px;} .kv{font-size:22px;font-weight:600;} .ks{font-size:11px;color:var(--muted);margin-top:2px;}
  .cr{display:grid;grid-template-columns:1.6fr 1fr;gap:12px;margin-bottom:12px;}
  .card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem;}
  .ct{font-size:11px;font-weight:600;color:var(--muted);letter-spacing:.06em;text-transform:uppercase;margin-bottom:1rem;}
  .leg{display:flex;flex-direction:column;gap:6px;margin-top:10px;} .li{display:flex;justify-content:space-between;align-items:center;font-size:12px;} .ld2{width:8px;height:8px;border-radius:50%;margin-left:6px;}
  .sb{margin-bottom:10px;} .sbl{display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;} .bt{height:6px;background:var(--surface2);border-radius:3px;overflow:hidden;} .bf{height:100%;border-radius:3px;}
  .ar{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px;}
  .sumbox{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem;margin-bottom:12px;} .sumbox p{font-size:14px;line-height:1.7;}
  .albox{background:#faeeda;border:1px solid #fac775;border-radius:var(--radius);padding:1rem 1.25rem;margin-bottom:12px;} .altit{font-size:12px;font-weight:600;color:#412402;margin-bottom:4px;}
  .ex{padding:8px 0;border-bottom:1px solid var(--border);} .ex:last-child{border-bottom:none;} .ex a{color:var(--blue);text-decoration:none;font-size:13px;} .ex a:hover{text-decoration:underline;} .ex span{font-size:13px;} .exs{font-size:11px;color:var(--muted);margin-top:2px;}
  .fn{font-size:11px;color:var(--muted);text-align:center;padding:1rem 0;border-top:1px solid var(--border);margin-top:1.5rem;}
  .tp{display:inline-flex;align-items:center;gap:5px;background:var(--surface2);border-radius:100px;padding:4px 10px;font-size:12px;margin:0 4px 4px 0;}
  .hidden{display:none!important;}
  @media(max-width:768px){.fg{grid-template-columns:1fr 1fr;}.kg{grid-template-columns:repeat(2,1fr);}.cr,.ar{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="app">
  <div class="hdr">
    <p class="lbl">BRAND INTELLIGENCE</p>
    <h1>מנוע ניטור מותג</h1>
    <p class="sub">סרוק מה נאמר על המותג שלך — לפי תקופה, לפי ערוץ, לפי סנטימנט</p>
  </div>
  <div class="fc" id="fs">
    <div class="fg">
      <div class="fl"><label>שם המותג / חברה</label><input id="brand" type="text" placeholder="לדוג׳: Kornit, אורנג׳, Wolt..."/></div>
      <div class="fl"><label>מתאריך</label><input id="sd" type="date"/></div>
      <div class="fl"><label>עד תאריך</label><input id="ed" type="date"/></div>
      <div class="fl"><label>מתחרים (אופציונלי)</label><input id="comp" type="text" placeholder="לדוג׳: Epson, Brother"/></div>
    </div>
    <button class="bp" onclick="startScan()">הפעל סריקה →</button>
  </div>
  <div id="ls" class="hidden ld"><div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div><p id="lm">מנתח נתונים...</p></div>
  <div id="es" class="hidden eb"></div>
  <div id="rs" class="hidden">
    <div class="rh"><div class="rt"><h2 id="rb"></h2><p id="rp"></p></div><div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;"><span id="sb2" class="badge"></span><button class="bs" onclick="newScan()">סריקה חדשה</button></div></div>
    <div class="kg"><div class="kpi"><div class="kl">אזכורים סה"כ</div><div class="kv" id="km">—</div></div><div class="kpi"><div class="kl">חשיפה כוללת</div><div class="kv" id="kr">—</div></div><div class="kpi"><div class="kl">ציון סנטימנט</div><div class="kv" id="ksc">—</div></div><div class="kpi"><div class="kl">Exposure Index</div><div class="kv" id="ke">—</div></div><div class="kpi"><div class="kl">Share of Voice</div><div class="kv" id="ksv">—</div></div></div>
    <div class="cr"><div class="card"><div class="ct">עוצמת כיסוי לאורך הזמן</div><canvas id="tc" height="140"></canvas></div><div class="card"><div class="ct">התפלגות חשיפה לפי ערוץ</div><canvas id="dc" height="160"></canvas><div class="leg" id="dl"></div></div></div>
    <div class="ar"><div class="card"><div class="ct">ניתוח סנטימנט</div><div id="sbars"></div><div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--border);"><div style="font-size:11px;color:var(--muted);margin-bottom:6px;">נושאים מובילים</div><div id="themes"></div></div></div><div class="card"><div class="ct">פירוט לפי ערוץ</div><div id="cl"></div></div><div class="card"><div class="ct">פעולות מומלצות</div><div id="al2"></div></div></div>
    <div class="sumbox"><div class="ct" style="margin-bottom:.5rem;">סיכום מנהלים</div><p id="st"></p></div>
    <div id="albox" class="hidden albox"><div class="altit">התראות</div><div id="alist"></div></div>
    <div class="card" style="margin-bottom:12px;"><div class="ct">דוגמאות מובילות</div><div id="exs"></div></div>
    <div class="fn">ניתוח מבוסס על מידע זמין · Brand Intelligence Engine</div>
  </div>
</div>
<script>
let tC=null,dC=null;
const LOADS=["מנתח נוכחות מותג...","בודק כיסוי תקשורתי...","מעריך נוכחות ברשתות...","מחשב חשיפה...","מסכם ממצאים..."];
const CN={articles:"כתבות ופרסום",social:"רשתות חברתיות",ads:"מודעות",events:"אירועים",forums:"פורומים"};
const CL={articles:"#1D9E75",social:"#378ADD",ads:"#BA7517",events:"#534AB7",forums:"#888780"};
function fN(n){if(!n&&n!==0)return"—";if(n>=1e6)return(n/1e6).toFixed(1)+"M";if(n>=1e3)return Math.round(n/1e3)+"K";return String(Math.round(n));}
function show(id){document.getElementById(id).classList.remove("hidden");}
function hide(id){document.getElementById(id).classList.add("hidden");}
const today=new Date(),month=new Date();month.setDate(today.getDate()-30);
document.getElementById("ed").value=today.toISOString().split("T")[0];
document.getElementById("sd").value=month.toISOString().split("T")[0];
async function startScan(){
  const brand=document.getElementById("brand").value.trim();
  if(!brand){alert("נא להזין שם מותג");return;}
  hide("fs");hide("es");hide("rs");show("ls");
  let li=0;const lt=setInterval(()=>{li=(li+1)%LOADS.length;document.getElementById("lm").textContent=LOADS[li];},2000);
  try{
    const r=await fetch("/scan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({brand,start_date:document.getElementById("sd").value,end_date:document.getElementById("ed").value,competitors:document.getElementById("comp").value.trim()})});
    const txt=await r.text();
    clearInterval(lt);hide("ls");
    let result;
    try{result=JSON.parse(txt);}catch(e){throw new Error("שגיאת שרת: "+txt.substring(0,200));}
    if(!result.success)throw new Error(result.error||"שגיאה לא ידועה");
    render(result.data);
  }catch(err){clearInterval(lt);hide("ls");show("fs");document.getElementById("es").textContent="שגיאה: "+err.message;show("es");}
}
function newScan(){hide("rs");show("fs");if(tC){tC.destroy();tC=null;}if(dC){dC.destroy();dC=null;}}
function render(d){
  const cats=d.categories||{};
  document.getElementById("rb").textContent=d.brand||"";
  document.getElementById("rp").textContent=d.period||"";
  const sm={"חיובי":{bg:"#e1f5ee",c:"#085041"},"ניטרלי":{bg:"#faeeda",c:"#412402"},"שלילי":{bg:"#fcebeb",c:"#501313"}};
  const sc=sm[d.overall_sentiment]||sm["ניטרלי"];
  const sb=document.getElementById("sb2");sb.style.background=sc.bg;sb.style.color=sc.c;
  sb.innerHTML=`<span style="width:6px;height:6px;border-radius:50%;background:currentColor;display:inline-block;"></span> סנטימנט ${d.overall_sentiment||""}`;
  const tr=Object.values(cats).reduce((s,c)=>s+(c.estimated_reach||0),0);
  document.getElementById("km").textContent=fN(d.total_mentions_estimate);
  document.getElementById("kr").textContent=fN(tr);
  const sc2=d.sentiment_score||0;const se=document.getElementById("ksc");se.textContent=(sc2>0?"+":"")+Math.round(sc2);se.style.color=sc2>30?"#1D9E75":sc2<-30?"#E24B4A":"#BA7517";
  document.getElementById("ke").textContent=(d.exposure_index||"—")+(d.exposure_index?"/100":"");
  document.getElementById("ksv").textContent=(d.share_of_voice||"—")+(d.share_of_voice?"%":"");
  const mv=d.monthly_volume||[];
  if(tC)tC.destroy();
  tC=new Chart(document.getElementById("tc"),{type:"bar",data:{labels:mv.map(m=>m.month),datasets:[{label:"כתבות",data:mv.map(m=>m.articles||0),backgroundColor:"#1D9E75",borderRadius:3},{label:"סושיאל",data:mv.map(m=>m.social||0),backgroundColor:"#378ADD",borderRadius:3},{label:"פורומים",data:mv.map(m=>m.forums||0),backgroundColor:"#BA7517",borderRadius:3}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{grid:{color:"rgba(0,0,0,0.05)"},beginAtZero:true}},animation:{duration:600}}});
  const cks=Object.keys(cats);const cd=cks.map(k=>cats[k].estimated_reach||0);const cc=cks.map(k=>CL[k]||"#888");
  if(dC)dC.destroy();
  dC=new Chart(document.getElementById("dc"),{type:"doughnut",data:{labels:cks.map(k=>CN[k]||k),datasets:[{data:cd,backgroundColor:cc,borderWidth:0,hoverOffset:4}]},options:{responsive:true,cutout:"68%",plugins:{legend:{display:false}},animation:{duration:600}}});
  const tl=cd.reduce((a,b)=>a+b,0)||1;
  document.getElementById("dl").innerHTML=cks.map((k,i)=>`<div class="li"><div style="display:flex;align-items:center;"><div class="ld2" style="background:${cc[i]};"></div>${CN[k]||k}</div><span style="font-weight:500;">${Math.round((cd[i]/tl)*100)}%</span></div>`).join("");
  const sb3=d.sentiment_breakdown||{positive:60,neutral:30,negative:10};
  document.getElementById("sbars").innerHTML=`<div class="sb"><div class="sbl"><span>חיובי</span><span style="color:#1D9E75;font-weight:500;">${sb3.positive||0}%</span></div><div class="bt"><div class="bf" style="width:${sb3.positive||0}%;background:#1D9E75;"></div></div></div><div class="sb"><div class="sbl"><span>ניטרלי</span><span style="font-weight:500;">${sb3.neutral||0}%</span></div><div class="bt"><div class="bf" style="width:${sb3.neutral||0}%;background:#888780;"></div></div></div><div class="sb"><div class="sbl"><span>שלילי</span><span style="color:#E24B4A;font-weight:500;">${sb3.negative||0}%</span></div><div class="bt"><div class="bf" style="width:${sb3.negative||0}%;background:#E24B4A;"></div></div></div>`;
  document.getElementById("themes").innerHTML=(d.top_themes||[]).map(t=>`<span class="tp"><span style="width:5px;height:5px;border-radius:50%;background:#1D9E75;display:inline-block;"></span>${t}</span>`).join("");
  document.getElementById("cl").innerHTML=cks.map(k=>{const c=cats[k];const sc4=c.sentiment==="חיובי"?"#1D9E75":c.sentiment==="שלילי"?"#E24B4A":"#BA7517";return`<div style="display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid var(--border);"><div style="display:flex;align-items:center;gap:7px;"><div style="width:8px;height:8px;border-radius:50%;background:${CL[k]||'#888'};"></div><span style="font-size:13px;">${CN[k]||k}</span></div><div><span style="font-size:13px;font-weight:500;">${fN(c.count)}</span><span style="font-size:11px;color:var(--muted);margin-right:6px;"> · ${fN(c.estimated_reach)}</span><span style="font-size:11px;color:${sc4};">${c.sentiment||""}</span></div></div>`;}).join("");
  const ac=["#1D9E75","#378ADD","#534AB7"];
  document.getElementById("al2").innerHTML=(d.recommended_actions||[]).map((a,i)=>`<div style="display:flex;gap:8px;align-items:flex-start;margin-bottom:12px;"><div style="min-width:22px;height:22px;border-radius:50%;background:${ac[i]||'#888'};color:#fff;font-size:11px;font-weight:600;display:flex;align-items:center;justify-content:center;">${i+1}</div><span style="font-size:13px;line-height:1.5;">${a}</span></div>`).join("");
  document.getElementById("st").textContent=d.summary_he||"";
  const alerts=(d.alerts||[]).filter(a=>a);
  if(alerts.length){document.getElementById("alist").innerHTML=alerts.map(a=>`<div style="font-size:13px;color:#412402;">${a}</div>`).join("");show("albox");}else hide("albox");
  let exH="";
  for(const[k,cat]of Object.entries(cats)){const exs=cat.examples;if(!exs||!exs.length)continue;exH+=`<div style="margin-bottom:1rem;"><div style="font-size:11px;font-weight:600;color:var(--muted);margin-bottom:5px;">${CN[k]||k}</div>`;exs.slice(0,2).forEach(ex=>{const label=ex.title||ex.text||ex.name||"";const sub=ex.source||ex.platform||ex.date||"";const url=ex.url&&ex.url.startsWith("http")?ex.url:null;exH+=`<div class="ex">${url?`<a href="${url}" target="_blank">${label}</a>`:`<span>${label}</span>`}${sub?`<div class="exs">${sub}</div>`:""}</div>`;});exH+="</div>";}
  document.getElementById("exs").innerHTML=exH||"<p style='font-size:13px;color:var(--muted);'>לא נמצאו דוגמאות</p>";
  show("rs");
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
        comps = body.get("competitors", "")

        if not brand:
            return jsonify({"success": False, "error": "נא להזין שם מותג"})

        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            return jsonify({"success": False, "error": "ANTHROPIC_API_KEY חסר"})

        period  = f"{start} עד {end}" if start and end else "30 הימים האחרונים"
        comp_ln = f"\nגם השווה למתחרים: {comps}." if comps else ""

        prompt = f"""נתח את נוכחות המותג "{brand}" בתקופה: {period}.{comp_ln}

החזר אך ורק JSON תקין (התחל ישירות עם {{, ללא markdown):
{{
  "brand": "{brand}",
  "period": "{period}",
  "summary_he": "3-4 משפטים בעברית על נוכחות המותג",
  "overall_sentiment": "חיובי",
  "sentiment_score": 65,
  "sentiment_breakdown": {{"positive": 68, "neutral": 24, "negative": 8}},
  "total_mentions_estimate": 500,
  "exposure_index": 72,
  "share_of_voice": 34,
  "categories": {{
    "articles": {{"count": 25, "sentiment": "חיובי", "estimated_reach": 500000, "examples": [{{"title": "כותרת", "source": "מקור", "url": "", "date": "2026-01"}}]}},
    "social": {{"count": 300, "sentiment": "ניטרלי", "estimated_reach": 200000, "platforms": ["LinkedIn"], "examples": [{{"text": "תוכן", "platform": "LinkedIn"}}]}},
    "ads": {{"count": 10, "sentiment": "חיובי", "estimated_reach": 300000, "platforms": ["Google"], "notes": "תיאור"}},
    "events": {{"count": 3, "sentiment": "חיובי", "estimated_reach": 5000, "examples": [{{"name": "אירוע", "date": "2026-01", "description": "תיאור"}}]}},
    "forums": {{"count": 50, "sentiment": "ניטרלי", "estimated_reach": 30000, "platforms": ["Reddit"], "examples": [{{"text": "תוכן", "platform": "Reddit"}}]}}
  }},
  "monthly_volume": [
    {{"month": "Jan", "articles": 5, "social": 50, "forums": 10}},
    {{"month": "Feb", "articles": 8, "social": 80, "forums": 15}},
    {{"month": "Mar", "articles": 6, "social": 60, "forums": 12}},
    {{"month": "Apr", "articles": 12, "social": 120, "forums": 20}}
  ],
  "top_themes": ["נושא 1", "נושא 2", "נושא 3"],
  "alerts": [],
  "recommended_actions": ["פעולה 1", "פעולה 2", "פעולה 3"]
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
                "max_tokens": 3000,
                "system": "אתה אנליסט בינה מותגית. ענה אך ורק ב-JSON תקין ללא markdown. התחל עם { וסיים עם }.",
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
            return jsonify({"success": False, "error": "לא נמצא JSON. תשובה: " + text[:300]})

        data = json.loads(m.group())
        return jsonify({"success": True, "data": data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
