<script lang="ts">
	import Navbar from "../components/Navbar.svelte";
	import PageHeader from "../components/PageHeader.svelte";
	import ProjectVM from "../components/ProjectVM.svelte";
	import { Projects } from "../stores";
	import PageTitle from "../components/PageTitle.svelte";

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

	let views = ["RESOURCES", "SETTINGS"];
	let currentView = "RESOURCES";

	function toVM(vm: any): VM {
		return vm as VM;
	}

	let newUserEmail;

	function submitAddUser() {
		fetch("__apiRoute__/project/adduser", {
			method: "POST",
			headers: {"Content-Type": "application/json"},
			body: JSON.stringify({project: params.project_id, email: newUserEmail})
		})
			.then(resp => resp.json())
			.then(data => {
				alert(data.meta.message)
			})
			.catch((err) => alert(err));
	}
</script>

<PageTitle title={project ? project.name : 'Project page'} />

<main>
	{#if project}
		<Navbar breadcrumbs={[
			{label: 'Dashboard', path: '/dashboard'},
			{label: project.name, path: `/dashboard/projects/${project._id}`},
			]} />
		<PageHeader options bind:current={currentView} labels={views}>
			{project.name}
		</PageHeader>
		<div class="content">
			{#if currentView === "RESOURCES"}
					<span class="title">Virtual Machines</span>
					{#if project.vms.length === 0}
						<div class="empty-list">Nothing to see here...</div>
						<a href="/#/dashboard/create" class="add-new-button"> CREATE VM </a>
					{:else}
					<span class="labels">
						<div class="hostname-label">HOSTNAME</div>
						<div class="location-label">POP</div>
						<div class="ip-label">ADDRESS</div>
					</span>
						<div class="vm-list">
							{#each project.vms as vm}
								<ProjectVM VM={toVM(vm)} link={'/dashboard/projects/' + project._id + '/resources/' + vm['_id']} />
							{/each}
						</div>
					{/if}
			{:else if currentView === "SETTINGS"}
				<div>
					<span class="title">Settings</span>
					<div class="user-form-container">
						<span class="user-form-subheader">Users:</span>
						<ul>
							{#each project.users as user}
								<li>{user}</li>
							{/each}
						</ul>
					</div>

					<div class="user-form-container">
						<span class="user-form-subheader">Add user to project:</span>
						<span class="user-form-subtitle">Enter a user's email. Make sure they already have signed up for an account.</span>
						<input bind:value={newUserEmail} autocomplete="off" type="text" class="user-input" placeholder="user@example.com"/>
						<button class="user-form-button" on:click={() => submitAddUser()}>ADD USER</button>
					</div>
				</div>
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

    .add-new-button {
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 500;
        color: white;
        background-color: #0e0d0d;
        border: none;
        font-family: inherit;
        margin: 0 auto;
        font-size: 16px;
        padding: 0 30px;
        text-decoration: none;
        width: 150px;
    }

    button:active {
        opacity: 0.8;
    }

    div.empty-list {
        font-weight: 500;
        text-align: center;
        padding-bottom: 10px;
        opacity: 0.8;
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

	.user-form-container {
		display: flex;
		flex-direction: column;
		margin-top: 25px;
		padding-left: 15px;
	}

	.user-form-subheader {
		font-size: 22px;
		font-weight: 500;
	}

	.user-form-subtitle {
		font-size: 16px;
		opacity: 0.5;
		padding-bottom: 10px;
	}

	.user-input {
		height: 38px;
		margin: 0 0 10px 0;
		border: 1px solid #0e0d0d;
		color: #0e0d0d;
		padding: 0 0 0 10px;
		font-size: 18px;
		width: 350px;
	}

	.user-form-button {
		height: 40px;
		font-weight: 500;
		color: white;
		background-color: #0e0d0d;
		border: none;
		font-family: inherit;
		font-size: 16px;
		width: 150px;
	}
</style>
