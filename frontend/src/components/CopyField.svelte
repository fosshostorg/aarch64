<script lang="ts">
    import Input from './Input.svelte';
    import {Snackbars} from '../stores';

    export let text: string = "";
    export let label: string = "Password";

    function copyHandler() {
        console.log('done')
        navigator.clipboard.writeText(text).then(function() {
            $Snackbars.push({
				color: "green",
				status: "OK",
				message: "copied",
				grouped: true,
			})
            $Snackbars = $Snackbars;
        }, function(err) {
            $Snackbars.push({
				color: "red",
				status: "ERROR",
				message: "copy failed",
				grouped: true,
			})
            $Snackbars = $Snackbars;
        });
        // alert("Password has been copied to clipboard")
    }
</script>

<main>
    <label for="text-input">{label}:</label>
    <div>
        <Input type="text" value={text} id="text-input" class="input-field" disabled />
        <button on:click={copyHandler}>COPY</button>
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

    button {
        height: 100%;
        border: none;
        color: white;
        background-color: #0e0d0d;
        font-size: 15px;
        font-weight: 500;
        font-family: inherit;
        cursor: pointer;
    }
</style>
