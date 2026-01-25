const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = 3001;

// Serve static files
app.use(express.static(__dirname));

// Root route handler for landing page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'catalog.html'));
});

// Headers that mimic a real iPhone Safari
const MOBILE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Referer': 'https://fem.encar.com/',
    'Origin': 'https://fem.encar.com',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
};

// API proxy endpoint
app.get('/api/car/:id', async (req, res) => {
    const carId = req.params.id;
    const apiUrl = `https://api.encar.com/v1/readside/vehicle/${carId}`;

    const params = {
        include: 'ADVERTISEMENT,CATEGORY,CONDITION,CONTACT,MANAGE,OPTIONS,PHOTOS,SPEC,PARTNERSHIP,CENTER,VIEW'
    };

    console.log(`🔍 Fetching car ${carId}...`);

    try {
        const response = await axios.get(apiUrl, {
            params,
            headers: MOBILE_HEADERS,
            timeout: 5000
        });
        console.log(`✅ Success ${carId}`);
        res.json(response.data);
    } catch (error) {
        if (error.response) {
            console.error(`❌ Error ${carId}: Status ${error.response.status}`);
            console.error(error.response.data);
            res.status(error.response.status).json(error.response.data);
        } else {
            console.error(`❌ Error ${carId}: ${error.message}`);
            res.status(500).json({ error: 'Failed to fetch car data' });
        }
    }
});

// Image Proxy to bypass hotlink protection
app.get('/api/image', async (req, res) => {
    const imageUrl = req.query.url;
    if (!imageUrl) return res.status(400).send('URL required');

    // Ensure we are only proxying encar images
    if (!imageUrl.includes('encar.com')) {
        return res.status(400).send('Only Encar images allowed');
    }

    try {
        const response = await axios({
            url: imageUrl,
            method: 'GET',
            responseType: 'stream',
            headers: {
                ...MOBILE_HEADERS,
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
            }
        });

        // Forward content type
        res.set('Content-Type', response.headers['content-type']);
        response.data.pipe(res);
    } catch (error) {
        console.error(`❌ Image fetch failed: ${imageUrl}`);
        res.status(404).send('Image not found');
    }
});

if (process.env.NODE_ENV !== 'production' || require.main === module) {
    app.listen(PORT, () => {
        console.log(`🚗 Encar Demo Server running at http://localhost:${PORT}`);
        console.log(`📱 Open your browser to see the demo!`);
    });
}

module.exports = app;
