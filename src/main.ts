import {app, BrowserWindow, ipcMain} from 'electron';
import * as path from 'path';
import fs from "node:fs";
import {createFileItems, readFileItems, updateFileItems} from "./fileSystem";

const isDev = !app.isPackaged;

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, './preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
            sandbox: true,
        },
    });

    if (isDev) {
        win.loadURL('http://localhost:3000'); // Dev: React server
    } else {
        win.loadFile(path.join(__dirname, '../build/index.html')); // Prod: build
    }
}

ipcMain.handle("create-items-file-json", createFileItems)

ipcMain.handle("update-items-file-json", updateFileItems)

ipcMain.handle("read-items-file-json", readFileItems)

app.whenReady().then(() => {
    createWindow();

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
});

