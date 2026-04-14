import os, json, re
from flask import Flask, render_template, request, jsonify
import anthropic

app = Flask(__name__)

def get_client():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY not set")
    return anthropic.Anthropic(api_key=key)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    try:
        body   = request.json or {}
        brand  = body.get("brand", "").strip()
        start  = body.get("start_date", "")
        end    = body.get("end_date", "")
        comps  = body.get("competitors", "")

        if not brand:
            return jsonify({"success": False, "error": "נא להזין שם מותג"})

        period = f"{start} עד {end}" if start and end else "30 הימים האחרונים"
        comp_line = f'\nSearch also for: {comps} and compare mention share.' if comps else ""

        SYSTEM = """You are a professional brand intelligence analyst.
Search the web comprehensively and return ONLY valid JSON — no markdown, no code fences.
Begin your response with { and end with }.
Write summary_he in Hebrew. All field names stay in English."""

        USER = f"""Search the web for all mentions of "{brand}" during: {period}.{comp_line}

Do at least 5 searches covering: news/press, social media, ads/campaigns, events, forums/communities.

Return ONLY this JSON structure (start directly with {{):
{{
  "brand": "{brand}",
  "period": "{period}",
  "summary_he": "3-4 משפטים בעברית על נוכחות המותג בתקופה",
  "overall_sentiment": "חיובי",
  "sentiment_score": 65,
  "sentiment_breakdown": {{"positive": 68, "neutral": 24, "negative": 8}},
  "total_mentions_estimate": 500,
  "exposure_index": 72,
  "share_of_voice": 34,
  "categories": {{
    "articles": {{
      "count": 25,
      "sentiment": "חיובי",
      "estimated_reach": 500000,
      "examples": [{{"title": "כותרת", "source": "מקור", "url": "https://...", "date": "2026-01-10"}}]
    }},
    "social": {{
      "count": 300,
      "sentiment": "ניטרלי",
      "estimated_reach": 200000,
      "platforms": ["LinkedIn", "Facebook"],
      "examples": [{{"text": "תוכן", "platform": "LinkedIn"}}]
    }},
    "ads": {{
      "count": 10,
      "sentiment": "חיובי",
      "estimated_reach": 300000,
      "platforms": ["Google", "Meta"],
      "notes": "תיאור קצר"
    }},
    "events": {{
      "count": 3,
      "sentiment": "חיובי",
      "estimated_reach": 5000,
      "examples": [{{"name": "שם אירוע", "date": "2026-01-20", "description": "תיאור"}}]
    }},
    "forums": {{
      "count": 50,
      "sentiment": "ניטרלי",
      "estimated_reach": 30000,
      "platforms": ["Reddit"],
      "examples": [{{"text": "תוכן", "platform": "Reddit"}}]
    }}
  }},
  "monthly_volume": [
    {{"month": "Jan", "articles": 5, "social": 50, "forums": 10}},
    {{"month": "Feb", "articles": 8, "social": 80, "forums": 15}},
    {{"month": "Mar", "articles": 6, "social": 60, "forums": 12}},
    {{"month": "Apr", "articles": 12, "social": 120, "forums": 20}}
  ],
  "top_themes": ["נושא 1", "נושא 2", "נושא 3", "נושא 4"],
  "alerts": [],
  "recommended_actions": ["פעולה 1", "פעולה 2", "פעולה 3"]
}}"""

        client = get_client()
        messages = [{"role": "user", "content": USER}]

        for _ in range(12):
            resp = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=4000,
                system=SYSTEM,
                tools=[{"type": "web_search_20250305", "name": "web_search"}],
                messages=messages,
            )

            messages.append({"role": "assistant", "content": resp.content})

            if resp.stop_reason == "end_turn":
                text = "".join(
                    b.text for b in resp.content if hasattr(b, "text") and b.type == "text"
                )
                m = re.search(r"\{[\s\S]*\}", text)
                if m:
                    data = json.loads(m.group())
                    return jsonify({"success": True, "data": data})
                return jsonify({"success": False, "error": "לא נמצא JSON בתשובה"})

            if resp.stop_reason == "tool_use":
                tool_results = [
                    {"type": "tool_result", "tool_use_id": b.id, "content": "done"}
                    for b in resp.content
                    if hasattr(b, "type") and b.type == "tool_use"
                ]
                if tool_results:
                    messages.append({"role": "user", "content": tool_results})

        return jsonify({"success": False, "error": "הסריקה לקחה יותר מדי זמן"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
