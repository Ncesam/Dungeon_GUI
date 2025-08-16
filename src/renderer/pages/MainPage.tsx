import React, {FC, useEffect, useState} from "react";
import Input from "@/ui/Input";
import ItemCard from "@/ui/ItemCard";
import Button from "@/ui/Button";
import {ButtonType} from "@/ui/Button.props";
import PopupAddItem from "@/ui/PopupAddItem";
import {startMonitoring, stopMonitoring} from "@/http/lots";


const MainPage: FC = () => {
    const [vkToken, setVkToken] = useState<string>("");
    const [urlItem, setUrlItem] = useState<string>("");
    const [maxPrice, setMaxPrice] = useState<number>(10000);
    const [delay, setDelay] = useState<number>(50);
    const [items, setItems] = useState<DungeonItem[]>([]);
    const [selectedItem, setSelectedItem] = useState<DungeonItem>();
    const startBot = async () => {
        const parsedUrl = parseUrl(urlItem);
        await startMonitoring({
            delay: delay,
            name: selectedItem?.name,
            item_id: selectedItem?.id,
            auth_key: parsedUrl?.authKey,
            user_id: parsedUrl?.userId,
            max_price: maxPrice
        })
    }
    const stopBot = async () => {
        const parsedUrl = parseUrl(urlItem);
        await stopMonitoring({
            delay: delay,
            name: selectedItem?.name,
            item_id: selectedItem?.id,
            auth_key: parsedUrl?.authKey,
            user_id: parsedUrl?.userId,
            max_price: maxPrice
        })
    }
    useEffect(() => {
        const fetchItems = async () => {
            const result = await window.electronAPI.readItemsFileJson();
            if (!("success" in result)) {
                setItems(result);
            } else {
                console.log("Ошибка", result.error);
            }
        };
        fetchItems();
    }, []);
    console.log(items.length)
    return (
        <div className={"w-full h-full flex flex-col items-center gap-10 justify-center"}>
            <div className={"w-full flex justify-center items-center"}>
                <div className={"w-1/4 flex flex-col items-center gap-3"}>
                    {items.length > 0 ? (
                        <>
                            <span className="w-2/6 text-base-input whitespace-nowrap">
                                Выбери предмет
                            </span>
                            <div className="w-full h-1/4 grid grid-cols-3 gap-1">
                                {items.map((item) => (
                                    <ItemCard key={item.id} id={item.id} name={item.name}/>
                                ))}
                            </div>
                        </>
                    ) : (
                        <span className="bg-base-label p-3 rounded-full text-base-input whitespace-nowrap">
                            Добавь предметы
                        </span>
                    )}
                </div>
                <div className={"w-1/2 flex flex-col items-center"}>
                    <Input label={"Аунтификационый ключ"} value={vkToken} setValue={setVkToken}/>
                    <Input label={"URL предмета"} value={urlItem} setValue={setUrlItem}/>
                    <Input label={"Максимальная цена"} value={maxPrice} setValue={setMaxPrice}/>
                    <Input label={"Задержка между покупаками"} value={delay} setValue={setDelay}/>
                </div>
            </div>
            <div className={"w-3/4 flex items-center justify-center"}>
                <Button type={ButtonType.submit} onClick={startBot}>Запустить бота</Button>
                <Button type={ButtonType.delete} onClick={stopBot}>Остановить бота</Button>
                <PopupAddItem/>
                <Button type={ButtonType.submit} onClick={() => null}>Запустить рыбалку</Button>
                <Button type={ButtonType.delete} onClick={() => null}>Остановить рыбалку</Button>
            </div>

        </div>
    )
}

function parseUrl(url: string): { userId: string; authKey: string } | null {
    const requiredStart = "https://vip3.activeusers.ru/app.php?";

    if (!url.startsWith(requiredStart)) {
        console.error("Url should start with " + requiredStart);
        return null;
    }

    const cleanedUrl = url.replace(
        "https://vip3.activeusers.ru/app.php?act=item&",
        ""
    );

    const parts = cleanedUrl.split("&");

    const userId = parts[2]?.split("=")[1];
    const authKey = parts[1]?.split("=")[1];

    if (!userId || !authKey) {
        console.error("URL missing required parameters");
        return null;
    }

    return {userId, authKey};
}

export default MainPage;