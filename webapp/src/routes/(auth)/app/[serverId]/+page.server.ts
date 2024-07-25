import IPCController from "$controllers/ipc";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
    const ipc = new IPCController();
    const panels = await ipc.getPanels(params.serverId)
    return { data: panels }
}
