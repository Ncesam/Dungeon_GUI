import React, {FC, useState} from "react";
import Button from "@/ui/Button";
import {PopupAddItemForm} from "@/ui/PopupAddItem.props";
import {ButtonType} from "@/ui/Button.props";
import Input from "@//ui/Input";
import {addItem} from "@/logics/items";


const PopupAddItem: FC<PopupAddItemForm> = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [nameItem, setNameItem] = useState<string>("");
    const [idItem, setIdItem] = useState<number>(0);
    const onClick = async () => {
        await addItem(nameItem, Number(idItem))
        setIsOpen(false);
    }
    return (
        <div className="w-full">
            <Button
                onClick={() => setIsOpen(true)}
                type={ButtonType.add}
            >
                Добавить Предмет
            </Button>

            {isOpen && (
                <div
                    className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 animate-fade-in">
                    <div className="bg-white rounded-xl p-6 shadow-xl w-[90%] max-w-md relative animate-slide-up">
                        <button
                            onClick={() => setIsOpen(false)}
                            className="absolute top-2 right-2 text-gray-400 hover:text-red-500 text-2xl"
                        >
                            &times;
                        </button>
                        <h2 className="text-xl font-bold mb-4 text-gray-800">Добавить предмет</h2>


                        <div className="flex flex-col gap-10">
                            <div className={"flex flex-col gap-3"}>
                                <Input
                                    type="text"
                                    placeholder="Книга Драконов"
                                    label="Название предмета"
                                    value={nameItem}
                                    setValue={setNameItem}
                                />
                                <Input
                                    type="text"
                                    placeholder="1"
                                    label="ID предмета"
                                    value={idItem}
                                    setValue={setIdItem}
                                />
                            </div>
                            <Button
                                onClick={onClick}
                                type={ButtonType.submit}
                            >
                                Сохранить
                            </Button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PopupAddItem;