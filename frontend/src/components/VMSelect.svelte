<script lang="ts">
    /*globals OS, Plan */
    import RadioButton from './RadioButton.svelte';

    export let planOptions: { [key: string]: Plan } = {};
    export let osOptions: { [key: string]: OS } = {};
    export let current = '';
    export let coreLimit = 0;
    
    $: isOS = Object.keys(osOptions).length !== 0;
</script>

<main>
    {#each Object.keys(isOS ? osOptions : planOptions) as option, i}
        <RadioButton id={option} bind:group={current} on:change disabled={!isOS && planOptions[option].vcpus > coreLimit}>
            <div class="selection-card" class:selected={current == option} class:disabled={!isOS && planOptions[option].vcpus > coreLimit}>
                {#if isOS}
                    <img src={`./img/${osOptions[option].image}`} alt={`${option} Logo`} />
                {/if}
                {#if isOS}
                <span class="selection-card-header"> {osOptions[option].class} </span>
                {:else}
                <span class="selection-card-header"> {option} </span>
                {/if}
                <divider />
                {#if isOS}
                    <span class="selection-card-text">
                        {osOptions[option].version}
                    </span>
                {:else}
                    <span class="selection-card-details">
                        <span class="vCPU">
                            <b>{planOptions[option].vcpus}</b>
                            vCPU
                        </span>
                        <span class="RAM">
                            <b>{planOptions[option].memory}GB</b>
                            RAM
                        </span>
                        <span class="SSD">
                            <b>{planOptions[option].ssd}GB</b>
                            SSD
                        </span>
                    </span>
                {/if}
            </div>
        </RadioButton>
    {/each}
</main>

<style>
    main {
        display: flex;
    }

    .selection-card {
        width: 125px;
        height: 125px;
        border: 1px solid #0e0d0d;
        background-color: #0e0d0d;
        display: flex;
        flex-shrink: 0;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        margin-left: 15px;
        cursor: pointer;
        box-sizing: border-box;
    }

    .selection-card.selected {
        background-color: white;
    }

    img {
        padding-top: 6px;
        width: 48px;
        filter: invert(1);
    }

    .selected img {
        filter: none;
    }

    .selection-card-header {
        color: white;
        font-weight: 500;
        font-size: 17px;
        padding-top: 5px;
    }

    .selected .selection-card-header {
        color: #0e0d0d;
    }

    .selection-card-text {
        font-size: 18px;
        color: white;
        opacity: 0.6;
    }

    .selected .selection-card-text {
        color: #0e0d0d;
    }

    .selection-card-details {
        font-size: 18px;
        font-weight: 300;
        color: white;
        display: flex;
        flex-direction: column;
        padding: 8px 0px;
    }

    .selected .selection-card-details {
        color: #0e0d0d;
    }

    .selection-card-details b {
        font-weight: bold;
    }

    divider {
        width: 125px;
        height: 1px;
        background-color: white;
    }

    .selected divider {
        background-color: #0e0d0d;
    }

    .disabled {
        color: #0e0d0d !important;
        background-color: #cecece !important;
        border-color: #b1b1b1 !important;
        cursor: default;
    }

    .disabled .selection-card-details, .disabled .selection-card-header {
        color: #838383 !important;
    }

    .disabled divider {
        background-color: #838383 !important;
    }
</style>
