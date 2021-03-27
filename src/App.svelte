<script>
	import Router from "svelte-spa-router";
	import { wrap } from "svelte-spa-router/wrap";
	import Index from "./pages/Index.svelte";
	import Login from "./pages/Login.svelte";
	import Signup from "./pages/Signup.svelte";
	import { onMount } from "svelte";
	import { consoleWelcomeMessage, getUserInfoAndProjects } from "./utils";
	import { Projects, User } from "./stores";
	import Dashboard from "./Dashboard.svelte";
	import NotFound from "./pages/NotFound.svelte";
	import MDPWrapper from "rollup-plugin-mdsvex-pages/src/components/MDPWrapper.svelte";

	const dashboardWrap = wrap({
		component: Dashboard,
		conditions: [
			async (detail) => {
				return await authenticate();
			},
		],
	});

	const routes = {
		"/": Index,
		"/login": Login,
		"/signup": Signup,
		"/dashboard": dashboardWrap,
		"/dashboard/*": dashboardWrap,
		"*": NotFound,
	};

	async function authenticate() {
		let res = await getUserInfoAndProjects();
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
