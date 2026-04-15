const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.static(__dirname)); // Serve HTML files from this directory

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('Could not connect to MongoDB', err));

// Schema
const dataSchema = new mongoose.Schema({
  key: { type: String, required: true, unique: true },
  value: { type: mongoose.Schema.Types.Mixed, required: true },
  updatedAt: { type: Date, default: Date.now }
});

const Data = mongoose.model('Data', dataSchema);

// API Routes

// Get all data (for pre-fetching)
app.get('/api/data', async (req, res) => {
  try {
    const allData = await Data.find({});
    // Transform to a single object: { key1: value1, key2: value2 }
    const result = {};
    allData.forEach(item => {
      result[item.key] = item.value;
    });
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Get specific key
app.get('/api/data/:key', async (req, res) => {
  try {
    const item = await Data.findOne({ key: req.params.key });
    res.json(item ? item.value : null);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Save specific key
app.post('/api/data/:key', async (req, res) => {
  try {
    const { key } = req.params;
    const value = req.body;
    
    const updated = await Data.findOneAndUpdate(
      { key },
      { value, updatedAt: Date.now() },
      { upsert: true, new: true }
    );
    
    res.json({ success: true, data: updated });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Bulk save (optional)
app.post('/api/data/bulk', async (req, res) => {
  try {
    const items = req.body; // Expecting { key1: val1, key2: val2 }
    const operations = Object.entries(items).map(([key, value]) => ({
      updateOne: {
        filter: { key },
        update: { value, updatedAt: Date.now() },
        upsert: true
      }
    }));
    await Data.bulkWrite(operations);
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
