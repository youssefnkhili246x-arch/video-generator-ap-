import os
import json
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def load_platforms_content():
    if os.path.exists("platforms_content.json"):
        with open("platforms_content.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "youtube_niche": "تطوير التطبيقات",
        "instagram_niche": "تصاميم وتطبيقات",
        "tiktok_niche": "فيديوهات قصيرة برمجية"
    }

def analyze_per_platform(data):
    prompt = f"""
    أنت مدير محتوى ذكي ومنصة إدارة قنوات متعددة. إليك محتوى كل منصة على حدة كما حدده المطور من تطبيقه الخاص:
    
    1. يوتيوب: {data.get('youtube_niche')}
    2. إنستغرام: {data.get('instagram_niche')}
    3. تيك توك: {data.get('tiktok_niche')}
    
    قم بتحليل كل منصة بشكل منفصل، واعطني فكرة فيديو دقيقة ومبتكرة خاصة بكل منصة على حدة بناءً على المحتوى المخصص لها.
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        print("--- التقرير والأفكار المنفصلة لكل منصة ---")
        print(result["candidates"][0]["content"]["parts"][0]["text"])
    else:
        print("خطأ في الاتصال بـ Gemini API")

if __name__ == "__main__":
    print("--- قراءة محتوى المنصات المستقل من التطبيق ---")
    platforms_data = load_platforms_content()
    analyze_per_platform(platforms_data)
