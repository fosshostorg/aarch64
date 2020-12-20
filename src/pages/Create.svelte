<script>
    import VMSelect from '../components/VMSelect.svelte';
    import Navbar from '../components/Navbar.svelte';
    import PageHeader from '../components/PageHeader.svelte';
    import { v4 as uuidv4 } from 'uuid';
    import Select from 'svelte-select';
    import { onMount } from 'svelte';

    let images = {};
    let tiers = {};
    let image = '';
    let tier = '';

    let projects = [
        {label: "vela's Project", route: '/projects/1', id: '1'}, 
        {label: "nqdrt1's Long Project Name", route: '/projects/2', id: '2'}
    ]

    let batch = 1;
    let hostnames = [uuidv4()];
    let project = projects[0];

    $: console.log(project)

    const addHost = (e) => {
        e.preventDefault();
        hostnames = [...hostnames, uuidv4()]
    }

    const removeHost = (e) => {
        e.preventDefault();
        hostnames.splice(-1, 1);
        hostnames = hostnames;
    }

    const createFormSubmit = (e) => {
        hostnames.forEach(async (hostname) => {

            const data = {
                hostname: hostname == '' || hostname == null ? uuidv4() : hostname,
                os: image,
                tier,
            }

            if (__production__) {
                const res = await fetch('__apiRoute__/projects', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: data
                })
                .then(res => res.json())
                .then(data => console.log(data))
                .catch(err => console.log(err))
            } else {
                console.log('%cFetch would have been posted with: ', "color: lightgreen")
                console.log(data);
            }
        })
    }

    const loadData = async () => {

        if (__production__) {
            await fetch('__apiRoute__/system')
            .then(res => res.json())
            .then(body => {tiers = body.data.tiers; images = body.data.images})
        } else {
            tiers = {
                't1': {vcpus: '1', memory: '1', disk: '32'},
                't2': {vcpus: '4', memory: '8', disk: '64'},
                't3': {vcpus: '8', memory: '16', disk: '10'},
                't4': {vcpus: '16', memory: '32', disk: '128'},
                't5': {vcpus: '32', memory: '64', disk: '128'},
            }

            images = {
                'Debian': {version: 'latest'},
                'Ubuntu': {version: 'latest'},
                'CentOS': {version: 'latest'}
            }

            image = Object.keys(images)[0];
            tier = Object.keys(tiers)[0];

        }
    }

    onMount(() => {
        loadData();
    })

</script>

<main>
    <Navbar breadcrumbs={['Dashboard', 'Manage', 'Create New VM']} />
    <div class="content">
        <PageHeader>Create VM</PageHeader>
        <div class="create-form">
            <form on:submit|preventDefault={createFormSubmit}>
                <span class="form-header">
                    Choose an image:
                </span>
                <div class="create-form-select">
                    <VMSelect data={images} bind:current={image} />
                </div>
                <span class="form-header">
                    Choose a tier:
                </span>
                <div class="create-form-select">
                    <VMSelect isOS={false} data={tiers} bind:current={tier} />
                </div>
                <span class="form-header">
                    Finalize and create:
                </span>
                <div class="create-form-final">
                    <div class="create-form-final-section">
                        <span class="create-form-subheader">
                            Batch creation:
                        </span>
                        <span class="create-form-subtitle">
                            Deploy multiple machines at the same time.
                        </span>
                        <div class="batch-create-button">
                            <button class="batch-create-add" on:click={(e) => {e.preventDefault(); if (batch < 5) {batch++; addHost(e)}}}>
                                <span class="material-icons">
                                    add
                                </span>
                            </button>
                            <div class="batch-label"><b>{batch}</b>VM{batch > 1 ? 's' : ''}</div>
                            <button class="batch-create-remove" on:click={(e) => {e.preventDefault(); if (batch > 1) { batch--, removeHost(e)}}}>
                                <span class="material-icons">
                                    remove
                                </span>
                            </button>
                        </div>
                        <div class="create-form-subheader">
                            Project:
                        </div>
                        <div class="select-wrapper">
                            <Select items={projects} selectedValue={project} optionIdentifier="id" isSearchable={false} isClearable={false}></Select>
                        </div>
                        <button class="submit" type="submit">
                            CREATE
                        </button>
                    </div>
                    <div class="create-form-final-section">
                        <span class="create-form-subheader">
                            Choose a hostname:
                        </span>
                        <span class="create-form-subtitle">
                            Give your machines a name.
                        </span>
                        {#each hostnames as hostname, index}
                        <input autocomplete="off" type="text" class="hostname-input" name={'hostname-' + index} bind:value={hostname} />
                        {/each}
                    </div>
                </div>
            </form>
        </div>
        
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
        --padding: 0px;
        --inputPadding: 0px;
        --listBorderRadius: 0px;
        --itemFirstBorderRadius: 0px;
        --itemIsActiveBG:  #0e0d0d;
        --itemHoverBG: #0e0d0d15;
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

    button.submit {
        width: 250px;
        margin-top: 40px;
        height: 40px;
        border: none;
        font-size: 22px;
        font-weight: bold;
        font-family: inherit;
        color: white;
        background-color: #46B0A6;
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
        opacity: .9;
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
        opacity: .7;
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

<!-- markup (zero or more items) goes here -->