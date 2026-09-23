import os
import requests

# متغيرات البيئة الأسرار
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")

TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHANNEL_NICHE = os.getenv("CHANNEL_NICHE", "تخصص عام")

def analyze_youtube():
    if not YOUTUBE_API_KEY or not YOUTUBE_CHANNEL_ID:
        print("معلومات يوتيوب غير متوفرة.")
        return []
    
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={YOUTUBE_CHANNEL_ID}&part=snippet,id&order=date&maxResults=3"
    response = requests.get(url)
    if response.status_code == 200:
        items = response.json().get("items", [])
        return [item["snippet"]["title"] for item in items if item["id"]["kind"] == "youtube#video"]
    return []

def analyze_instagram():
    if not IG_ACCESS_TOKEN or not IG_USER_ID:
        print("معلومات إنستغرام غير متوفرة.")
        return []
    
    url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media?fields=caption,comments_count,like_count&access_token={IG_ACCESS_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("data", [])
        return [post.get("caption", "بدون عنوان") for post in data[:3]]
    return []

def analyze_tiktok():
    if not TIKTOK_ACCESS_TOKEN:
        print("معلومات تيك توك غير متوفرة.")
        return []
    
    headers = {"Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}"}
    url = "https://open.tiktokapis.com/v2/video/list/?fields=cover_url,title,like_count,comment_count"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        videos = response.json().get("data", {}).get("videos", [])
        return [v.get("title", "بدون عنوان") for v in videos[:3]]
    return []

def send_to_gemini(all_data):
    prompt = f"""
    أنت مدير قنواتي على السوشيال ميديا. هذه هي بيانات أداء الفيديوهات الأخيرة عبر منصات يوتيوب، إنستغرام، وتيك توك:
    {all_data}
    
    التخصص الصارم لهذه القناة هو حصرياً: '{CHANNEL_NICHE}'.
    يُمنع منعاً كلياً الخروج عن هذا التخصص.
    قم بتحليل الأداء، واقترح لي 3 أفكار دقيقة لفيديوهات جديدة تتماشى حصرياً مع هذا التخصص وتلبي طلبات المتابعين.
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        print("--- التقرير والأفكار المقترحة من المدير الآلي ---")
        print(result["candidates"][0]["content"]["parts"][0]["text"])
    else:
        print("خطأ في الاتصال بـ Gemini API")

if __name__ == "__main__":
    print(f"--- بدء تحليل القنوات المنصات الثلاث للتخصص: {CHANNEL_NICHE} ---")
    yt_data = analyze_youtube()
    ig_data = analyze_instagram()
    tt_data = analyze_tiktok()
    
    combined_data = {
        "YouTube": yt_data,
        "Instagram": ig_data,
        "TikTok": tt_data
    }
    
    send_to_gemini(combined_data)
