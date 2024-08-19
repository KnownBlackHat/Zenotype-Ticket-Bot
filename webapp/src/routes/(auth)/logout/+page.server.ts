import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import { env } from "$env/dynamic/private";

export const load: PageServerLoad = async ({ cookies, fetch }) => {
    const token = cookies.get('token');
    if (token) {
        const payload = {
            client_id: env.CLIENT_ID,
            client_secret: env.CLIENT_SECRET,
            token: token.split(' ')[1],
            token_type: token.split(' ')[0]
        };
        const rep = await fetch('https://discord.com/api/oauth2/token/revoke', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams(payload)
        });
        if (rep.status === 200) {
            cookies.delete('token', { path: '/' });
            cookies.delete('jtkn', { path: '/' });
        }
    }
    throw redirect(301, '/login')
}
