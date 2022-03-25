<script>
    import Router, { push } from 'svelte-spa-router';
    import Create from './pages/Create.svelte';
    import Project from './pages/Project.svelte';
    import NewProject from './pages/NewProject.svelte';
    import Sidebar from './components/Sidebar.svelte';
    import { Projects, User } from './stores';
    import { onMount } from 'svelte';
    import Resource from './pages/Resource.svelte';
    import AuditLog from './pages/AuditLog.svelte';
    import Account from './pages/Account.svelte';
    import { wrap } from 'svelte-spa-router/wrap';

    const prefix = '/dashboard';
    const routes = {
        '/create': Create,
        '/auditlog': wrap({
            component: AuditLog,
            props: {
                admin: true
            }
        }),
        '/account': Account,
        '/projects/create': NewProject,
        '/projects/:project_id/:page?': Project,
        '/projects/:project_id/resources/:resource_id': Resource
    };

    onMount(() => {
        // Redirect to projects create page if user doesn't have any projects, otherwise redirect to their first project
        if (
            window.location.hash === '#/dashboard' ||
            window.location.hash === '#/dashboard/'
        ) {
            if ($Projects.length < 1) {
                push('/dashboard/projects/create');
            } else {
                push('/dashboard/projects/' + $Projects[0]._id);
            }
        }
    });
</script>

<Sidebar />
<div>
    <Router {routes} {prefix} />
</div>

<style>
    div {
        width: 100%;
    }
</style>
