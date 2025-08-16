import {FC} from "react";
import {ButtonForm} from "@/ui/Button.props";
import clsx from "clsx";


const Button: FC<ButtonForm> = ({children, onClick, type}) => {
    return (
        <div className={"w-full"}>
            <button className={type} onClick={onClick}>{children}</button>
        </div>
    )
}

export default Button;