import IPCController from "$controllers/ipc";
import UserController from "$controllers/user";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = ({ params, cookies }) => {
    const ipc = new IPCController();
    const token = cookies.get('token');
    const userController = new UserController(token ?? '');
    const panels = userController.validate(params.serverId).then((valid) => {

        if (!valid)
            throw error(403, 'validation failed')

        return ipc.getPanels(params.serverId)
    });

    return { panels };
}
