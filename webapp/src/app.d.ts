// See https://kit.svelte.dev/docs/types#app

import type UserController from "$controllers/user";
import type { UserInfo } from "$controllers/user";

// for information about these interfaces
declare global {
    namespace App {
        // interface Error {}
        interface Locals {
            user: UserInfo;
            userController: UserController;
        }
        // interface PageData {}
        // interface PageState {}
        // interface Platform {}
    }
}

export { };
