
export const addItem = async (name: string, id: number) => {
    await window.electronAPI.updateItemsFileJson(name, id)
    console.log("File items updated")
}

const getAllItems = () => {

}

export const createFile = async () => {
    await window.electronAPI.createItemsFileJson()
    console.log("File Items created")
}

