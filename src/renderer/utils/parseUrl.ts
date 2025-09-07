export const parseUrl = (url: string): { userId: number; authKey: string } | null => {
    const requiredStart = "https://vip3.activeusers.ru/app.php?";
    if (!url.startsWith(requiredStart)) {
        console.error("Url should start with " + requiredStart);
        return null;
    }
    const cleanedUrl = url.replace(
        requiredStart + "act=item&",
        ""
    );
    const parts = cleanedUrl.split("&");
    const userId = Number(parts[2]?.split("=")[1]);
    const authKey = parts[1]?.split("=")[1];
    if (!userId || !authKey) {
        console.error("URL missing required parameters");
        return null;
    }
    return {userId, authKey};
}