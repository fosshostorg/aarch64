<script>
    import {onMount} from "svelte";
    import {User} from '../stores'

    export let breadcrumbs = [];

    $: console.log($User)

    function logOut() {
        const res = fetch('__apiRoute__/user/logout', {
            method: 'GET',
            headers: {'Content-Type': 'application/json'}
        })
            .then(res => res.json())
            .then(data => {
                if (data.meta.success) {
                    window.location.href = "/#/"
                }
            })
            .catch(err => console.log(err))
    }
</script>

<nav>
    <div class="breadcrumb">
        {#each breadcrumbs as breadcrumb, index}
        <span class="breadcrumb-text" class:breadcrumb-main={index == breadcrumbs.length - 1}>
            {breadcrumb}
        </span>
            {#if index !== breadcrumbs.length - 1}
            <span class="material-icons icon">
                chevron_right
            </span>
            {/if}
        {/each}
    </div>
    <div class="navbar-right">
        <span class="material-icons">account_circle</span>
        <span class="navbar-user-name">{$User['email']}</span>
        <span class="material-icons">expand_more</span>
        <!-- TODO: Dropdown here with a logout button that calls userLogout() -->
    </div>
</nav>

<style>
    nav {
        margin-top: 25px;
        height: 50px;
        margin-bottom: 30px;
        display: flex;
        width: 100%;
        justify-content: space-between;
        color: #0e0d0d;
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

