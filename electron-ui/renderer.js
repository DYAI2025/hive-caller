const { contextBridge } = require('electron');
const axios = require('axios');

window.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('trigger');
  const statusEl = document.getElementById('status');

  btn.addEventListener('click', () => {
    axios.post('http://localhost:8723/trigger').catch(() => {});
  });

  setInterval(() => {
    axios.get('http://localhost:8723/status').then(r => {
      statusEl.innerText = r.data.state;
    });
  }, 1000);
});
