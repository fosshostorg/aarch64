<script>

</script>

<main>
    <nav>
        <img class="logo" src="./img/ARM-64.png" alt="ARM-64 Logo" />
        <divider></divider>
        <ul class="sidebar-categories">
            <li class="sidebar-category">
                <span class="sidebar-category-header">PROJECTS</span>
                <ul class="sidebar-category-items">
                    <li class="sidebar-category-item">vela's Project</li>
                    <li class="sidebar-category-item">nqdrt1's Long Project Name</li>
                </ul>
            </li>
            <divider></divider>
            <li class="sidebar-category">
                <span class="sidebar-category-header">PROJECTS</span>
                <ul class="sidebar-category-items">
                    <li class="sidebar-category-item"></li>
                </ul>
            </li>
            <divider></divider>
            <li class="sidebar-category">
                <span class="sidebar-category-header">PROJECTS</span>
                <ul class="sidebar-category-items">
                    <li class="sidebar-category-item"></li>
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
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        padding: 0px;
        margin: 0px;
        margin-left: 7px;
        margin-top: 15px;
    }

    .sidebar-category-items {
        font-size: 18px;
        width: 100%;
        margin: 0px;
        padding: 0px;
        padding-left: 25px;
    }

    .sidebar-category-item {
        max-width: calc(100% - 25px);
        min-width: 0;
        height: 40px;
        margin: 0px;
        padding: 0px;
        display: flex;
        align-items: center; 
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

</style>
