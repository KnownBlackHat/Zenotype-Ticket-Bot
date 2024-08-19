import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, fetch, request }) => {
    const url = new URL(request.url);
    const code = url.searchParams.get('code');
    if (!code) {
        throw redirect(307, '/app');
    }
    const resp = await fetch('/api/v1/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code })
    });
    if (resp.status === 200) {
        cookies.set('token', await resp.json(), {
            path: '/',
            httpOnly: true,
            secure: false
        });
        throw redirect(307, '/app');
    }
    throw redirect(307, '/app');
}
