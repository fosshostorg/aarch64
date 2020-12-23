<script>
	import Router, { push } from 'svelte-spa-router';
	import Index from './pages/Index.svelte';
	import Create from './pages/Create.svelte';
	import Login from './pages/Login.svelte';
	import Project from './pages/Project.svelte';
	import NewProject from './pages/NewProject.svelte';
	import Sidebar from './components/Sidebar.svelte';
	import {location} from 'svelte-spa-router';
	import { afterUpdate, onMount } from 'svelte';
	import { getUserInfo, getUserInfoAndProjects, getUserProjects } from './utils';
	import { Projects, User } from './stores';
	import Dashboard from './Dashboard.svelte';

	const routes = {
		'/login': Login,
		'/dashboard': Dashboard,
		'/dashboard/*': Dashboard,
		'*': Login,
	}

	let authenticated = null;

	async function authenticate() {
		if ($location == '/login' || $location == '/login/') {
			return true;
		} else {
			let res = await getUserInfoAndProjects()
			console.log(res, 'RES')
			if (!(res.user == null)) {
				if (res.user.meta.success && res.projects.meta.success) {
					$User = res.user.data;
					$Projects = res.projects.data;
					return true;
				} else if (res.user.meta.message == "Not authenticated") {
					push('/login');
				}
			} else {
				push('/login')
			}
		}
	}

	onMount(async () => {
		authenticated = authenticate();
	})

	afterUpdate(() => {authenticated = authenticate()})

	function routeLoading(event) {
		console.log('test')
		// if ($User == null || $Projects == null) {
		// 	console.log('redirected');
		// 	push('/login');
		// }
	}

	function routeLoaded(event) {
		console.log('routeLoaded event')
	}

</script>

<main>
	{#if authenticated !== null}
		{#await authenticated}
		{:then value}
			{#if value}
			<Router {routes} />
			{/if}
		{/await}
	{/if}
</main>



<style>
	main {
		width: 100%;
		display: flex;
		min-width: 1300px;
	}
</style>