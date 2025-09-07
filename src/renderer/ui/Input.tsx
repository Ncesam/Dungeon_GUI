import {FC} from "react";
import {InputForm} from "@/ui/Input.props";


const Input: FC<InputForm> = ({
                                  type = "type",
                                  placeholder = "Example",
                                  label = "Example",
                                  setValue,
                                  value = "Example"
                              }) => {
    return (
            <span className={"inline-block relative group w-3/4 m-8"}>
                <input type={type} className={"slide-up-input absolute top-0 left-0 w-full z-0"} placeholder={placeholder}
                       value={value}
                       onChange={(event) => setValue(event.target.value)}/>
                <label
                    className={"slide-up-label absolute top-0 left-0 z-10 w-full flex items-center justify-center cursor-pointer"}>{label}</label>
            </span>
    )
}

export default Input;