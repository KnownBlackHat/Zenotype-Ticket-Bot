import type { Panel } from "$controllers/ipc";
import IPCController from "$controllers/ipc";

export const actions = {
    default: async ({ request }: { request: Request }) => {
        const data = await request.formData();
        const guildId = data.get('serverId') as string;
        const panel: unknown = {

            title: data.get('title') as string,
            description: data.get('description') as string,
            color: data.get('color') as string,
            channel: data.get('channel') as string,
            disable_panel: data.get('disable_panel') as string,
            button_color: data.get('button_color') as string,
            button_text: data.get('button_text') as string,
            button_emoji: data.get('button_emoji') as string,
            mention_on_open: data.get('mention_on_open') as string,
            support_team: data.get('support_team') as string,
            category: data.get('category') as string,
            naming_scheme: data.get('naming_scheme') as string,
            large_image_url: data.get('large_image_url') as string,
            small_image_url: data.get('small_image_url') as string,
            wlcm_title: data.get('wlcm_title') as string,
            wlcm_description: data.get('wlcm_description') as string,
            wlcm_color: data.get('wlcm_color') as string,
            author_name: data.get('author_name') as string,
            author_icon_url: data.get('author_icon_url') as string,
            role: data.get('role') as string,

        }
        const ipc = new IPCController();
        const resp = await ipc.addPanel(guildId, panel as Panel);
        return resp;
    }
}
