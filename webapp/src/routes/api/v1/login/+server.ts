import { error, json } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import type { RequestHandler } from './$types';

interface OauthPayload {
    access_token: string;
    token_type: string;
    expires_in: number;
    refresh_token: string;
    scope: string;

}

export const POST: RequestHandler = async ({ request, fetch }) => {
    const response = await request.json();
    const data = {
        client_id: env.CLIENT_ID,
        client_secret: env.CLIENT_SECRET,
        grant_type: 'authorization_code',
        code: response.code,
        redirect_uri: env.REDIRECT_URI
    };
    const headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    };
    const req = await fetch('https://discord.com/api/oauth2/token', { method: 'POST', headers, body: new URLSearchParams(data) });
    const res: OauthPayload = await req.json()
    const token = `${res.token_type} ${res.access_token}`;
    const required_scope = ['identify', 'guilds.members.read', 'guilds', 'email'];
    const scopes = res.scope.split(' ');
    scopes.forEach((v: string) => {
        if (!required_scope.includes(v)) {
            throw error(405, 'Insufficient Scopes');
        }
    });
    return json(token, { status: 200 });
}
