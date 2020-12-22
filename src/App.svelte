<script>
	import Router from 'svelte-spa-router';
	import Index from './pages/Index.svelte';
	import Create from './pages/Create.svelte';
	import Login from './pages/Login.svelte';
	import Project from './pages/Project.svelte';
	import Sidebar from './components/Sidebar.svelte';
	import {location} from 'svelte-spa-router';

	const routes = {
		'/create': Create,
		'/projects/*': Project,
		'*': Index,
	}

	$: console.log($location);

</script>

{#if $location.includes('login')}
<Login />
{:else}
<main>
	<Sidebar />
	<div>
		<Router {routes} />
	</div>

</main>
{/if}



<style>
	main {
		width: 100%;
		display: flex;
		min-width: 1300px;
	}

	div {
		/* margin-left: var(--sidebar-width); */
		width: calc(100% - var(--sidebar-width));
	}
</style>