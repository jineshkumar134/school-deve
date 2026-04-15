/**
 * MongoDB Client Wrapper for School Development Portal
 */

const API_URL = '/api/data';
let dataCache = {};
let dbReady = false;
const readyCallbacks = [];

// Initialize data from MongoDB
async function initDB() {
  console.log('Initializing MongoDB connection...');
  try {
    const response = await fetch(API_URL);
    if (response.ok) {
      const remoteData = await response.json();
      dataCache = remoteData;
      
      // Migration: if localStorage has data not in MongoDB, we could sync it
      // For now, let's just merge them, with MongoDB taking priority
      Object.keys(localStorage).forEach(key => {
        if (dataCache[key] === undefined) {
          try {
            const localVal = JSON.parse(localStorage.getItem(key));
            dataCache[key] = localVal;
            // Optionally push this to MongoDB now
            saveToRemote(key, localVal);
          } catch(e) {}
        }
      });

      dbReady = true;
      console.log('MongoDB data loaded.');
      readyCallbacks.forEach(cb => cb());
    } else {
      throw new Error('Server responded with ' + response.status);
    }
  } catch (err) {
    console.warn('Backend server not reached. Using localStorage fallback.', err);
    // Fallback to localStorage
    Object.keys(localStorage).forEach(key => {
      try {
        dataCache[key] = JSON.parse(localStorage.getItem(key));
      } catch(e) {}
    });
    dbReady = true;
    readyCallbacks.forEach(cb => cb());
  }
}

async function saveToRemote(key, value) {
  try {
    await fetch(`${API_URL}/${key}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(value)
    });
  } catch (err) {
    console.error('Save to MongoDB failed:', err);
  }
}

// Global DB Object
window.DB = {
  get: (key, fallback) => {
    if (dataCache[key] !== undefined) return dataCache[key];
    return fallback;
  },
  set: (key, value) => {
    dataCache[key] = value;
    // Update localStorage as a local cache/buffer
    localStorage.setItem(key, JSON.stringify(value));
    // Persist to MongoDB
    saveToRemote(key, value);
  },
  onReady: (cb) => {
    if (dbReady) cb();
    else readyCallbacks.push(cb);
  }
};

// Start initialization
initDB();
