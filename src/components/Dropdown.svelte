<script>
    let items = {
        "POWER OFF": {icon: 'power_settings_new'},
        "REBOOT": {icon: 'refresh'},
        "DELETE": {icon: 'delete'}
    }

    // let selected = dropdown[0];
    export let open = false;

    const handleFocusout = (e) => {
        if (open) {
            if (e.relatedTarget !== null && e.relatedTarget.id !== '') {
                if (e.relatedTarget.id !== "dropdown") {
                    open = false;
                }
            } else {
                open = false;
            }
        }
    }

    addEventListener('focusout', handleFocusout);

</script>

<main on:>
    {#if open}
    <div tabindex="-1">
    {#each Object.keys(items) as item}
        <button id="dropdown">
            <span class="material-icons">
                {items[item].icon}
            </span>
            {item}
        </button>
    {/each}
    </div>
    {/if}
</main>

<style>
    main {
        height: 0px;
        width: 0px;
        position: relative;
        font-family: inherit;
    }

    div {
        height: auto;
        width: auto;
        background-color: white;
        box-shadow: 5px 5px 5px #ccc;
        position: absolute;
        right: 0;
        top: 0;
        display: flex;
        flex-direction: column;
        font-family: inherit;
        border: 1px solid #0e0d0d;
    }

    div :not(:last-child) {
        /* border-top: 1px solid #0e0d0d; */
        border-bottom: 1px solid #0e0d0d;
    }

    button {
        width: auto;
        font-size: 14px;
        font-weight: 500;
        font-family: inherit;
        display: flex;
        align-items: center;
        padding: 5px 7px;
        margin: 0px;
        background-color: white;
        border: none;
        color: black;
        cursor: pointer;
    }

    button:hover {
        background-color: #0e0d0d15;
    }

    button span {
        margin-right: 8px;
    }

</style>