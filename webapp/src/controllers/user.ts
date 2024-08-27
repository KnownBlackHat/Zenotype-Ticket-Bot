import IPCController, { type Guild } from "./ipc";

export interface GuildMember {
    user: object;
    nick: string;
    avatar: string;
    roles: string[];
    joined_at: string;
    deaf: boolean;
    mute: boolean;
}

export interface UserInfo {
    id: BigInteger;
    username: string;
    global_name: string;
    avatar: string;
    premium_type?: number;
    email?: string;
    accent_color?: string;
}

class UserController {
    #token: string;
    #ipc: IPCController;

    constructor(public token: string) {
        this.#token = token;
        this.#ipc = new IPCController();
    }
    async #req(route: string, method: "GET" | "POST" = "GET", data?: object) {
        const options: RequestInit = {
            method, headers: {
                'Content-Type': 'application/json',
                'Authorization': this.#token
            },
        }
        if (method === "POST") {
            options.body = JSON.stringify(data)
        }

        const req = await fetch(`https://discord.com/api/v10${route}`, options);
        if (req.status.toString().startsWith('2')) {
            console.log("Access Denied By User Controller")
            return null
        }
        return await req.json()
    }

    public async getUser() {
        const user: UserInfo | null = await this.#req('/users/@me');
        return user;
    }

    public async getFinalGuild() {
        const guilds: Guild[] | null = await this.#req('/users/@me/guilds');
        if (!guilds) return guilds
        const ipcGuilds: Guild[] = await this.#ipc.getGuild()
        const availableGuild = guilds.filter(item => ipcGuilds.some(item2 => item2.id == item.id))
        return availableGuild;
    }

    public async getGuildMember(guildId: string) {
        const guildMember: GuildMember | null = await this.#req(`/users/@me/guilds/${guildId}/member`);
        return guildMember;
    }


    public async validate(guildId: string): Promise<boolean> {
        const role = await this.#ipc.getRole(guildId);
        const guildMember = await this.getGuildMember(guildId);
        if (guildMember?.roles.includes(role)) { return true };
        return false;
    }

}

export default UserController;
