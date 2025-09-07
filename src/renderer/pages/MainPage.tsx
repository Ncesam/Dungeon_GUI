import React, {FC, useEffect, useState} from "react";
import Input from "@/ui/Input";
import Button from "@/ui/Button";
import {ButtonType} from "@/ui/Button.props";
import PopupAddItem from "@/ui/PopupAddItem";
import ItemsList from "@/components/ItemsList";
import {fetchItems} from "@/services/itemsService";
import {notify} from "@/utils/notify";
import {startBot, stopBot} from "@/services/botService";


const MainPage: FC = () => {
    const [vkToken, setVkToken] = useState<string>("");
    const [urlItem, setUrlItem] = useState<string>("");
    const [maxPrice, setMaxPrice] = useState<number>(10000);
    const [delay, setDelay] = useState<number>(50);

    const [items, setItems] = useState<DungeonItem[]>([]);
    const [selectedItem, setSelectedItem] = useState<DungeonItem | null>(null);

    const validateForm = () => {
        if (!selectedItem) {
            notify.error("Выберите предмет");
            return false;
        }

        if (urlItem.trim() === "") {
            notify.error("Введите URL");
            return false;
        }

        if (vkToken.trim() === "") {
            notify.error("Введите VK Token");
            return false;
        }

        return true;
    };
    const callBotAction = async (action: "start" | "stop") => {
        if (!validateForm()) return;

        try {
            const service = action === "start" ? startBot : stopBot;
            const result = await service(urlItem, {
                delay,
                name: selectedItem!.name,
                itemId: selectedItem!.id,
                vkToken,
                maxPrice
            });

            if (result.ok) {
                notify.success(`Бот успешно ${action === "start" ? "запущен 🚀" : "остановлен ⏹️"}`);
            } else {
                notify.error(result.error || `Не удалось ${action === "start" ? "запустить" : "остановить"} бота`);
            }
        } catch (err) {
            notify.error(`Ошибка при ${action === "start" ? "запуске" : "остановке"} бота`);
            console.error(err);
        }
    };

    useEffect(() => {
        (async () => {
            const result = await fetchItems()
            if (result.data) {
                setItems(result.data);
            } else {
                console.log("Ошибка", result.error);
            }
        })()
    }, []);
    return (
        <div className={"w-full h-full flex flex-col items-center gap-10 justify-center"}>
            <div className={"w-full flex justify-center items-center"}>
                <ItemsList items={items} selectedItem={selectedItem} onSelect={setSelectedItem}/>
                <div className={"w-1/2 h-full flex flex-col items-center"}>
                    <Input label={"Аунтификационый ключ"} value={vkToken} setValue={setVkToken}/>
                    <Input label={"URL предмета"} value={urlItem} setValue={setUrlItem}/>
                    <Input label={"Максимальная цена"} value={maxPrice} setValue={setMaxPrice}/>
                    <Input label={"Задержка между покупаками"} value={delay} setValue={setDelay}/>
                </div>
            </div>
            <div className={"w-3/4 flex items-center justify-center"}>
                <Button type={ButtonType.submit} onClick={() => callBotAction("start")}>Запустить бота</Button>
                <Button type={ButtonType.delete} onClick={() => callBotAction("stop")}>Остановить бота</Button>
                <PopupAddItem/>
                <Button type={ButtonType.submit} onClick={() => null}>Запустить рыбалку</Button>
                <Button type={ButtonType.delete} onClick={() => null}>Остановить рыбалку</Button>
            </div>

        </div>
    )
}


export default MainPage;


