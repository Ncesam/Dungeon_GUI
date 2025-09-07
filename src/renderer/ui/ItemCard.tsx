import {FC} from "react";
import {ItemCardForm} from "@/ui/ItemCard.props";
import Button from "@/ui/Button";
import {ButtonType} from "@/ui/Button.props";


const ItemCard: FC<ItemCardForm> = ({name, id}) => {
    const idItem = id
    return (
        <Button onClick={() => null} type={ButtonType.submit}>{name}</Button>
    )
}

export default ItemCard;