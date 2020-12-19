<script>
    import VMSelect from '../components/VMSelect.svelte'

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



</script>

<main>
    <nav>
        <div class="breadcrumb">
            <span class="breadcrumb-text">
                Account
            </span>
            <span class="material-icons icon">
                chevron_right
            </span>
            <span class="breadcrumb-text">
                Dashboard
            </span>
            <span class="material-icons icon">
                chevron_right
            </span>
            <span class="breadcrumb-text breadcrumb-main">
                Create VM
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
                            <button class="batch-create-add" on:click={() => {batch++}}>
                                <span class="material-icons">
                                    add
                                </span>
                            </button>
                            <div class="batch-label"><b>{batch}</b> VM</div>
                            <button class="batch-create-remove" on:click={() => {batch > 1 ? batch-- : null}}>
                                <span class="material-icons">
                                    remove
                                </span>
                            </button>
                        </div>
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

    nav {
        margin-top: 25px;
        height: 50px;
        margin-bottom: 30px;
        display: flex;
        width: 100%;
        justify-content: space-between;
        color: #0e0d0d;
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
    }

    .create-form-final-section {
        display: flex;
        flex-direction: column;
    }

    .create-form-final {
        padding-left: 30px;
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