const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const PYTHON_BACKEND_URL = 'http://localhost:8000';

app.post('/api/generate', async (req, res) => {
    try {
        const response = await axios.post(`${PYTHON_BACKEND_URL}/generate`, req.body);
        res.json(response.data);
    } catch (error) {
        const status = error.response ? error.response.status : 500;
        const message = error.response ? error.response.data.detail : error.message;
        res.status(status).json({ error: message });
    }
});

app.get('/api/history', async (req, res) => {
    try {
        const response = await axios.get(`${PYTHON_BACKEND_URL}/history`);
        res.json(response.data);
    } catch (error) {
        const status = error.response ? error.response.status : 500;
        const message = error.response ? error.response.data.detail : error.message;
        res.status(status).json({ error: message });
    }
});

const PORT = 3001;
app.listen(PORT, () => {
    console.log(`Gateway running on http://localhost:${PORT}`);
});