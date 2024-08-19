import UserController from '$controllers/user';
import { JWT_HASH } from '$env/static/private';
import jwt from 'jsonwebtoken';
import { redirect, type Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
    if (event.url.pathname.startsWith('/app')) {
        console.log("auth check for ", event.url.pathname);

        const token = event.cookies.get('token')
        const jtoken = event.cookies.get('jtkn')
        const currentPath = event.url.pathname + event.url.search

        if (!token) throw redirect(307, `/login?redirectTo=${currentPath}`);

        const userController = new UserController(token)

        // Check for jwt and tries to validate from it else from discord api
        if (!jtoken) {
            console.log('auth by discord api')
            const user = await userController.getUser() // shouldn't be this requested  on client side?
            if (!user) throw redirect(308, '/login')
            event.locals.user = user;
            const hash = jwt.sign({
                ...user,
                exp: Math.floor(Date.now() / 1000) + 3600 * 24,
            }, JWT_HASH)
            event.cookies.set('jtkn', hash, {
                path: '/',
                httpOnly: true,
                secure: false
            })

        } else {
            console.log('auth by jwt')
            try {
                event.locals.user = jwt.verify(jtoken, JWT_HASH)
            } catch (err) {
                console.log('jwt error ', err)
                event.cookies.delete('jtkn', { path: '/' })
                throw redirect(307, `/login?redirectTo=${currentPath}`)
            }
        }
        if (event.locals.user) event.locals.userController = userController
        console.log('access granted')



    }

    return await resolve(event);
}
