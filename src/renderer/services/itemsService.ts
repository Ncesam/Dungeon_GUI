export const fetchItems = async (): Promise<{ ok: boolean, error?: any, data?: DungeonItem[] }> => {
    const response = await window.electronAPI.readItemsFileJson();
    if ("success" in response) {
        return {ok: false, error: response.error};
    } else {
        return {ok: true, data: response};
    }
}

export const addNewItem = async (item: { name: string, id: number }) => {
    return await window.electronAPI.updateItemsFileJson(item.name, item.id);
}

export const deleteItem = async (id: number) => {

}