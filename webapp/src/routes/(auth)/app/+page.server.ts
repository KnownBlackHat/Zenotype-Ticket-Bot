import UserController from "$controllers/user";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = ({ cookies }) => {
    const userController = new UserController(cookies.get('token') ?? '');
    const guilds = userController.getFinalGuild()
    return { guilds };
}
