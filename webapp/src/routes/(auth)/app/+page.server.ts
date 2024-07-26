import UserController from "$controllers/user";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ cookies }) => {
    const userController = new UserController(cookies.get('token') ?? '');
    const guild = await userController.getFinalGuild()
    return { data: guild };
}
