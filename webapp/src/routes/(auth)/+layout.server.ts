import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "../login/$types";
import UserController from "$controllers/user";

export const load: PageServerLoad = async ({ cookies }) => {
    const token = cookies.get('token')
    if (!token) {
        redirect(307, '/login')
    } else {
        const user = new UserController(token);
        const info = await user.getUser()
        cookies.set('user_id', info.id.toString(),
            { sameSite: 'lax', secure: false, path: '/' });
        return info;
    }
}
