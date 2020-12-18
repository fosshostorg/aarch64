<script>
	import Router from 'svelte-spa-router';
	import Index from './pages/Index.svelte';
	const routes = new Map();
	routes.set('*', Index);

</script>

<Router {routes} />

<style>

</style>