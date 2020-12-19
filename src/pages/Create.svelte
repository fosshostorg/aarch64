<script>
    import VMSelect from '../components/VMSelect.svelte'
    import { v4 as uuidv4 } from 'uuid';

    let images = [
        {title: 'Debian', img: './img/debian.svg', version: 'latest'},
        {title: 'Ubuntu', img: './img/ubuntu.svg', version: 'latest'},
        {title: 'CentOS', img: './img/centos.svg', version: 'latest'}
    ]

    let tiers = [
        {title: 'Tier 1', vCPU: '1', RAM: '1GB', SSD: '32GB'},
        {title: 'Tier 2', vCPU: '4', RAM: '8GB', SSD: '64GB'},
        {title: 'Tier 3', vCPU: '8', RAM: '16GB', SSD: '10GB'},
        {title: 'Tier 4', vCPU: '16', RAM: '32GB', SSD: '128GB'},
        {title: 'Tier 5', vCPU: '32', RAM: '64GB', SSD: '128GB'},
    ]

    let batch = 1;

    let hostnames = [uuidv4()];

    const addHost = (e) => {
        e.preventDefault();
        hostnames = [...hostnames, uuidv4()]
    }

    const removeHost = (e) => {
        e.preventDefault();
        hostnames.splice(-1, 1);
        hostnames = hostnames;
    }

</script>

<main>
    <nav>
        <div class="breadcrumb">
            <span class="breadcrumb-text">
                Dashboard
            </span>
            <span class="material-icons icon">
                chevron_right
            </span>
            <span class="breadcrumb-text">
                Manage
            </span>
            <span class="material-icons icon">
                chevron_right
            </span>
            <span class="breadcrumb-text breadcrumb-main">
                Create New VM
            </span>
        </div>
        <div class="navbar-right">
            <span class="material-icons">
                account_circle
            </span>
            <span class="navbar-user-name">
                nqdrt1
            </span>
            <span class="material-icons">
                expand_more
            </span>
        </div>
    </nav>

    <div class="content">
        <span class="page-header">
            Create VM
            <divider></divider>
        </span>
        <div class="create-form">
            <form>
                <span class="form-header">
                    Choose an image:
                </span>
                <div class="create-form-select">
                    <VMSelect data={images}  />
                </div>
                <span class="form-header">
                    Choose a tier:
                </span>
                <div class="create-form-select">
                    <VMSelect isOS={false} data={tiers} />
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
                            <button class="batch-create-add" on:click={(e) => {e.preventDefault(); batch++; addHost(e)}}>
                                <span class="material-icons">
                                    add
                                </span>
                            </button>
                            <div class="batch-label"><b>{batch}</b>VM</div>
                            <button class="batch-create-remove" on:click={(e) => {e.preventDefault(); if (batch > 1) { batch--, removeHost(e)}}}>
                                <span class="material-icons">
                                    remove
                                </span>
                            </button>
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

    nav {
        margin-top: 25px;
        height: 50px;
        margin-bottom: 30px;
        display: flex;
        width: 100%;
        justify-content: space-between;
        color: #0e0d0d;
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

    .page-header {
        font-weight: bold;
        font-size: 30px;
        margin-left: 25px;
        display: flex;
        flex-direction: column;
    }

    divider {
        height: 1px;
        background-color:#0e0d0d;
        width: calc(100% - 25px);
        margin: 4px 0px;
    }

    .content {
        width: 100%;
        display: flex;
        flex-direction: column;
    }

    .breadcrumb {
        display: flex;
        flex-direction: row;
        font-size: 20px;
        align-items: center;
        margin-left: 25px;
    }

    .breadcrumb-text {
        padding-bottom: 4px;
    }

    .breadcrumb-main {
        font-weight: 500;
    }

    .navbar-right {
        display: flex;
        height: 100%;
        align-items: center;
        margin-right: 25px;
        cursor: pointer;
    }

    .navbar-user-name {
        padding: 0px 4px 4px;
    }

</style>

<!-- markup (zero or more items) goes here -->