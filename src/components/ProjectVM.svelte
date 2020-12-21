<script>
    import {push} from 'svelte-spa-router';


    export let os = '';
    export let name = '';
    export let ip = '';
    export let online = false;
    export let link = '';

</script>

<main on:click={() => {push(link)}}>
    <span class="img">
        <img src={'./img/' + os.toLowerCase() + '.svg'} alt={os + ' Logo'} />
        <span class="status" class:online></span>
    </span>
    <div>
        {name}
    </div>
    <span class="ip">
        {ip}
    </span>
    <button class="material-icons icon">
        more_horiz
    </button>
</main>

<style>
    main {
        border: 1px solid #0e0d0d;
        height: 40px;
        width: calc(100% - 30px);
        margin: 10px 15px;
        display: flex;
        flex-wrap: nowrap;
        align-items: center;
        cursor: pointer;
    }

    div {
        flex-grow: 1;
        padding-left: 15px;
        font-weight: 500;
        font-size: 20px;
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
        flex-grow: 1;
        align-items: center;
        justify-content: flex-start;
    }

    img {
        height: 30px;
        filter: invert(1);
        position: absolute;
        top: 5px;
        left: 5px;
    }
</style>