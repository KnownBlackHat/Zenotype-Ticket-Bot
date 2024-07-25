import { env } from "$env/dynamic/private";
import { redirect } from "@sveltejs/kit";


export interface Panel {
    title: string;
    thumbnail: string;
    image: string;
    description: string;
    category: BigInteger;
}

export default class IPCController {
    async #req(route: string) {
        const req = await fetch(`http://${env.IPC_DOMAIN}${route}`);
        if (req.status !== 200) {
            throw redirect(307, '/login');
        }
        return await req.json()
    }

    public async getPanels(guildId: string) {
        const panels: Panel[] = await this.#req(`/panels?guild=${guildId}`);
        return panels;
    }

}
