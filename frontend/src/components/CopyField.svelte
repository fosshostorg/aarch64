<script lang="ts">
    import Input from './Input.svelte';
    import { Snackbars } from '../stores';
    import Button from './Button.svelte';

    export let text = '';
    export let label = 'Password';

    function copyHandler() {
        console.log('done');
        navigator.clipboard.writeText(text).then(
            function () {
                $Snackbars.push({
                    color: 'green',
                    status: 'OK',
                    message: 'copied',
                    grouped: true
                });
                $Snackbars = $Snackbars;
            },
            function (err) {
                $Snackbars.push({
                    color: 'red',
                    status: 'ERROR',
                    message: 'copy failed',
                    grouped: true
                });
                $Snackbars = $Snackbars;
            }
        );
    }
</script>

<main>
    <label for="text-input">{label}:</label>
    <div>
        <Input type="text" value={text} id="text-input" class="input-field" disabled />
        <Button class="copy-button" on:click={copyHandler}>COPY</Button>
    </div>
</main>

<style>
    main {
        margin-top: 1.5rem;
    }

    div {
        display: flex;
        flex-direction: row;
        align-items: center;
        height: 40px;
        width: 100%;
    }

    label {
        font-weight: 500;
        margin: 10px 0;
        display: flex;
        align-items: center;
        opacity: 0.7;
    }

    div :global(.input-field) {
        flex-grow: 1;
    }

    div :global(.copy-button) {
        height: 38px;
        color: white;
        font-size: 15px;
        font-weight: 500;
        font-family: inherit;
        cursor: pointer;
    }
</style>
