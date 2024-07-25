import { env } from "$env/dynamic/private";
import { redirect } from "@sveltejs/kit";

export interface UserInfo {
    id: BigInteger;
    username: string;
    global_name: string;
    avatar: string;
    premium_type?: number;
    email?: string;
    accent_color?: string;
}

export interface Guild {
    id: BigInteger;
    icon: string;
    permissions: string;
    name: string;
    description?: string;
    owner: boolean;
    owner_id: BigInteger
}

class UserController {
    constructor(public token: string) {
        this.token = token;
    }

    async #ireq(route: string) {
        const req = await fetch(`http://${env.IPC_DOMAIN}${route}`, {
            headers: { Authorization: this.token }
        });
        if (req.status !== 200) {
            throw redirect(307, '/login');
        }
        return await req.json()
    }

    async #req(route: string) {
        const req = await fetch(`https://discord.com/api/v10${route}`, {
            headers: { Authorization: this.token }
        });
        if (req.status !== 200) {
            throw redirect(307, '/login');
        }
        return await req.json()
    }

    public async getUser() {
        const user: UserInfo = await this.#req('/users/@me');
        return user;
    }

    public async getGuild() {
        const guilds: Guild[] = await this.#req('/users/@me/guilds');
        return { data: guilds };
    }

}

export default UserController;
