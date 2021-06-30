import { Writable, writable } from 'svelte/store';

export const Projects: Writable<Project[]> = writable([]);
export const User: Writable<User> = writable(null);
export const Snackbars: Writable<Snackbar[]> = writable([]);
