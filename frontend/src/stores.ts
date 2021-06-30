import { Writable, writable } from 'svelte/store'

export const Projects: Writable<Project[]> = writable([])
export const User: Writable<any> = writable(null)
export const Snackbars: Writable<any[]> = writable([])
