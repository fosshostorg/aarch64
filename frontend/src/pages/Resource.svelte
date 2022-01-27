<script lang="ts">
    /*globals Project */
    import Navbar from '../components/Navbar.svelte';
    import PageHeader from '../components/PageHeader.svelte';
    import PageTitle from '../components/PageTitle.svelte';
    import VMInfo from '../components/VMInfo.svelte';
    import VMOptions from '../components/VMOptions.svelte';
    import { Projects } from '../stores';
    import CopyField from '../components/CopyField.svelte';
    import CreationInfo from '../components/CreationInfo.svelte';

    export let params: { project_id: string; resource_id: string } = {
        project_id: '',
        resource_id: ''
    };

    const getProjectById = (id: string, _projects: Project[]): Project => {
        let returnProject: Project = {};
        let projects = [..._projects];
        projects.forEach(project => {
            if (project._id == id) {
                returnProject = project;
            }
        });
        return returnProject;
    };

    let project: Project;
    $: project = getProjectById(params.project_id, $Projects);
</script>

<PageTitle title="AARCH64 | VMs" />

<main>
    {#if project}
        {#each project.vms as vm}
            {#if vm._id === params.resource_id}
                <Navbar
                    breadcrumbs={[
                        { label: 'Dashboard', path: '/dashboard/' },
                        {
                            label: project.name,
                            path: `/dashboard/projects/${project._id}`
                        },
                        {
                            label: 'Resource',
                            path: `/dashboard/projects/${project._id}/resources/${vm._id}`
                        }
                    ]}
                />
                <PageHeader isResource state={vm.state}>{vm.hostname}</PageHeader>
                <div class="wrapper">
                    <div class="info">
                        <span class="title">System:</span>
                        <span class="info-wrapper">
                            <VMInfo {vm} />
                        </span>
                        <CreationInfo {vm} />
                        <CopyField label="Address" text={vm.address.slice(0, -3)} />
                        <CopyField text={vm.password} />

                        {#if vm.nat != undefined}
                            <CopyField label="NAT Address" text={vm.nat.vm} />
                            <CopyField label="NAT Gateway" text={vm.nat.host.slice(0, -3)} />
                        {/if}
                    </div>
                    <div class="actions">
                        <VMOptions {vm} />
                    </div>
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

    div.wrapper {
        margin-left: 40px;
        margin-top: 20px;
        display: flex;
        justify-content: space-between;
    }

    div.info {
        display: flex;
        flex-direction: column;
        padding-right: 20px;
    }

    div.actions {
        display: flex;
        margin-right: 25px;
        border-left: 1px solid #ccc;
    }

    span.title {
        font-size: 24px;
        opacity: 0.7;
        font-weight: 500;
        margin: 10px 0px;
        display: flex;
        align-items: center;
    }
</style>
