import React from "react";


export interface ButtonForm {
    onClick?: () => void;
    children?: React.ReactNode;
    type?: ButtonType
}

export enum ButtonType {
    submit = "p-5 whitespace-nowrap rounded-xl bg-base-label text-center text-base-input font-bold shadow-lg transition-all duration-300 ease-in-out hover:scale-110 hover:bg-base-input hover:text-base-label",
    add = "bg-base-input hover:bg-gray-900 text-base-label hover:text-base-input font-semibold py-2 px-5 rounded-lg shadow-md transition transform hover:scale-105 hover:shadow-lg duration-300 ease-in-out",
    delete = "bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-full shadow-lg transition duration-300 ease-in-out hover:scale-105"
}