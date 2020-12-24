<script lang="ts">
    export let options: boolean = false;
    export let current: string = '';
    export let labels: string[] = [];
</script>

<span>
    <div class="header">
        <slot />
        {#if options}
        <div class="button-wrapper">
            {#each labels as label}
            <button class:current={current == label} on:click={() => {current = label}}>{label}</button>
            {/each}
        </div>
        {/if}
    </div>
    <divider></divider>
</span>

<style>
    span {
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
        margin: 0px 0px 4px;
    }

    button {
        border: none;
        background-color: transparent;
        font-family: inherit;
        font-weight: 500;
        font-size: 16px;
        height: 30px;
        margin: 0px;
        margin-bottom: -5px;
        cursor: pointer;
    }

    button.current {
        border-bottom: 5px solid #0e0d0d;
    }

    button:active {
        padding: 0px 8px;
    }

    div.header {
        display: flex;
        width: calc(100% - 25px);
        align-items: flex-end;
        justify-content: space-between;
    }

</style>