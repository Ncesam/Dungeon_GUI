import {startMonitoring, stopMonitoring} from "@/http/lots";
import {parseUrl} from "@/utils/parseUrl";
import {notify} from "@/utils/notify";

export const stopBot = async (url: string, schema: BotPayload): Promise<{ ok: boolean, error?: any }> => {
    try {
        let parsedUrl;
        try {
            parsedUrl = parseUrl(url);
            if (!parsedUrl?.authKey || !parsedUrl?.userId) {
                throw new Error("Некорректный URL");
            }
        } catch (err) {
            notify.error("Введите правильный URL");
            return {ok: false, error: "Incorrect URL"};
        }
        await stopMonitoring(
            {
                delay: schema.delay,
                name: schema.name,
                item_id: schema.itemId,
                auth_key: parsedUrl?.authKey,
                user_id: parsedUrl?.userId,
                max_price: schema.maxPrice,
                vk_token: schema.vkToken
            }
        );
        return {ok: true};
    } catch (err) {
        console.error("Ошибка запуска бота:", err);
        return {ok: false, error: err};
    }
};

interface BotPayload {
    delay: number;
    name: string;
    itemId: number;
    maxPrice: number;
    vkToken: string;
}

export const startBot = async (url: string, schema: BotPayload): Promise<{ ok: boolean, error?: any }> => {
    try {
        let parsedUrl;
        try {
            parsedUrl = parseUrl(url);
            if (!parsedUrl?.authKey || !parsedUrl?.userId) {
                throw new Error("Некорректный URL");
            }
        } catch (err) {
            notify.error("Введите правильный URL");
            return {ok: false, error: "Incorrect URL"};
        }
        await startMonitoring(
            {
                delay: schema.delay,
                name: schema.name,
                item_id: schema.itemId,
                auth_key: parsedUrl?.authKey,
                user_id: parsedUrl?.userId,
                max_price: schema.maxPrice,
                vk_token: schema.vkToken
            }
        );
        return {ok: true};
    } catch (err) {
        console.error("Ошибка запуска бота:", err);
        return {ok: false, error: err};
    }
};
