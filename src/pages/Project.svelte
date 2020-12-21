<script>
    import Navbar from '../components/Navbar.svelte';
    import PageHeader from '../components/PageHeader.svelte';
    import {location} from 'svelte-spa-router';
    import ProjectVM from '../components/ProjectVM.svelte';
    import {v4 as uuidv4} from 'uuid';

    let projects = [
        {label: "vela's Project", route: '/projects/1', id: '1', vms: {
            '58b8e1f0-412e-4c7e-8b0d-172a268c5d29': {os: 'Debian', ip: '54.134.44.5', online: true},
            '52abafc8-e4d8-47f6-a884-d0b9a6c961d3': {os: 'Ubuntu', ip: '54.134.44.6', online: true},
            '7b519a16-d321-45c5-a9f4-7627d521c391': {os: 'CentOS', ip: '54.134.44.7', online: false},
        }},
        {label: "nqdrt1's Long Project Name", route: '/projects/2', id: '2', vms: {}}
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
    <PageHeader options bind:current={currentView} labels={views}>{project.label}</PageHeader>
    <div class="content">
        <span class="title">
            Virtual Machines
        </span>
        <div class="vm-list">
            {#each Object.keys(project.vms) as vm}
            <ProjectVM os={project.vms[vm].os} link={'/projects/' + project.id + '/resources/' + vm} name={vm} ip={project.vms[vm].ip} online={project.vms[vm].online}/>
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
    

</style>