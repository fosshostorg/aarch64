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
                    Choose an Image:
                </span>
                <div class="create-form-select">
                    <VMSelect data={images}  />
                </div>
                <span class="form-header">
                    Choose a Tier:
                </span>
                <div class="create-form-select">
                    <VMSelect isOS={false} data={tiers} />
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