<script>
    import Navbar from '../components/Navbar.svelte';
    import PageHeader from '../components/PageHeader.svelte';
    import {location} from 'svelte-spa-router';

    let projects = [
        {label: "vela's Project", route: '/projects/1', id: '1'}, 
        {label: "nqdrt1's Long Project Name", route: '/projects/2', id: '2'}
    ]

    const getProjectById = (id) => {
        let returnProject = null;
        projects.forEach((project) => {
            if (project.id == id) {
                returnProject = project;
            }
        })
        return returnProject;
    }

    $: project = getProjectById($location.split('/')[2]);


    let views = ['RESOURCES', 'SETTINGS']
    let currentView = 'RESOURCES';

</script>

<main>
    {#if project}
    <Navbar breadcrumbs={['Dashboard', 'Projects', project.label]} />
    <div class="content">
        <PageHeader options bind:current={currentView} labels={views}>{project.label}</PageHeader>
    </div>
    {/if}
</main>

<style>

    main {
        width: 100%;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    

</style>