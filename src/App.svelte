<script lang="ts">
	import Router, { push } from 'svelte-spa-router';
	import {wrap} from 'svelte-spa-router/wrap';
	import Index from './pages/Index.svelte';
	import Create from './pages/Create.svelte';
	import Login from './pages/Login.svelte';
	import Project from './pages/Project.svelte';
	import NewProject from './pages/NewProject.svelte';
	import Sidebar from './components/Sidebar.svelte';
	import {location} from 'svelte-spa-router';
	import { afterUpdate, onMount } from 'svelte';
	import { consoleWelcomeMessage, getUserInfo, getUserInfoAndProjects, getUserProjects } from './utils';
	import { Projects, User } from './stores';
	import Dashboard from './Dashboard.svelte';
	import NotFound from './pages/NotFound.svelte';

	const dashboardWrap = wrap({
			component: Dashboard,
			conditions: [
				async (detail) => {
					const res = await authenticate();

					if (res) {
						return true; 
					} else {
						return false;
					}
				}
			]
		})

	const routes = {
		'/login': Login,
		'/dashboard': dashboardWrap,
		'/dashboard/*': dashboardWrap,
		'*': NotFound,
	}

	let authenticated = null;

	async function authenticate() {
		let res = await getUserInfoAndProjects()
		console.log(res, 'RES')
		if (res.user !== null) {
			if (res.user.meta.success && res.projects.meta.success) {
				$User = res.user.data;
				$Projects = res.projects.data;
				return true;
			} else if (res.user.meta.message == "Not authenticated") {
				push('/login')
				return false;
			}
		} else {
			push('/login')
			return false;
		}
	}

	// onMount(async () => {
	// 	authenticated = authenticate();
	// })

	// afterUpdate(() => {authenticated = authenticate()})

	function conditionsFailed(event) {
		console.log('conditions failed')
		// push('/login');
	}

	function routeLoaded(event) {
		console.log('routeLoaded event')
	}

	onMount(() => {
		consoleWelcomeMessage();
	})
                                                                            

</script>

<main>
	<Router {routes} on:conditionsFailed={conditionsFailed} />
</main>



<style>
	main {
		width: 100%;
		display: flex;
		min-width: 1300px;
	}
</style>