import { env } from "$env/dynamic/private";


export interface Guild {
    id: BigInteger;
    icon: string;
    name: string;
    description?: string;
    owner_id: BigInteger
}

export interface Panel {
    id: number;
    title: string;
    description: string;
    color: string;
    channel: BigInteger;
    disable_panel: boolean;
    button_color: string;
    button_text: string;
    button_emoji: string;
    mention_on_open: string;
    support_team: BigInteger[];
    category: BigInteger;
    naming_scheme: string;
    large_image_url: string;
    small_image_url: string;
    wlcm_title?: string;
    wlcm_description?: string;
    wlcm_color?: string;
    author_name: string;
    author_icon_url?: string;
    role: BigInteger;
}

export interface Message {
    userId: BigInteger,
    userName: string,
    channel: BigInteger
    message: string,
    createdAt: object,
    updatedAt: object
}

export interface Ticket {
    id: number;
    userId: BigInteger;
}

export default class IPCController {
    async #req(route: string, method: "GET" | "POST" = "GET", data?: Record<string, unknown>) {
        const options: RequestInit = {
            method, headers: {
                'Content-Type': 'application/json',
            }
        }
        if (method === "POST") {
            options.body = JSON.stringify(data)
        }

        const req = await fetch(`http://${env.IPC_DOMAIN}${route}`, options);
        return await req.json()
    }

    public async getPanels(guildId: string): Promise<Panel[]> {
        const panels: Panel[] = await this.#req(`/panels?guild=${guildId}`);
        return panels;
    }

    public async findPanels(id: number): Promise<Panel> {
        const panels: Panel = await this.#req(`/panels/find?panel=${id}`);
        return panels;
    }

    public async findTicketMessage(id: number): Promise<Message[]> {
        const messages: Message[] = await this.#req(`/messages?ticket=${id}`);
        return messages;
    }

    public async getTickets(id: number): Promise<Ticket[]> {
        const tickets: Ticket[] = await this.#req(`/tickets?panel=${id}`);
        return tickets;
    }

    public async addPanel(guildId: string, panel: Panel): Promise<{ success: boolean, error: string }> {
        const response: { success: boolean, error: string } = await this.#req(`/panels/add?guild=${guildId}`, "POST", { ...panel });
        return response;
    }


    public async getRole(guildId: string): Promise<string> {
        const role: { role: string } = await this.#req(`/role?guild=${guildId}`);
        return role.role;
    }

    public async getGuild() {
        const guilds: Guild[] = await this.#req('/guilds');
        return guilds;
    }

}
