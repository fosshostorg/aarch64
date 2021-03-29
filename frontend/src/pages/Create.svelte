<script lang="ts">
	import VMSelect from "../components/VMSelect.svelte";
	import Navbar from "../components/Navbar.svelte";
	import PageHeader from "../components/PageHeader.svelte";
	import {v4 as uuidv4} from "uuid";
	import Select from "svelte-select";
	import {onMount} from "svelte";
	import {Projects} from "../stores";
	import {createVM, getMockSystemData, getUserProjects} from "../utils";
	import {push} from "svelte-spa-router";
	import PageTitle from "../components/PageTitle.svelte";
	import Spinner from "../components/Spinner.svelte";

	let images = {};
	let plans = {};
	let locations = [];
	let image = "";
	let plan = "";

	let batch = 1;
	let hostnames = [uuidv4()];
	let project = $Projects[0];
	let location = null;

	let showSpinner = false;

	// // Debugging
	// $: console.log(project)
	// $: console.log(location)

	const addHost = (e) => {
		e.preventDefault();
		hostnames = [...hostnames, uuidv4()];
	};

	const removeHost = (e) => {
		e.preventDefault();
		hostnames.splice(-1, 1);
		hostnames = hostnames;
	};

	const createFormSubmit = async (e) => {
		showSpinner = true;

		// @ts-ignore
		if (__production__) {
			if (hostnames.length > 1) {
				let project_id;
				for (const hostname of hostnames) {
					project_id = project._id;
					await createVM(project._id, hostname, plan, image, location.name)
							.then((data) => {
								console.log(data)
							}) // TODO: Forward here somehow
							.catch((err) => console.log(err));
				}
				await push("/dashboard/projects/" + project_id);
				return;
			}

			await createVM(project._id, hostnames[0], plan, image, location.name)
					.then((data) => {
						if (data !== null) {
							push("/dashboard/projects/" + project._id);
						} else {
							console.log(data)
						}
					})
					.catch((err) => console.log(err));

		} else {
			console.log(
					"%cFetch would have been posted with: ",
					"color: lightgreen"
			);
			console.log(project._id, hostnames, plan, image, location.name);
		}
	};

	const loadData = async () => {
		// @ts-ignore
		if (__production__) {
			await fetch("__apiRoute__/system")
					.then((res) => res.json())
					.then((body) => {
						if (!body.meta.success) {
							window.location.href = "/#/login";
						}

						let data: System = body.data as System;
						plans = data.plans;
						locations = data.pops;
						images = data.oses;

						image = Object.keys(images)[0];
						plan = Object.keys(plans)[0];
						location = locations[0];
					});
		} else { // !production
			let data: System = getMockSystemData() as System;
			plans = data.plans;
			locations = data.pops;
			images = data.oses;

			image = Object.keys(images)[0];
			plan = Object.keys(plans)[0];
			location = locations[0];
		}
	};

	onMount(() => {
		loadData();
	});
</script>

<PageTitle title="AARCH64 | Create VM" />

