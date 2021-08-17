<script lang="ts">
    /*globals System, Project, Pop, APIResponse */
    import VMSelect from '../components/VMSelect.svelte';
    import Navbar from '../components/Navbar.svelte';
    import PageHeader from '../components/PageHeader.svelte';
    import { v4 as uuidv4 } from 'uuid';
    import Select from 'svelte-select';
    import { onMount } from 'svelte';
    import { Projects, User } from '../stores';
    import { checkMeta, createVM } from '../utils';
    import { push } from 'svelte-spa-router';
    import PageTitle from '../components/PageTitle.svelte';
    import Spinner from '../components/Spinner.svelte';
    import Input from '../components/Input.svelte';
    import Button from '../components/Button.svelte';

    // TODO: Auto-fill correct project when redirected from project page

    /* Where fetched system details are stored */
    let data: System = {
        pops: [],
        plans: {},
        oses: {}
    };

    /* The currently selected image and plan */
    let image = '';
    let plan = '';

    /* Number of VMs to create in this batch */
    let batch = 1;
    /* List of hostnames used for each VM in the batch */
    let hostnames: string[] = [uuidv4()] as string[];
    /* The currently selected project, defaults to the first project the user has */
    let project: Project = $Projects[0] as Project;
    /* The currently selected locaiton */
    let location: Pop | null = null;

    /* Amount of budget used, amount left for creation */
    $: budget_used =
        project.budget_used + batch * (data.plans[plan] ? data.plans[plan]['vcpus'] : 0);
    $: can_create = budget_used <= project.budget || $User.admin == true;

    /* Loading screen */
    let showSpinner = false;

    /* Adds a new hostname field w/ increase in batch size */
    const addHost = (e: Event) => {
        e.preventDefault();
        if (batch >= 5 || project.budget_used + (batch+1) * (data.plans[plan] ? data.plans[plan]['vcpus'] : 0) > project.budget) {
            return;
        }
        batch++;
        hostnames = [...hostnames, uuidv4()];
    };

    /* Removes a hostname field w/ decrease in batch size */
    const removeHost = (e: Event) => {
        e.preventDefault();
        if (batch <= 1) {
            return;
        }
        batch--;
        hostnames.splice(-1, 1);
        hostnames = hostnames;
    };

    /* Resets hostnames and batch size to 1 */
    const resetHosts = () => {
        hostnames = [hostnames[0]];
        batch = 1;
    }

    /* Creates the VMs by looping through every hostname in the list, will wait until all in the batch have been created */
    const createFormSubmit = async () => {
        showSpinner = true;

        for (const hostname of hostnames) {
            await createVM(project._id, hostname, plan, image, location.name).catch(err =>
                console.log(err)
            );
        }

        showSpinner = false;
        void push('/dashboard/projects/' + project._id);
    };

    /* Loads the os, plan, and pop data */
    const loadData = async () => {
        await fetch('__apiRoute__/system')
            .then(res => res.json())
            .then((body: APIResponse<System>) => {
                if (!body.meta.success) {
                    checkMeta(body);
                    return;
                }

                data = body.data;

                image = Object.keys(data.oses)[0];
                plan = Object.keys(data.plans)[0];
                location = data.pops[0];
            });
    };

    onMount(() => {
        void loadData();
    });
</script>

<PageTitle title="AARCH64 | Create VM" />

