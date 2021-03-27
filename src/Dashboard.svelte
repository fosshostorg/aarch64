<script>
	import Router, { push } from "svelte-spa-router";
	import Create from "./pages/Create.svelte";
	import Project from "./pages/Project.svelte";
	import NewProject from "./pages/NewProject.svelte";
	import Sidebar from "./components/Sidebar.svelte";
	import { Projects, User } from "./stores";
	import { onMount } from "svelte";
	import Resource from "./pages/Resource.svelte";

	const prefix = "/dashboard";
	const routes = {
		"/create": Create,
		"/projects/create": NewProject,
		"/projects/:project_id": Project,
		"/projects/:project_id/resources/:resource_id": Resource,
	};

	onMount(() => {
		if ($User == {} || $User == null || $User == "undefined") {
			console.log("redirected");
		}

		// Redirect to projects create page if user doesn't have any projects, otherwise redirect to their first project
		if ($Projects.length < 1) {
			push("/dashboard/projects/create")
		} else {
			push("/dashboard/projects/" + $Projects[0]._id)
		}
	});
</script>

{#if $User !== {}}
	<Sidebar />
	<div>
		<Router {routes} {prefix} />
	</div>
{/if}

<style>
	div {
		width: calc(100% - var(--sidebar-width));
	}
</style>
