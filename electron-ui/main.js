const { app, BrowserWindow, globalShortcut } = require('electron');
const path = require('path');
const axios = require('axios');

function createWindow () {
  const win = new BrowserWindow({
    width: 300,
    height: 150,
    webPreferences: {
      preload: path.join(__dirname, 'renderer.js')
    }
  })
  win.loadFile('index.html')
}

app.whenReady().then(() => {
  createWindow();

  const config = require('../config.json');
  const hotkey = config.hotkey || 'CommandOrControl+Shift+H';
  globalShortcut.register(hotkey, () => {
    axios.post('http://localhost:8723/trigger').catch(() => {});
  });

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  })
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});
