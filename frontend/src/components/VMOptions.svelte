<script lang="ts">
    /*globals VM */
    import { dropdownItems } from '../utils';

    export let vm: VM;

    let options = dropdownItems(vm);
</script>

<div class="action-options">
    <div class="action-title">ACTIONS</div>
    {#each options as option}
        <span class="action-option" on:click={option.action}>
            <span class="material-icons">{option.icon}</span>
            {option.label}
        </span>
    {/each}
</div>

<style>
    div.action-options {
        display: flex;
        flex-direction: column;
        margin-left: 15px;
    }

    div.action-options span.action-option {
        height: 35px;
        border: 1px solid #0e0d0d;
        border-top: none;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        font-weight: 500;
        padding: 0px 8px 0px 4px;
        cursor: pointer;
    }

    span.action-option span {
        padding: 0px 4px;
    }

    span.action-option:hover {
        background-color: #0e0d0d15;
    }

    div.action-title {
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        background-color: #0e0d0d;
    }
</style>
