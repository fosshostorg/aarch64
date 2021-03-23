<script lang="ts">
	import Navbar from "../components/Navbar.svelte";
	import PageHeader from "../components/PageHeader.svelte";
	import PageTitle from "../components/PageTitle.svelte";
	import VMInfo from "../components/VMInfo.svelte";
	import IPInfo from "../components/IPInfo.svelte";
	import VMOptions from "../components/VMOptions.svelte";
	import { Projects } from "../stores";

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
	$: console.log(project.vms);

	function toVM(vm: any): VM {
		return vm as VM;
	}
</script>

<PageTitle title="Resources" />

<main>
	{#if project}
		{#each project.vms as vm}
			{#if toVM(vm).uuid == params.resource_id}
			<Navbar breadcrumbs={[
				{label: 'Dashboard', path: '/dashboard/'},
				{label: project.name, path: `/dashboard/projects/${project._id}`},
				{label: 'Resource', path: `/dashboard/projects/${project._id}/resources/${vm.uuid}`}
				]} />
				<PageHeader>{toVM(vm).hostname}</PageHeader>
				<div class="wrapper">
					<div class="info">
						<span class="title">System:</span>
						<span class="info-wrapper">
							<VMInfo vm={toVM(vm)} />
						</span>
						<span class="title">Network:</span>
						<IPInfo vm={toVM(vm)} />
					</div>
					<div class="actions">
						<VMOptions vm={toVM(vm)} />
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
		display: block;
		margin: 10px 0px;
	}
</style>
