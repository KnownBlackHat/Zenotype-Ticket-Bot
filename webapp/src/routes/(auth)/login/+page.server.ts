import { env } from '$env/dynamic/private';
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, cookies, url }) => {
    const token = cookies.get('token')
    const redirectTo = url.searchParams.get('redirectTo') || '/app'
    if (token) {
        const user_info = await fetch('https://discord.com/api/v10/users/@me', {
            headers: { Authorization: token }
        });
        if (user_info.status === 200) throw redirect(307, `/${redirectTo.slice(1)}`)
    }

    return { client_id: env.CLIENT_ID, redirect_uri: env.REDIRECT_URI };
}
