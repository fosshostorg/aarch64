<script>
	import Router from 'svelte-spa-router';
	import Index from './pages/Index.svelte';
	import Create from './pages/Create.svelte'
	import Sidebar from './components/Sidebar.svelte'
	
	const routes = new Map();
	routes.set('/create', Create);
	routes.set('*', Index);

</script>

<main>
	<Sidebar />
	<div>
		<Router {routes} />
	</div>

</main>


<style>
	main {
		width: 100%;
		display: flex;
	}

	div {
		/* margin-left: var(--sidebar-width); */
		width: calc(100% - var(--sidebar-width));
	}
</style>