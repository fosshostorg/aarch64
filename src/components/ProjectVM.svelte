<script lang="ts">
    import {push} from 'svelte-spa-router';
    import Dropdown from './Dropdown.svelte';

    export let VM: VM = {
        hostname: '',
        os: '',
        ipv4: '',
        ipv6: '',
        online: false,
    }

    export let link: string = '';

    let dropdownItems: DropdownItem[] = [
        {label: 'SHUTDOWN', icon: 'power_settings_new', action: (e) => {}},
        {label: 'REBOOT', icon: 'refresh', action: (e) => {}},
        {label: 'STOP', icon: 'stop', action: (e) => {}},
        {label: 'RESET', icon: 'sync_problem', action: (e) => {}}
    ]

    let listOpen = false;

    const handleSettings = (e) => {
        listOpen = !listOpen;
    }

</script>

<main>
    <span class="wrapper" on:click={() => {push(link)}}>
        <span class="img">
            <img src={'./img/' + VM.os.toLowerCase() + '.svg'} alt={VM.os + ' Logo'} />
            <span class="status" class:online={VM.online}></span>
        </span>
        <div>
            {VM.hostname}
        </div>
        <span class="ip">
            <b>v4:</b> {VM.ipv4} | <b>v6:</b> {VM.ipv6}
        </span>
    </span>
    <button class="material-icons icon" on:click={handleSettings}>
        <span class="dropdown">
            <Dropdown bind:open={listOpen} items={dropdownItems}/>
        </span>
        more_horiz
    </button>
    
</main>

<style>
    main {
        border: 1px solid #0e0d0d;
        min-height: 40px;
        width: calc(100% - 30px);
        margin: 10px 15px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        cursor: pointer;
    }

    span.dropdown {
        font-family: Roboto, -apple-system, BlinkMacSystemFont, 'Segoe UI', Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }

    span.wrapper {
        width: calc(100% - 40px);
        display: flex;
        align-items: center;
        cursor: pointer;
        min-height: 40px;
    }

    div {
        flex-grow: 1;
        padding-left: 15px;
        font-weight: 500;
        font-size: 20px;
        flex-shrink: 0;
    }

    button.icon {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        cursor: pointer;
        border: none;
        padding: 0px;
        margin: 0px;
        background-color: white;
        flex-shrink: 0;
    }

    button.icon:active {
        padding: 0px;
    }

    span.img {
        height: 40px;
        width: 40px;
        background-color: #0e0d0d;
        position: relative;
    }

    span.status {
        height: 14px;
        width: 14px;
        position: absolute;
        background-color: #AA1717;
        right: -4px;
        bottom: 5px;
        z-index: 5;
    }

    span.status.online {
        background-color: #74AA17;
    }

    span.ip {
        display: flex;
        width: calc(50% - 40px);
        padding-left: 0px;
        align-items: center;
        justify-content: flex-start;
    }

    .ip b {
        font-weight: bold;
    }

    img {
        height: 30px;
        filter: invert(1);
        position: absolute;
        top: 5px;
        left: 5px;
    }
</style>