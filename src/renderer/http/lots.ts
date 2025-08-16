import $api from "./api";

export const startMonitoring = async (schema: SchemeStartBot) => {
    await $api.post("/start", {...schema})
}

export const stopMonitoring = async (schema: SchemeStartBot) => {
    await $api.post("/stop", {...schema})
}

