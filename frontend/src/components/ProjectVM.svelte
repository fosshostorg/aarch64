<script lang="ts">
    /*globals VM */
    import { push } from 'svelte-spa-router';
    import Dropdown from './Dropdown.svelte';
    import { dropdownItems } from '../utils';

    export let VM: VM = {
        _id: '',
        hostname: '',
        pop: '',
        project: '',
        prefix: '',
        os: '',
        host: 0,
        vcpus: 0,
        memory: 0,
        ssd: 0,
        password: '',
        phoned_home: false,
        address: '',
        gateway: '',
        creator: '',
        state: 0,
        created: { by: '', at: 0 }
    };

    export let link = '';

    let listOpen = false;

    const handleSettings = () => {
        listOpen = !listOpen;
    };
</script>

<main>
    <span
        class="wrapper"
        on:click={() => {
            void push(link);
        }}
    >
        <span class="img">
            <img src={'./img/' + VM.os.toLowerCase() + '.svg'} alt={VM.os + ' Logo'} />
            <span class="status" class:online={VM.state == 1} />
        </span>
        <div class="hostname">{VM.hostname}</div>
        <div class="location">
            {VM.pop.toUpperCase()}{VM.host}
        </div>
        <span class="ip">
            {VM.address}
        </span>
    </span>
    <button class="material-icons icon" on:click={handleSettings}>
        <span class="dropdown">
            <Dropdown bind:open={listOpen} items={dropdownItems(VM)} />
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
        font-family: Roboto, -apple-system, BlinkMacSystemFont, 'Segoe UI', Oxygen, Ubuntu,
            Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }

    span.wrapper {
        width: calc(100% - 40px);
        display: flex;
        align-items: center;
        cursor: pointer;
        min-height: 40px;
    }

    div.hostname {
        /* flex-grow: 1; */
        padding-left: 15px;
        flex-basis: 385px;
        /* flex-shrink: 0; */
        font-size: 18px;
        font-weight: 500;
    }

    div.location {
        flex-grow: 1;
        display: flex;
        justify-content: center;
        flex-basis: 0px;
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
        background-color: #aa1717;
        right: -4px;
        bottom: 5px;
        z-index: 5;
    }

    span.status.online {
        background-color: #74aa17;
    }

    span.ip {
        display: flex;
        /* width: calc(50% - 40px); */
        padding-left: 0px;
        align-items: center;
        justify-content: center;
        flex-grow: 1;
        flex-basis: 270px;
    }

    img {
        height: 30px;
        filter: invert(1);
        position: absolute;
        top: 5px;
        left: 5px;
    }
</style>
