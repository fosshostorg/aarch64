<script>
	import Router, { push } from 'svelte-spa-router';
	import Index from './pages/Index.svelte';
	import Create from './pages/Create.svelte';
	import Login from './pages/Login.svelte';
	import Project from './pages/Project.svelte';
	import NewProject from './pages/NewProject.svelte';
	import Sidebar from './components/Sidebar.svelte';
	import {location} from 'svelte-spa-router';
	import { onMount } from 'svelte';
	import { getUserInfo, getUserInfoAndProjects, getUserProjects } from './utils';
	import { Projects, User } from './stores';
	import Dashboard from './Dashboard.svelte';

	const routes = {
		'/login': Login,
		'/dashboard': Dashboard,
		'/dashboard/*': Dashboard,
		'*': Login,
	}

	let authenticated = false;

	onMount(async () => {
		if (!$location.includes('login')) {
			if ($User == {} || $Projects == []) {
				push('/login');
			} else {
				await getUserInfoAndProjects()
				.then(res => {
					console.log(res, 'RES')
					if (!(res.user == null)) {
						if (res.user.meta.success && res.projects.meta.success) {
							$User = res.user.data.data;
							$Projects = res.projects.data.data;
						}
					} else {
						// if (res.user.meta.message = "Not authenticated") {
						// 	push('/login');
						// }
						push('/login')
					}
				})
			}
		}
	})

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
	<Router {routes} />
</main>



<style>
	main {
		width: 100%;
		display: flex;
		min-width: 1300px;
	}
</style>