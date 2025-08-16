import {contextBridge, ipcRenderer} from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
    createItemsFileJson: () => ipcRenderer.invoke("create-items-file-json"),
    updateItemsFileJson: (itemName: string, idItem: number) => ipcRenderer.invoke("update-items-file-json", itemName, idItem),
    readItemsFileJson: () => ipcRenderer.invoke("read-items-file-json"),
})
