import { redirect } from "@sveltejs/kit";

interface UserInfo {
    id: BigInteger;
    username: string;
    global_name: string;
    avatar: string;
    premium_type: number;
    email: string;
}

class UserController {
    constructor(public token: string) {
        this.token = token;
    }

    public async getUser() {
        const req = await fetch('https://discord.com/api/v10/users/@me', {
            headers: { Authorization: this.token }
        });
        if (req.status !== 200) {
            throw redirect(307, '/login');
        }
        const user: UserInfo = await req.json();
        return user;
    }
}

export default UserController;
