<script>
    let projects = [{name: "vela's Project"}, {name: "nqdrt1's Long Project Name"}]
</script>

<main>
    <nav>
        <img class="logo" src="./img/ARM-64.png" alt="ARM-64 Logo" />
        <divider></divider>
        <ul class="sidebar-categories">
            <li class="sidebar-category">
                <span class="sidebar-category-header">
                    PROJECTS
                    <span class="material-icons dropdown">
                        expand_more
                    </span>
                </span>
                <ul class="sidebar-category-items">
                    {#each projects as project}
                    <li class="sidebar-category-item">
                        <a href="#">
                            {project.name}
                        </a>
                    </li>
                    {/each}
                </ul>
            </li>
            <divider></divider>
            <li class="sidebar-category">
                <span class="sidebar-category-header">
                    MANAGE
                    <span class="material-icons dropdown">
                        expand_more
                    </span>
                </span>
                <ul class="sidebar-category-items">
                    <li class="sidebar-category-item">
                        <a href="#">
                            Virtual Machines
                        </a>
                    </li>
                    <li class="sidebar-category-item">
                        <a href="#">
                            Create New VM
                        </a>
                    </li>
                </ul>
            </li>
            <divider></divider>
            <li class="sidebar-category">
                <span class="sidebar-category-header">
                    ACCOUNT
                    <span class="material-icons dropdown">
                        expand_more
                    </span>
                </span>
                <ul class="sidebar-category-items">
                    <li class="sidebar-category-item">
                        <a href="#">
                            Settings
                        </a>
                    </li>
                    <li class="sidebar-category-item">
                        <a href="#">
                            API
                        </a>
                    </li>
                    <li class="sidebar-category-item">
                        <a href="#">
                            Support
                        </a>
                    </li>
                </ul>
            </li>
        </ul>
    </nav>


</main>

<style>
    main {
        width: 100%;
        min-height: 100vh;
        --sidebar-width: 250px;
    }

    nav {
        background-color: #0E0D0D;
        width: var(--sidebar-width);
        height: 100vh;
        position: sticky;
        top: 0;
        left: 0;
        display: flex;
        flex-flow: column nowrap;
        align-items: center;
    }

    .logo {
        width: calc(var(--sidebar-width) - 100px);
        margin: 25px 0px;
    }

    divider {
        display: block;
        width: calc(var(--sidebar-width) - 50px);
        height: 1px;
        background-color: white;
        opacity: .3;
    }

    li, ul {
        list-style-type: none;
    }

    .sidebar-categories {
        width: calc(var(--sidebar-width) - 50px);
        height: auto;
        color: white;
        margin: 0px;
        padding: 0px;
    }

    .sidebar-category {
        display: flex;
        flex-direction: column;
        margin-bottom: 20px;
    }

    .sidebar-category-header {
        width: auto;
        font-size: 20px;
        font-weight: bold;
        padding: 0px;
        margin: 0px;
        margin-left: 7px;
        margin-top: 15px;
        padding-bottom: 5px;
    }

    .sidebar-category-items {
        font-size: 18px;
        width: 100%;
        margin: 0px;
        padding: 0px;
        padding-left: 25px;
    }

    .sidebar-category-item {
        width: calc(100% - 25px);
        height: 40px;
        margin: 0px;
        padding: 0px;
        display: flex;
        align-items: center; 
    }

    .sidebar-category-item a {
        color: white;
        text-decoration: none;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
    }

    .sidebar-category-item:hover::before {
        content: " ";
        width: var(--sidebar-width);
        height: 40px;
        background-color: white;
        opacity: .25;
        display: block;
        position: absolute;
        left: 0;
    }

    .dropdown {
        float: right;
    }

    .rotate {
        transform: rotate(-90deg);
    }

</style>
