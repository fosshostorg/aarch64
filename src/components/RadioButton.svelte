<script>
    export let id = '';
    export let group = '';

</script>

<label class="container" on:click>
    <input type="radio" value={id} bind:group={group}>
    <slot></slot>
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