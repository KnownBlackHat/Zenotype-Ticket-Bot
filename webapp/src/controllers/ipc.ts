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
    async #req(route: string, method: "GET" | "POST" = "GET", data?: string) {
        const options: RequestInit = {
            method, headers: {
                'Content-Type': 'application/json',
            }
        }
        if (method === "POST") {
            options.body = JSON.stringify(data)
        }

        const req = await fetch(`http://${env.IPC_DOMAIN}${route}`, options);
        if (req.status !== 200) {
            throw redirect(307, '/login');
        }
        return await req.json()
    }

    public async getPanels(guildId: string): Promise<Panel[]> {
        const panels: Panel[] = await this.#req(`/panels?guild=${guildId}`);
        return panels;
    }

}