const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = 3001;

// Serve static files
app.use(express.static(__dirname));

// API proxy endpoint
app.get('/api/car/:id', async (req, res) => {
    const carId = req.params.id;
    const apiUrl = `https://api.encar.com/v1/readside/vehicle/${carId}`;
    
    const params = {
        include: 'ADVERTISEMENT,CATEGORY,CONDITION,CONTACT,MANAGE,OPTIONS,PHOTOS,SPEC,PARTNERSHIP,CENTER,VIEW'
    };
    
    const headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://fem.encar.com/',
        'Origin': 'https://fem.encar.com',
        'Accept': 'application/json'
    };

    try {
        const response = await axios.get(apiUrl, { params, headers, timeout: 10000 });
        res.json(response.data);
    } catch (error) {
        console.error(`Error fetching car ${carId}:`, error.message);
        res.status(500).json({ error: 'Failed to fetch car data' });
    }
});

app.listen(PORT, () => {
    console.log(`🚗 Encar Demo Server running at http://localhost:${PORT}`);
    console.log(`📱 Open your browser to see the demo!`);
});
