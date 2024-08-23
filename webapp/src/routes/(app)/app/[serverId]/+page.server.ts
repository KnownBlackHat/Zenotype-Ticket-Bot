import IPCController from "$controllers/ipc";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const get_panels = async () => {
        if (!locals.userController.validate(params.serverId)) {
            throw redirect(403, '/app?msg="Unauthorized user"')
        }
        const ipc = new IPCController();
        return await ipc.getPanels(params.serverId)

    }
    return { panels: get_panels() };
}
