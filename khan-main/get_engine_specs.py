#!/usr/bin/env python3
"""
Получение ключевых характеристик автомобиля: тип двигателя, коробка передач, мощность
Использование: python3 get_engine_specs.py <ID_МАШИНЫ>
"""
import requests
import json
import sys
from typing import TypedDict, Optional


class CarInfo(TypedDict):
    car_name: str
    price: float
    engine_size: int
    engine_type: str
    mileage: int
    year: int
    month: int
    transmission: str


class CarSpecsRetriever:
    """Класс для получения спецификаций автомобиля"""

    BASE_URL = "https://apipcmusc.che168.com/v1/car/getcarinfo"
    PARAMS_URL = "https://cacheapigo.che168.com/CarProduct/GetParam.ashx"

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }

    @classmethod
    def get_car_info(cls, car_id: int) -> Optional[CarInfo]:
        """Получить информацию об автомобиле по ID

        Args:
            car_id: ID автомобиля на che168.com

        Returns:
            CarInfo объект с характеристиками автомобиля или None при ошибке
        """
        try:
            # Получаем базовую информацию
            base_data = cls._get_base_info(car_id)
            if not base_data:
                return None

            spec_id = base_data.get('specid')
            if not spec_id:
                print(f"Не найден specid для автомобиля {car_id}")
                return None

            # Получаем детальные параметры
            param_data = cls._get_detailed_params(spec_id)
            if not param_data:
                return None

            # Извлекаем и возвращаем структурированные данные
            return cls._extract_car_info(base_data, param_data)

        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            return None

    @classmethod
    def _get_base_info(cls, car_id: int) -> Optional[dict]:
        """Получить базовую информацию об автомобиле"""
        url = f"{cls.BASE_URL}?_appid=2sc.pc&infoid={car_id}"

        try:
            response = requests.get(url, headers=cls.HEADERS, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data.get('returncode') == 0:
                return data.get('result')
            else:
                print(f"API вернул ошибку: {data.get('message')}")
                return None

        except requests.RequestException as e:
            print(f"Ошибка сети: {e}")
            return None

    @classmethod
    def _get_detailed_params(cls, spec_id: int) -> Optional[dict]:
        """Получить детальные параметры автомобиля"""
        url = f"{cls.PARAMS_URL}?specid={spec_id}"

        try:
            response = requests.get(url, headers=cls.HEADERS, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data.get('returncode') == 0:
                return data.get('result')
            else:
                print("Ошибка получения детальных параметров")
                return None

        except requests.RequestException as e:
            print(f"Ошибка сети при получении параметров: {e}")
            return None

    @classmethod
    def _extract_car_info(cls, base_data: dict, param_data: dict) -> CarInfo:
        """Извлечь структурированную информацию об автомобиле"""
        # Извлекаем год из строки типа "2019年"
        year_str = base_data.get('firstregyear', '')
        year = 0
        if year_str and '年' in year_str:
            try:
                year = int(year_str.replace('年', ''))
            except ValueError:
                year = 0

        # Извлекаем месяц из даты
        month = 0
        first_reg_date = base_data.get('firstregdate', '')
        if first_reg_date and '-' in first_reg_date:
            try:
                month = int(first_reg_date.split('-')[1])
            except (ValueError, IndexError):
                month = 1

        # Инициализируем значения по умолчанию
        car_info: CarInfo = {
            'car_name': base_data.get('carname', ''),
            'price': float(base_data.get('price', 0)),
            'engine_size': 0,  # Объем двигателя в см³
            'engine_type': '',
            'mileage': int(base_data.get('mileage', 0) * 10000),  # Конвертируем в км
            'year': year,
            'month': month,
            'transmission': ''
        }

        # Извлекаем данные из параметров
        params = param_data.get('paramtypeitems', [])

        for param_type in params:
            param_name = param_type.get('name')

            # Основные параметры
            if param_name == '基本参数':
                for param in param_type.get('paramitems', []):
                    name = param.get('name')
                    value = param.get('value', '')

                    if name == '发动机':
                        car_info['engine_type'] = value
                    elif name == '变速箱':
                        car_info['transmission'] = value

            # Детали двигателя
            elif param_name == '发动机':
                for param in param_type.get('paramitems', []):
                    name = param.get('name')
                    value = param.get('value', '')

                    if name == '排量(mL)':
                        try:
                            car_info['engine_size'] = int(float(value))
                        except (ValueError, TypeError):
                            car_info['engine_size'] = 0

        return car_info

    @classmethod
    def print_car_info(cls, car_info: CarInfo) -> None:
        """Красиво вывести информацию об автомобиле"""
        print("=" * 70)
        print(f"🚗 {car_info['car_name']}")
        print("=" * 70)
        print(f"💰 Цена: {car_info['price']}万 RMB")
        print(f"🔧 Двигатель: {car_info['engine_type']}")
        print(f"📏 Объем: {car_info['engine_size']} см³")
        print(f"⚙️ Коробка: {car_info['transmission']}")
        print(f"🛣️ Пробег: {car_info['mileage']} км")
        print(f"📅 Год/месяц: {car_info['year']}.{car_info['month']:02d}")
        print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 get_engine_specs.py <ID_МАШИНЫ>")
        print("Пример: python3 get_engine_specs.py 57369943")
        sys.exit(1)

    try:
        car_id = int(sys.argv[1])
    except ValueError:
        print("❌ ID машины должен быть числом")
        sys.exit(1)

    # Получаем информацию через класс
    car_info = CarSpecsRetriever.get_car_info(car_id)

    if car_info:
        # Выводим информацию
        CarSpecsRetriever.print_car_info(car_info)

        # Сохраняем в файл
        filename = f'car_info_{car_id}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(car_info, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Данные сохранены в: {filename}")
    else:
        print("❌ Не удалось получить информацию об автомобиле")
        sys.exit(1)
