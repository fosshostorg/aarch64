<script lang="ts">
	import Navbar from "../components/Navbar.svelte";
	import PageHeader from "../components/PageHeader.svelte";
	import Router, { location } from "svelte-spa-router";
	import ProjectVM from "../components/ProjectVM.svelte";
	import { v4 as uuidv4 } from "uuid";
	import { Projects } from "../stores";
	import PageTitle from "../components/PageTitle.svelte";
	import ProjectVm from "../components/ProjectVM.svelte";
	import Resource from "./Resource.svelte";

	export let params: any = {};

	$: console.log(params);

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
	$: console.log(project);

	let views = ["RESOURCES", "SETTINGS"];
	let currentView = "RESOURCES";

	function toVM(vm: any): VM {
		return vm as VM;
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
			<span class="title"> Virtual Machines </span>
			{#if project.vms.length == 0}
				<div class="empty-list">Nothing to see here...</div>
				<button class="add-new-button"> ADD RESOURCES </button>
			{:else}
				<span class="labels">
					<div class="hostname-label">HOSTNAME</div>
					<div class="location-label">LOCATION</div>
					<div class="ip-label">IP</div>
				</span>
				<div class="vm-list">
					{#each project.vms as vm}
						<ProjectVM
							VM={toVM(vm)}
							link={'/dashboard/projects/' + project._id + '/resources/' + vm['uuid']} />
					{/each}
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

	button.add-new-button {
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
		padding: 0px 30px;
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
		flex-basis: 0px;
	}

	.ip-label {
		flex-grow: 1;
		flex-basis: 270px;
		display: flex;
		justify-content: center;
	}
</style>
