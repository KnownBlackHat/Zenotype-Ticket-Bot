import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = ({ locals }) => {
    const guilds = locals.userController.getFinalGuild()
    return { guilds };
}
