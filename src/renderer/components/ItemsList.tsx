import React, {FC} from "react";
import ItemCard from "@/ui/ItemCard";
import {ItemsListProps} from "@/components/ItemsList.props";


const ItemsList: FC<ItemsListProps> = ({items, selectedItem, onSelect}) => {
    return (
        <div className="w-1/4 flex flex-col items-center gap-3">
            {items.length > 0 ? (
                <>
          <span className="w-2/6 text-base-input whitespace-nowrap">
            Выбери предмет
          </span>
                    <div className="relative w-full h-1/4 grid grid-cols-3 gap-1">
                        {items.map((item) => (
                            <div
                                key={item.id}
                                className={`w-full h-full cursor-pointer ${
                                    selectedItem?.id === item.id ? "border-3 border-yellow-500" : ""
                                }`}
                                onClick={() => onSelect(item)}
                            >
                                <ItemCard id={item.id} name={item.name}/>
                            </div>
                        ))}
                    </div>
                </>
            ) : (
                <span
                    className="bg-base-label p-6 lg:p-3 text-3xl lg:text-lg rounded-full text-center text-base-input whitespace-nowrap">
          Добавь предметы
        </span>
            )}
        </div>
    );
};

export default ItemsList;