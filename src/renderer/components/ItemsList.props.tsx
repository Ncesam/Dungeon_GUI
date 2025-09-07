export interface ItemsListProps {
    items: DungeonItem[];
    selectedItem: DungeonItem | null;
    onSelect: (item: DungeonItem) => void;
}
