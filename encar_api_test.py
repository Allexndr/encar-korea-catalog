import requests
import json
import uuid
import sys

def get_car_data(url):
    print(f"Analyzing URL: {url}")
    
    # 1. Extract Car ID based on user's logic
    try:
        if "/cars/detail/" in url:
            car_id = url.split("/cars/detail/")[1].split("?")[0]
        else:
            print("❌ Invalid URL format. Expected .../cars/detail/...")
            return
    except Exception as e:
        print(f"❌ Error parsing URL: {e}")
        return

    print(f"✅ Extracted Car ID: {car_id}")
    
    # 2. Define Internal API Endpoint (Found via inspection)
    # The mobile site fetches from: https://api.encar.com/v1/readside/vehicle/{ID}
    api_url = f"https://api.encar.com/v1/readside/vehicle/{car_id}" 
    
    # Parameters observed in network traffic
    params = {
        "include": "ADVERTISEMENT,CATEGORY,CONDITION,CONTACT,MANAGE,OPTIONS,PHOTOS,SPEC,PARTNERSHIP,CENTER,VIEW"
    }
    
    # Headers to mimic a browser (Anti-bot minimal protection)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://fem.encar.com/",
        "Origin": "https://fem.encar.com",
        "Accept": "application/json, text/plain, */*"
    }

    print(f"🔄 Requesting Internal API: {api_url}...")
    
    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n" + "="*50)
            print("🚀 API SUCCESS! DATA EXTRACTED:")
            print("="*50)
            
            # --- Parsing Data ---
            cat = data.get("category", {})
            spec = data.get("spec", {})
            ad = data.get("advertisement", {})
            photos = data.get("photos", [])
            
            # Basic Info
            print(f"🚗 Name (KR):  {cat.get('manufacturerName')} {cat.get('modelGroupName')} {cat.get('gradeName')}")
            print(f"🚗 Name (EN):  {cat.get('manufacturerEnglishName', '-')} {cat.get('modelGroupEnglishName', '-')} {cat.get('gradeEnglishName', '-')}")
            print(f"📅 Year:       {spec.get('yearName')}")
            print(f"⛽ Fuel:       {spec.get('fuelName')}")
            print(f"🎨 Color:      {spec.get('colorName')}")
            print(f"🛣️  Mileage:    {spec.get('mileage')} km")
            
            # Price
            price = ad.get("price")
            print(f"💰 Price:      {price} (KRW * 10,000) -> {price * 10000:,} KRW")
            
            # Location
            print(f"📍 Location:   {ad.get('officeCityStateAttribute', {}).get('name')}")
            
            # Images
            print(f"📸 Photos:     {len(photos)} found")
            if photos:
                # Debugging photo structure if needed
                # print(photos[0]) 
                # usually it's 'location' but let's check
                photo_url = photos[0].get('location') or photos[0].get('path') or photos[0].get('url')
                print(f"   First Photo: {photo_url}")
            
            # Raw Data Dump (Small part)
            print("\n--- Raw JSON Dump (First 5 keys) ---")
            print(list(data.keys())[:5])

            
        else:
            print(f"❌ API Request Failed: {response.status_code}")
            print(response.text[:200])
            
    except Exception as e:
        print(f"❌ Exception during request: {e}")

if __name__ == "__main__":
    # Test URL from user
    target_url = "https://fem.encar.com/cars/detail/40570144?advClickPosition=mweb_mhightlight_g1_t18&listAdvType=mhighlight&type=detail&view_type=checked&_gl=1*1kicvzq*_gcl_au*MTQ5NTc3MjA4MC4xNzY0Mzk2ODY1*_ga*MTI4OTg1OTk2OS4xNzMyODk0MTcx*_ga_BQ7RK9J6BZ*czE3NjgyODU0NTAkbzg2NyRnMSR0MTc2ODI5MTEyMyRqNjAkbDAkaDE5NDkwNTQxNjY"
    
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        
    get_car_data(target_url)
