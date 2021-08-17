<script lang="ts">
    export let id = '';
    export let group = '';
    export let disabled = false;
</script>

<label class="container" on:click>
    <input type="radio" value={id} bind:group on:change {disabled} />
    <slot />
</label>

<style>
    label {
        display: flex;
    }

    .container input {
        opacity: 0;
        cursor: default;
        position: absolute;
    }
</style>
