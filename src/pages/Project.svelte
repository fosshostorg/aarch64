<script lang="ts">
    import Navbar from '../components/Navbar.svelte';
    import PageHeader from '../components/PageHeader.svelte';
    import {location} from 'svelte-spa-router';
    import ProjectVM from '../components/ProjectVM.svelte';
    import {v4 as uuidv4} from 'uuid';
    import { Projects } from '../stores';
    import PageTitle from "../components/PageTitle.svelte";

    export let params: any = {};

    $: console.log($Projects);

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

    $: project = getProjectById(params.id, $Projects)
    $: console.log(project);

    let views = ['RESOURCES', 'SETTINGS']
    let currentView = 'RESOURCES';

    function toVM(vm: any): VM {
        return (vm as VM)
    }

</script>

<PageTitle title={project ? project.name : 'Project page'} />

<main>
    {#if project}
    <Navbar breadcrumbs={['Dashboard', 'Projects', project.name]} />
    <PageHeader options bind:current={currentView} labels={views}>{project.name}</PageHeader>
    <div class="content">
        <span class="title">
            Virtual Machines
        </span>
        <span class="labels">
            <div class="hostname-label">HOSTNAME</div>
            <div class="location-label">LOCATION</div>
            <div class="ip-label">IP</div>
        </span>
        <div class="vm-list">
            {#each project.vms as vm}
            <ProjectVM VM={toVM(vm)} link={'/dashboard/projects/' + project._id + '/resources/' + vm['hostname']}/>
            {/each}
        </div>
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

    .content {
        width: calc(100% - 30px);
        margin-left: 15px;
        margin-top: 5px;
    }

    .title {
        color: #0E0D0D;
        opacity: 0.7;
        padding: 15px;
        font-size: 22px;
        font-weight: 500;
    }
    
    span.labels {
        width: calc(100% - 65px);
        height: 20px;
        display: flex;
        align-items: flex-end;
        margin-left: 15px;
        font-weight: bold;
        font-size: 15px;
        margin-top: 5px;
    }

    .hostname-label {
        flex-grow: 1;
        margin-left: 55px;
    }

    .location-label {
        flex-grow: 1;
    }

    .ip-label {
        flex-grow: 2;
    }

</style>