<script lang="ts">
    import Navbar from '../components/Navbar.svelte';
    import PageHeader from '../components/PageHeader.svelte';
    import PageTitle from '../components/PageTitle.svelte';
    import VMInfo from '../components/VMInfo.svelte';
    import {Projects} from '../stores'

    export let params: any = {};

    $: console.log(params);

    const getProjectById = (id: string, _projects: any[]) => {
        let returnProject = null;
        let projects = [ ..._projects ];
        projects.forEach((project) => {
            if (project._id == id) {
                returnProject = project;
            }
        })
        return returnProject;
    }

    $: project = getProjectById(params.project_id, $Projects)
    $: console.log(project.vms);

    function toVM(vm: any): VM {
        return (vm as VM)
    }

</script>

<PageTitle title="Resources" />

<main>
    {#if project}
    <Navbar breadcrumbs={['Dashboard', 'Projects', project.name]} />
    <PageHeader>{project.name}</PageHeader>

    {#each project.vms as vm}
        {#if toVM(vm).uuid == params.resource_id}
            <div>
                <VMInfo vm={toVM(vm)} />
            </div>
            
        {/if}
    {/each}
    {/if}
</main>


<style>
    main {
        width: 100%;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    div {
        margin-left: 40px;
        margin-top: 20px;
    }

</style>