import IPCController from "$controllers/ipc";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = ({ params }) => {
    const ipc = new IPCController();
    const fetchTickets = async () => {
        const tickets = await ipc.getTickets(Number(params.panelId))
        return tickets
    }

    return {
        tickets: fetchTickets()
    }
}
