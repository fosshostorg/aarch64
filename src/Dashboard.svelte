<script>
    import Router from 'svelte-spa-router';
    import Index from './pages/Index.svelte';
	import Create from './pages/Create.svelte';
	import Project from './pages/Project.svelte';
	import NewProject from './pages/NewProject.svelte';
    import Sidebar from './components/Sidebar.svelte';
    import { User } from './stores';
    import { onMount } from 'svelte';
    
    const prefix = '/dashboard'
    const routes = {
        '/create': Create,
		'/projects/create': NewProject, 
		'/projects/*': Project,
		'*': Index,
    }

    onMount(() => {
        if ($User == {} || $User == null || $User == 'undefined') {
            console.log('redirected')
        }
    })

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
