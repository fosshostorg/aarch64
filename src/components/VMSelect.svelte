<script>
    import RadioButton from './RadioButton.svelte';
    export let isOS = true;

    export let data = [];

    let current = data[0].title;
</script>

<main>
    {#each data as option}
    <RadioButton id={option.title} bind:group={current}>
        <div class="selection-card" class:selected={current == option.title}>
            {#if isOS}
            <img src={option.img} alt={option.title + ' Logo'} />
            {/if}
            <span class="selection-card-header">
                {option.title}
            </span>
            <divider></divider>
            {#if isOS}
            <span class="selection-card-text">
                {option.version}
            </span>
            {:else}
            <span class="selection-card-details">
                <span class="vCPU">
                    <b>{option.vCPU}</b> vCPU
                </span>
                <span class="RAM">
                    <b>{option.RAM}</b> RAM
                </span>
                <span class="SSD">
                    <b>{option.SSD}</b> SSD
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
        width: 123px;
        height: 123px;
        border: 1px solid #0e0d0d;
        background-color: #0e0d0d;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        margin-left: 15px;
        cursor: pointer;
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
        font-size: 22px;
    }

    .selected .selection-card-header  {
        color: #0e0d0d;
    }

    .selection-card-text {
        font-size: 18px;
        color: white;
        opacity: .6;
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
        margin-left: -1px;
    }

    .selected divider {
        background-color: #0e0d0d;
    }
</style>

