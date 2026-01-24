# Найден API эндпоинт для получения информации о машине с che168.com

## URL запроса

```
https://apipcmusc.che168.com/v1/car/getcarinfo?_appid=2sc.pc&infoid={car_id}
```

## Параметры

- `_appid` - идентификатор приложения (для PC версии: `2sc.pc`)
- `infoid` - ID машины (например: `56635701`)

## Пример запроса

Для машины с ID `56635701`:
```
https://apipcmusc.che168.com/v1/car/getcarinfo?_appid=2sc.pc&infoid=56635701
```

## Формат ответа

API возвращает JSON с информацией о машине:

```json
{
  "returncode": 0,
  "message": "成功",
  "result": {
    "infoid": 56635701,
    "carname": "探岳 2022款 380TSI 四驱R-Line智联版",
    "brandid": 1,
    "brandname": "大众",
    "seriesid": 4744,
    "seriesname": "探岳",
    "specid": 54817,
    "cid": 230100,
    "cname": "哈尔滨",
    "pid": 230000,
    "displacement": "2",
    "mileage": 4.5,
    "price": 16.5,
    "dealerid": 466343,
    "dealername": "黑龙江卡弗特汽车科技服务有限公司",
    ...
  }
}
```

## Заголовки запроса

Рекомендуемые заголовки:
```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: application/json, text/javascript, */*; q=0.01
Referer: https://www.che168.com/dealer/{dealer_id}/{car_id}.html
```

## Дополнительные найденные эндпоинты

1. **VR фотографии:**
   ```
   https://apipcmusc.che168.com/v1/car/getcarvrpics?_appid=2sc.m&infoid={car_id}
   ```

2. **Обработчик деталей (возвращает HTML):**
   ```
   https://www.che168.com/handler/dealer/cardetail.ashx?infoid={car_id}&dealerid={dealer_id}
   ```

## Примечания

- API работает без аутентификации для публичных данных
- Для мобильной версии используйте `_appid=2sc.m` вместо `2sc.pc`
- ID машины (`infoid`) можно найти в URL страницы: `/dealer/{dealer_id}/{car_id}.html`