<main>
    <Navbar
        breadcrumbs={[
            { label: 'Dashboard', path: '/dashboard' },
            { label: 'Create New VM', path: '/dashboard/create' }
        ]}
    />
    <div class="content">
        {#if $Projects.length > 0}
            {#if showSpinner}
                <div style="display: flex; justify-content: center;">
                    <Spinner />
                </div>
            {:else}
                <PageHeader>Create VM</PageHeader>
                <div class="create-form">
                    <form on:submit|preventDefault={createFormSubmit}>
                        <span class="form-header"> Choose an image: </span>
                        <div class="create-form-select">
                            {#if Object.keys(data.oses).length > 0}
                                <VMSelect bind:current={image} osOptions={data.oses} />
                            {:else}
                                <Spinner />
                            {/if}
                        </div>
                        <span class="form-header"> Choose a plan: </span>
                        <div class="create-form-select">
                            {#if Object.keys(data.plans).length > 0}
                                <VMSelect
                                    bind:current={plan}
                                    planOptions={data.plans}
                                    coreLimit={project.budget - project.budget_used}
                                    on:change={resetHosts}
                                />
                            {:else}
                                <Spinner />
                            {/if}
                        </div>
                        <span class="form-header"> Finalize and create: </span>
                        <div class="create-form-final">
                            <div class="create-form-final-section">
                                <span class="create-form-subheader">
                                    Batch creation:
                                </span>
                                <span class="create-form-subtitle">
                                    Deploy multiple machines at the same time
                                </span>
                                <div class="batch-create-button">
                                    <button
                                        class="batch-create-remove"
                                        on:click={removeHost}
                                    >
                                        <span class="material-icons"> remove </span>
                                    </button>
                                    <div class="batch-label">
                                        <b>{batch}</b>VM{batch > 1 ? 's' : ''}
                                    </div>
                                    <button
                                        class="batch-create-add"
                                        on:click={addHost}
                                    >
                                        <span class="material-icons"> add </span>
                                    </button>
                                </div>
                                <div class="create-form-subheader">Project:</div>
                                <div class="select-wrapper">
                                    <Select
                                        isClearable={false}
                                        isSearchable={false}
                                        items={$Projects}
                                        optionIdentifier="_id"
                                        getOptionLabel={option => {
                                            return option.name;
                                        }}
                                        getSelectionLabel={option => {
                                            if (option) return option.name;
                                        }}
                                        bind:selectedValue={project}
                                        on:select={resetHosts}
                                    />
                                    <!-- Just FYI, you might need to set some other function overrides from svelte-select. -->
                                </div>
                                <div class="create-form-subheader">Location:</div>
                                <div class="select-wrapper">
                                    {#if location !== null}
                                        <Select
                                            isClearable={false}
                                            isSearchable={false}
                                            items={data.pops}
                                            optionIdentifier="location"
                                            getOptionLabel={(option, filterText) => {
                                                return option.location;
                                            }}
                                            getSelectionLabel={option => {
                                                if (option) return option.location;
                                            }}
                                            bind:selectedValue={location}
                                        />
                                    {/if}
                                </div>
                                <div class="create-form-subheader">Project Usage:</div>
                                <span class="create-form-subtitle">
                                    Limit: {project.budget}
                                    {project.budget === 1 ? 'cores' : 'core'}
                                    <br />
                                    Current: {project.budget_used}
                                    {project.budget_used === 1 ? 'cores' : 'core'}
                                    <br />
                                    <span class={can_create ? '' : 'red-text'}
                                        >New: {budget_used}
                                        {budget_used === 1 ? 'cores' : 'core'}</span
                                    >
                                </span>
                                <Button
                                    class="submit-button"
                                    width="250px"
                                    color="#46b0a6"
                                    disabled={!can_create}>CREATE</Button
                                >
                                <span style="margin-bottom: 2rem;" />
                            </div>
                            <div class="create-form-final-section">
                                <span class="create-form-subheader"
                                    >Choose a hostname:</span
                                >
                                <span class="create-form-subtitle"
                                    >Give your machines a name</span
                                >
                                {#each hostnames as hostname, index}
                                    <Input
                                        autocomplete="off"
                                        type="text"
                                        class="hostname-input"
                                        name={'hostname-' + index}
                                        bind:value={hostname}
                                    />
                                {/each}
                            </div>
                        </div>
                    </form>
                </div>
            {/if}
        {:else}
            <PageHeader>You don't have any projects yet</PageHeader>
            <div class="create-form">
                <button class="large" on:click={() => push('/dashboard/projects/create')}
                    >CREATE PROJECT</button
                >
            </div>
        {/if}
    </div>
</main>

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

    div :global(.hostname-input) {
        width: 360px;
        margin-bottom: 1rem;
    }

    .red-text {
        color: red;
    }

    button.large {
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

    div :global(.submit-button) {
        margin-top: 10px;
    }

    div :global(.submit-button:active:not(.disabled)) {
        background-color: #46b05d !important;
        border-color: #46b05d !important;
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
        width: 40px;
        cursor: pointer;
    }

    .batch-create-button button:active {
        padding: 0 8px;
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
        display: flex;
        align-items: center;
    }

    .form-header:not(:first-child) {
        margin-top: 15px;
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
