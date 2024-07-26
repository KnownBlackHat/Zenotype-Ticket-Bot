import IPCController from "$controllers/ipc";
import UserController from "$controllers/user";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, cookies }) => {
    const ipc = new IPCController();
    const token = cookies.get('token');
    const userController = new UserController(token ?? '');
    const validation = await userController.validate(params.serverId);
    if (!validation)
        throw error(403, 'validation failed')

    const panels = await ipc.getPanels(params.serverId)
    return { data: panels }
}
