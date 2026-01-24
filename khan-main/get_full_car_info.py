#!/usr/bin/env python3
"""
Получение полной информации о машине: базовые данные + конфигурация
"""
import requests
import json
import sys

def get_full_car_info(car_id):
    """Получить полную информацию о машине"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
    
    print("=" * 80)
    print("ПОЛУЧЕНИЕ ПОЛНОЙ ИНФОРМАЦИИ О МАШИНЕ")
    print("=" * 80)
    
    # 1. Получаем базовую информацию
    print("\n1. Получаю базовую информацию...")
    base_url = f"https://apipcmusc.che168.com/v1/car/getcarinfo?_appid=2sc.pc&infoid={car_id}"
    
    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        base_data = response.json()
        
        if base_data.get('returncode') != 0:
            print(f"Ошибка: {base_data.get('message')}")
            return None
        
        car = base_data.get('result', {})
        spec_id = car.get('specid')
        
        print(f"✓ ID машины: {car.get('infoid')}")
        print(f"✓ Название: {car.get('carname')}")
        print(f"✓ Марка: {car.get('brandname')}")
        print(f"✓ Цена: {car.get('price')} 万")
        print(f"✓ Пробег: {car.get('mileage')} 万公里")
        print(f"✓ ID спецификации: {spec_id}")
        
        if not spec_id:
            print("\n⚠️ Не найден specid, детальная конфигурация недоступна")
            return base_data
        
        # 2. Получаем параметры
        print(f"\n2. Получаю детальные параметры (specid={spec_id})...")
        param_url = f"https://cacheapigo.che168.com/CarProduct/GetParam.ashx?specid={spec_id}"
        
        param_response = requests.get(param_url, headers=headers, timeout=10)
        param_data = param_response.json()
        
        if param_data.get('returncode') == 0:
            params = param_data.get('result', {}).get('paramtypeitems', [])
            print("✓ Получены параметры:")
            for param_type in params[:3]:  # Показываем первые 3
                for param in param_type.get('paramitems', [])[:5]:
                    print(f"  - {param.get('name')}: {param.get('value')}")
        
        # 3. Получаем полную конфигурацию
        print(f"\n3. Получаю полную конфигурацию...")
        config_url = f"https://cacheapi.che168.com/CarProduct/GetSpecListConfig.ashx?specid={spec_id}"
        
        config_response = requests.get(config_url, headers=headers, timeout=10)
        config_data = config_response.json()
        
        if config_data.get('returncode') == 0:
            configs = config_data.get('result', {}).get('configtypeitems', [])
            print(f"✓ Получено категорий конфигурации: {len(configs)}")
            for cfg in configs[:5]:
                print(f"  - {cfg.get('name')} ({len(cfg.get('configitems', []))} опций)")
        
        # Сохраняем всё
        full_data = {
            'base_info': base_data,
            'parameters': param_data,
            'full_config': config_data
        }
        
        filename = f'full_car_info_{car_id}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Все данные сохранены в: {filename}")
        print("=" * 80)
        
        return full_data
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 get_full_car_info.py <ID_МАШИНЫ>")
        print("Пример: python3 get_full_car_info.py 56635701")
        sys.exit(1)
    
    car_id = sys.argv[1]
    get_full_car_info(car_id)


