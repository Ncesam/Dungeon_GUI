declare module '*.png';
declare module '*.jpg';
declare module '*.jpeg';
declare module "*.svg" {
    import React from "react";
    const SVG: React.VFC<React.SVGProps<SVGSVGElement>>;
    export default SVG;
}

declare const __PLATFORM__: 'mobile' | 'desktop';
declare const __ENV__: 'production' | 'development';

export {}

interface IElectronAPI {
    createItemsFileJson: () => Promise<{ success: boolean; path?: string; error?: string }>;
    updateItemsFileJson: (itemName: string, idItem: number) => Promise<{ success: boolean; error?: string }>
    readItemsFileJson: () => Promise<{ success: boolean; error?: string } | DungeonItem[]>;
}

declare global {
    interface Window {
        electronAPI: IElectronAPI
    }

    interface DungeonItem {
        id: number
        name: string
    }

    interface SchemeStartBot {
        item_id: int
        max_price: int
        user_id: int
        auth_key: str
        delay: int
        name: str
    }
}
