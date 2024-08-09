import { env } from '$env/dynamic/private';
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, cookies }) => {
    const token = cookies.get('token')
    if (token) {
        const user_info = await fetch('https://discord.com/api/v10/users/@me', {
            headers: { Authorization: token }
        });
        if (user_info.status === 200) return redirect(307, '/app')
    }

    return { client_id: env.CLIENT_ID, redirect_uri: env.REDIRECT_URI };
}
