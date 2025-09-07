import React from 'react';
import MainPage from "@/pages/MainPage";
import {Toaster} from "react-hot-toast";

export default function App() {
    return (
        <div className={"w-screen h-screen flex items-center justify-center"}>
            <MainPage/>
            <Toaster/>
        </div>
    );
}

