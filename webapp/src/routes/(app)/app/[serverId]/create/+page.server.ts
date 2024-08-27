import type { Panel } from "$controllers/ipc";
import IPCController from "$controllers/ipc";
import type { Actions, Action } from "./$types";

function panelBuilder(data: FormData): Panel {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const panel: any = {};
    for (const [key, value] of data) {
        if (!key.endsWith("(optional)") && !value) {
            throw Error(`${key} was not defined`)
        }

        const nkey = key.replace("(optional)", "");
        panel[nkey] = value;
    }
    return panel as Panel
}

const panelSubmit: Action = async ({ request }) => {
    const url = new URL(request.url);
    const data = await request.formData();
    const guildId = url.pathname.split('/')[2];
    const ipc = new IPCController();
    let panel: Panel;

    try {
        panel = panelBuilder(data)
    } catch (error) {
        return { success: false, error }; // FIX: Use invalid for error in forms
    }
    const resp = await ipc.addPanel(guildId, panel);
    if (resp.success === false) {
        return { success: false, error: resp.error }
    }

    return { success: true };
}

export const actions: Actions = { panelSubmit }