<main>
	<Navbar breadcrumbs={[
		{label: 'Dashboard', path:'/dashboard'},
		{label: 'Create New VM', path:'/dashboard/create'},
		]} />
	<div class="content">
		{#if $Projects.length > 0}
			{#if showSpinner}
				<div style="display: flex; justify-content: center;">
					<Spinner/>
				</div>
			{:else}
				<PageHeader>Create VM</PageHeader>
				<div class="create-form">
					<form on:submit|preventDefault={createFormSubmit}>
						<span class="form-header"> Choose an image: </span>
						<div class="create-form-select">
							<VMSelect bind:current={image} data={images} />
						</div>
						<span class="form-header"> Choose a plan: </span>
						<div class="create-form-select">
							<VMSelect bind:current={plan} data={plans} isOS={false} />
						</div>
						<span class="form-header"> Finalize and create: </span>
						<div class="create-form-final">
							<div class="create-form-final-section">
						<span class="create-form-subheader">
							Batch creation:
						</span>
								<span class="create-form-subtitle">
							Deploy multiple machines at the same time.
						</span>
								<div class="batch-create-button">
									<button
											class="batch-create-add"
											on:click={(e) => {
									e.preventDefault();
									if (batch < 5) {
										batch++;
										addHost(e);
									}
								}}>
										<span class="material-icons"> add </span>
									</button>
									<div class="batch-label">
										<b>{batch}</b>VM{batch > 1 ? 's' : ''}
									</div>
									<button
											class="batch-create-remove"
											on:click={(e) => {
									e.preventDefault();
									if (batch > 1) {
										batch--, removeHost(e);
									}
								}}>
										<span class="material-icons"> remove </span>
									</button>
								</div>
								<div class="create-form-subheader">Project:</div>
								<div class="select-wrapper">
									<Select
											isClearable={false}
											isSearchable={false}
											items={$Projects}
											optionIdentifier="_id"
											selectedValue={project}
											getOptionLabel={(option, filterText) => {
									return option.isCreator ? `Create \"${filterText}\"` : option.name;
								}}
											getSelectionLabel={(option) => {
									if (option) return option.name;
								}}
									/>
									<!-- Just FYI, you might need to set some other function overrides from svelte-select. -->
								</div>
								<div class="create-form-subheader">Location:</div>
								<div class="select-wrapper">
									{#if location !== null}
										<Select
												isClearable={false}
												isSearchable={false}
												items={locations}
												optionIdentifier="location"
												getOptionLabel={(option, filterText) => {
										return option.isCreator ? `Create \"${filterText}\"` : option.location;
									}}
												getSelectionLabel={(option) => {
										if (option) return option.location;
									}}
												bind:selectedValue={location} />
									{/if}
								</div>
								<button class="submit" type="submit"> CREATE </button>
							</div>
							<div class="create-form-final-section">
						<span class="create-form-subheader">
							Choose a hostname:
						</span>
								<span class="create-form-subtitle">
							Give your machines a name.
						</span>
								{#each hostnames as hostname, index}
									<input
											autocomplete="off"
											type="text"
											class="hostname-input"
											name={'hostname-' + index}
											bind:value={hostname} />
								{/each}
							</div>
						</div>
					</form>
				</div>
			{/if}
		{:else}
			<PageHeader>You don't have any projects yet</PageHeader>
			<div class="create-form">
				<button on:click={() => push("/dashboard/projects/create")}>CREATE PROJECT</button>
			</div>
		{/if}
	</div>
</main>
<!-- markup (zero or more items) goes here -->

<style>
	main {
		width: 100%;
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	.select-wrapper {
		--border: 1px solid #0e0d0d;
		--borderHoverColor: 1px solid #0e0d0d;
		--borderFocusColor: 1px solid #0e0d0d;
		--borderRadius: 0px;
		--height: 40px;
		width: 250px;
		--padding: 5px 0px;
		--inputPadding: 0px;
		--listBorderRadius: 0px;
		--itemFirstBorderRadius: 0px;
		--itemIsActiveBG: #0e0d0d;
		--itemHoverBG: #0e0d0d15;
		display: flex;
		flex-direction: column;
	}

	div.create-form-subheader {
		margin-top: 15px;
		padding-bottom: 5px;
	}

	.hostname-input {
		height: 38px;
		padding: 0px;
		margin: 0px 0px 10px 0px;
		border: 1px solid #0e0d0d;
		color: #0e0d0d;
		padding-left: 10px;
		font-size: 18px;
		width: 350px;
	}

	button {
		width: 250px;
		margin-top: 40px;
		height: 40px;
		border: none;
		font-size: 22px;
		font-weight: bold;
		font-family: inherit;
		color: white;
		background-color: black;
	}

	button.submit {
		width: 250px;
		margin-top: 40px;
		height: 40px;
		border: none;
		font-size: 22px;
		font-weight: bold;
		font-family: inherit;
		color: white;
		background-color: #46b0a6;
		transition: ease background-color 0.2s;
	}

	button.submit:active {
		padding: 0px 8px;
		background-color: #46b05d;
	}

	.batch-create-button {
		display: flex;
		width: 250px;
		align-items: center;
		justify-content: space-between;
	}

	.batch-create-button div {
		background-color: #0e0d0d;
		flex-grow: 1;
		height: 40px;
		border-left: 1px solid white;
		border-right: 1px solid white;
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 22px;
		font-weight: 300;
	}

	.batch-create-button div b {
		font-weight: bold;
		padding-right: 5px;
	}

	.batch-create-button button {
		background-color: #0e0d0d;
		border: none;
		height: 40px;
		cursor: pointer;
	}

	.batch-create-button button:active {
		padding: 0px 8px;
		opacity: 0.9;
	}

	.batch-create-button button span {
		color: white;
	}

	.create-form-subheader {
		font-size: 22px;
		font-weight: 500;
	}

	.create-form-subtitle {
		font-size: 16px;
		opacity: 0.5;
		padding-bottom: 10px;
	}

	.create-form-final-section {
		display: flex;
		flex-direction: column;
		margin-right: 15px;
	}

	.create-form-final {
		padding-left: 30px;
		display: flex;
	}

	.create-form-select {
		padding-left: 15px;
	}

	.form-header {
		font-weight: 500;
		opacity: 0.7;
		font-size: 28px;
		padding-left: 15px;
		height: 55px;
		display: inline-block;
		display: flex;
		align-items: center;
	}

	.create-form {
		width: auto;
		margin-left: 25px;
	}

	.content {
		width: 100%;
		display: flex;
		flex-direction: column;
	}
</style>
