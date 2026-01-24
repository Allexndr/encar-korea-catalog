#!/usr/bin/env python3
"""
Простой скрипт для получения информации о машине с che168.com
Использование: python3 get_car_info.py 56635701
"""
import requests
import json
import sys

def get_car_info(car_id):
    """Получить информацию о машине по ID"""
    url = f"https://apipcmusc.che168.com/v1/car/getcarinfo?_appid=2sc.pc&infoid={car_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('returncode') == 0:
            car = data.get('result', {})
            print("=" * 60)
            print("ИНФОРМАЦИЯ О МАШИНЕ")
            print("=" * 60)
            print(f"ID: {car.get('infoid')}")
            print(f"Название: {car.get('carname')}")
            print(f"Марка: {car.get('brandname')}")
            print(f"Модель: {car.get('seriesname')}")
            print(f"Цена: {car.get('price')} 万")
            print(f"Пробег: {car.get('mileage')} 万公里")
            print(f"Год: {car.get('firstregyear')}")
            print(f"Город: {car.get('cname')}")
            print(f"Дилер: {car.get('dealername')}")
            print(f"ID дилера: {car.get('dealerid')}")
            print("=" * 60)
            
            # Сохранить полный JSON в файл
            filename = f"car_{car_id}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\nПолные данные сохранены в: {filename}")
            
            return data
        else:
            print(f"Ошибка: {data.get('message', 'Неизвестная ошибка')}")
            return None
            
    except Exception as e:
        print(f"Ошибка при запросе: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 get_car_info.py <ID_МАШИНЫ>")
        print("Пример: python3 get_car_info.py 56635701")
        sys.exit(1)
    
    car_id = sys.argv[1]
    get_car_info(car_id)


