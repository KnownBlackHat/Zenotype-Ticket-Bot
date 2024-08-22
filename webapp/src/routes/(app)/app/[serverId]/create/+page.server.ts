import type { Panel } from "$controllers/ipc";
import IPCController from "$controllers/ipc";
import type { Actions, Action } from "./$types";

const panelSubmit: Action = async ({ request }) => {
    const url = new URL(request.url);
    const data = await request.formData();

    const panel: object = {};
    for (const [key, value] of data) {
        if (!key.endsWith("(optional)") && !value) {
            return { success: false, error: `${key} was not defined` }; // FIX: Use invalid for error in forms
        }

        const nkey = key.replace("(optional)", "");
        panel[nkey] = value;
    }

    const guildId = url.pathname.split('/')[2];


    const ipc = new IPCController();
    const resp = await ipc.addPanel(guildId, panel as Panel);
    if (resp.success === false) {
        return { success: false, error: resp.error }
    }
    return { success: true };
}

export const actions: Actions = { panelSubmit }
