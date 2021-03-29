<script lang="ts">
    import {push} from "svelte-spa-router";

    export let text: string = "";

    function copyHandler() {
        let copyText = document.getElementById("text-input");
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        document.execCommand("copy");
        // alert("Password has been copied to clipboard")
    }
</script>

<main>
    <label for="text-input">Password: &nbsp;<span class="material-icons" on:click={() => push("/docs")}>help_outline</span></label>
    <div>
        <input type="text" value="{text}" id="text-input">
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

    input {
        border: 1px solid #0e0d0d;
        height: 100%;
        color: #0e0d0d;
        padding: 0 0 0 10px;
        font-size: 18px;
        box-sizing: border-box;
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
    }
</style>
