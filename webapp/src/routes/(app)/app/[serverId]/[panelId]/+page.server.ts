import IPCController from "$controllers/ipc";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = ({ params }) => {
    const ipc = new IPCController();
    // const findPanel = async () => {
    //     const panel = await ipc.findPanels(Number(params.panelId));
    //     return panel

    // }

    const fetchMessages = async () => {
        const messages = await ipc.findPanelMessage(Number(params.panelId));
        return messages;
    }

    return {
        // panel: findPanel()
        messages: fetchMessages()
    }
}
