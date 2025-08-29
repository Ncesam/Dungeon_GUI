import path from "path";
import fs from "node:fs";
import * as electron from "electron";


export async function createFileItems(event: electron.IpcMainInvokeEvent) {
    const appDataPath = electron.app.getPath('userData');

    fs.mkdirSync(appDataPath, {recursive: true});

    const filePath = path.join(appDataPath, 'items.json')

    try {
        await fs.promises.writeFile(filePath, JSON.stringify({items: []}));

        return {success: true, path: filePath};
    } catch (err: any) {
        console.error('Error creating file', err);
        return {success: false, error: err.message};
    }
}

export async function updateFileItems(event: electron.IpcMainInvokeEvent, nameItem: string, idItem: number) {
    const appDataPath = electron.app.getPath('userData');

    fs.mkdirSync(appDataPath, {recursive: true});

    const filePath = path.join(appDataPath, 'items.json');
    try {
        fs.readFileSync(filePath, "utf8");
    } catch (err) {
        await createFileItems(event)
    }
    try {
        const data = fs.readFileSync(filePath, "utf8");
        let jsonData = JSON.parse(data);

        if (!Array.isArray(jsonData.items)) {
            jsonData.items = [];
        }

        jsonData.items.push({id: Number(idItem), name: nameItem});

        fs.writeFileSync(filePath, JSON.stringify(jsonData, null, 2), "utf8");

        return {success: true, path: filePath};

    } catch (err: any) {
        console.error('Error updating file', err);
        return {success: false, error: err.message};
    }
}

export async function readFileItems(event: electron.IpcMainInvokeEvent) {
    const appDataPath = electron.app.getPath('userData');

    fs.mkdirSync(appDataPath, {recursive: true});

    const filePath = path.join(appDataPath, 'items.json')
    try {
        const data = fs.readFileSync(filePath, "utf8");
        return JSON.parse(data).items as DungeonItem[];
    } catch (err: any) {
        await createFileItems(event);
        return {success: false, error: err.message};
    }
}