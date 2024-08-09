import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, fetch, request }) => {
    const url = new URL(request.url);
    const code = url.searchParams.get('code');
    if (!code) {
        redirect(307, '/');
    }
    const resp = await fetch('/api/v1/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code })
    });
    if (resp.status === 200) {
        cookies.set('token', await resp.json(), { sameSite: 'lax', secure: false, path: '/' });
        redirect(307, '/');
    }
    redirect(307, '/');
}
