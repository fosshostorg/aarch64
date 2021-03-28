<script lang="ts">
    import {replace} from "svelte-spa-router";

    export let text: string = "";

    function copyHandler() {
        let copyText = document.getElementById("text-input");
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        document.execCommand("copy");
        alert("Temporary password has been copied to clipboard")
    }
</script>

<main>
    <label for="text-input">Temporary Password: &nbsp;<span class="material-icons" on:click={() => replace("/docs/quickstart")}>help_outline</span></label>
    <div>
        <input type="text" value="{text}" id="text-input">
        <button on:click={copyHandler}>Copy</button>
    </div>
</main>

<style>
    div {
        display: flex;
        flex-direction: row;
        align-items: baseline;
    }

    label {
        font-weight: 500;
        margin: 10px 0;
        display: flex;
        align-items: center;
    }

    input {
        border: 1px solid #0e0d0d;
        height: 40px;
        color: #0e0d0d;
        padding: 0 0 0 10px;
        font-size: 18px;
        margin: 0 0 18px 0;
    }

    button {
        height: 40px;
        border: none;
        color: white;
        background-color: #0e0d0d;
        font-size: 15px;
        font-weight: 500;
        font-family: inherit;
        margin: 0;
    }
</style>
