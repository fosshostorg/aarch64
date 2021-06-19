<script lang="ts">
    import Navbar from "../components/Navbar.svelte";
    import PageHeader from "../components/PageHeader.svelte";
    import ProjectVM from "../components/ProjectVM.svelte";
    import { Projects, User } from "../stores";
    import PageTitle from "../components/PageTitle.svelte";
    import Input from "../components/Input.svelte";
    import Button from "../components/Button.svelte";
    import { push } from "svelte-spa-router";
    import Proxies from "../components/project/Proxies.svelte";
    import AuditLog from "./AuditLog.svelte";
    import { checkMeta, updateProjects } from "../utils";
import Settings from "../components/project/Settings.svelte";

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

    let project: Project;
    $: project = getProjectById(params.project_id, $Projects);

    let views = ["RESOURCES", "SETTINGS", "PROXIES", "AUDIT LOG"];
    let currentView = "RESOURCES";
</script>

<PageTitle title={project ? project.name : 'Project page'}/>

<main>
    {#if project}
        <Navbar breadcrumbs={[
			{label: 'Dashboard', path: '/dashboard'},
			{label: project.name, path: `/dashboard/projects/${project._id}`},
			]}/>
        <PageHeader options labels={views} baseHref={"/#/dashboard/projects/" + params.project_id} {params}>
            {project.name}
        </PageHeader>
        <div class="content">
            {#if params.page === null || params.page === "resources"}
                <span class="title">Virtual Machines</span><br>
                <span class="subtitle">{project.budget_used} out of {project.budget} allocated {project.budget === 1 ? "cores" : "core"} used</span>
                {#if project.vms.length === 0}
                    <div class="empty-list">
                        Nothing to see here...<br>
                        <Button href="/#/dashboard/create" style="margin-top: 20px;">CREATE VM</Button>
                    </div>
                {:else}
					<span class="labels">
						<div class="hostname-label">HOSTNAME</div>
						<div class="location-label">POP</div>
						<div class="ip-label">ADDRESS</div>
					</span>
                    <div class="vm-list">
                        {#each project.vms as vm}
                            <ProjectVM VM={vm} link={'/dashboard/projects/' + project._id + '/resources/' + vm['_id']}/>
                        {/each}
                    </div>
                {/if}
            {:else if params.page === "settings"}
                <Settings {project} {params}/>
            {:else if params.page === "proxies"}
                <Proxies {project}/>
            {:else if params.page === "auditlog"}
                <AuditLog admin={false} {params}/>
            {/if}
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

    div.empty-list {
        font-weight: 500;
        text-align: center;
        padding-bottom: 10px;
        color: #575656;
    }

    .content {
        width: calc(100% - 30px);
        margin-left: 15px;
        margin-top: 5px;
    }

    .title {
        color: #0e0d0d;
        opacity: 0.7;
        padding: 15px;
        font-size: 22px;
        font-weight: 500;
    }

    .subtitle {
        color: #0e0d0d;
        opacity: 0.7;
        padding: 15px;
        font-size: 15px;
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
        flex-grow: 0;
        margin-left: 40px;
        padding-left: 15px;
        flex-basis: 385px;
    }

    .location-label {
        flex-grow: 1;
        display: flex;
        justify-content: center;
        flex-basis: 0;
    }

    .ip-label {
        flex-grow: 1;
        flex-basis: 270px;
        display: flex;
        justify-content: center;
    }
</style>
