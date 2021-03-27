<script>
	import Router, { push } from "svelte-spa-router";
	import { wrap } from "svelte-spa-router/wrap";
	import Index from "./pages/Index.svelte";
	import Create from "./pages/Create.svelte";
	import Login from "./pages/Login.svelte";
	import Project from "./pages/Project.svelte";
	import NewProject from "./pages/NewProject.svelte";
	import Sidebar from "./components/Sidebar.svelte";
	import { location } from "svelte-spa-router";
	import { afterUpdate, onMount } from "svelte";
	import {
		consoleWelcomeMessage,
		getUserInfo,
		getUserInfoAndProjects,
		getUserProjects,
	} from "./utils";
	import { Projects, User } from "./stores";
	import Dashboard from "./Dashboard.svelte";
	import NotFound from "./pages/NotFound.svelte";
	import MDPWrapper from "rollup-plugin-mdsvex-pages/src/components/MDPWrapper.svelte";

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
			},
		],
	});

	const routes = {
		"/": Index,
		"/login": Login,
		"/dashboard": dashboardWrap,
		"/dashboard/*": dashboardWrap,
		"*": NotFound,
	};

	async function authenticate() {
		let res = await getUserInfoAndProjects();
		console.log(res, "RES");
		$User = res.user;
		$Projects = res.projects;
		return true;
	}

	function conditionsFailed(event) {
		console.log("conditions failed");
	}

	function routeLoaded(event) {
		console.log("routeLoaded event");
	}

	onMount(() => {
		consoleWelcomeMessage();
	});
</script>

<MDPWrapper>
	<main>
		<Router {routes} on:conditionsFailed={conditionsFailed} />
	</main>
</MDPWrapper>

<style>
	main {
		width: 100%;
		display: flex;
		min-width: 1300px;
	}
</style>
