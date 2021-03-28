<script lang="ts">
    import Navbar from "../components/Navbar.svelte";
    import PageHeader from "../components/PageHeader.svelte";
    import PageTitle from "../components/PageTitle.svelte";
    import VMInfo from "../components/VMInfo.svelte";
    import IPInfo from "../components/IPInfo.svelte";
    import VMOptions from "../components/VMOptions.svelte";
    import {Projects} from "../stores";
    import {push} from "svelte-spa-router";
    import CopyField from "../components/CopyField.svelte";

    export let params: any = {};

    const getProjectById = (id: string, _projects: any[]) => {
        let returnProject = null;
        let projects = [..._projects];
        projects.forEach((project) => {
            if (project._id == id) {
                returnProject = project;
            }
        });
        return returnProject;
    };

    $: project = getProjectById(params.project_id, $Projects);

    function toVM(vm: any): VM {
        return vm as VM;
    }
</script>

<PageTitle title="AARCH64 | VMs"/>

<main>
    {#if project}
        {#each project.vms as vm}
            {#if toVM(vm)._id === params.resource_id}
                <Navbar breadcrumbs={[
				{label: 'Dashboard', path: '/dashboard/'},
				{label: project.name, path: `/dashboard/projects/${project._id}`},
				{label: 'Resource', path: `/dashboard/projects/${project._id}/resources/${vm._id}`}
				]}/>
                <PageHeader>{toVM(vm).hostname}</PageHeader>
                <div class="wrapper">
                    <div class="info">
                        <span class="title">System:</span>
                        <span class="info-wrapper">
							<VMInfo vm={toVM(vm)}/>
						</span>
                        <span class="title">Network:&nbsp;<span class="material-icons" on:click={() => {push("/docs/networking")}}>help_outline</span></span>
                        <IPInfo vm={toVM(vm)}/>
                        <CopyField text={vm.password}/>
                    </div>
                    <div class="actions">
                        <VMOptions vm={toVM(vm)}/>
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

    .material-icons {
        cursor: pointer;
    }
</style>
