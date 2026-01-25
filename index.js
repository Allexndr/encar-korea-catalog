const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

// Разрешаем отдавать статические файлы (картинки, стили)
app.use(express.static(__dirname));

// Главная страница
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'catalog.html'));
});

// Страница автомобиля (детальная)
app.get('/car.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'car.html'));
});

// Короткий путь для удобства
app.get('/car', (req, res) => {
    res.sendFile(path.join(__dirname, 'car.html'));
});

// Заголовки для маскировки под iPhone
const MOBILE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Referer': 'https://fem.encar.com/',
    'Origin': 'https://fem.encar.com',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
};

// Прокси для данных авто
app.get('/api/car/:id', async (req, res) => {
    const carId = req.params.id;
    const apiUrl = `https://api.encar.com/v1/readside/vehicle/${carId}`;
    try {
        const response = await axios.get(apiUrl, {
            params: { include: 'ADVERTISEMENT,CATEGORY,CONDITION,CONTACT,MANAGE,OPTIONS,PHOTOS,SPEC,PARTNERSHIP,CENTER,VIEW' },
            headers: MOBILE_HEADERS,
            timeout: 5000
        });
        res.json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json({ error: 'Encar API error' });
    }
});

// Прокси для изображений
app.get('/api/image', async (req, res) => {
    const imageUrl = req.query.url;
    if (!imageUrl || !imageUrl.includes('encar.com')) return res.status(400).send('Invalid image URL');
    try {
        const response = await axios({
            url: imageUrl,
            method: 'GET',
            responseType: 'stream',
            headers: { ...MOBILE_HEADERS, 'Accept': 'image/webp,image/*;q=0.8' }
        });
        res.set('Content-Type', response.headers['content-type']);
        response.data.pipe(res);
    } catch (error) {
        res.status(404).send('Not found');
    }
});

if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`🚗 Server running at http://localhost:${PORT}`);
    });
}

module.exports = app;
