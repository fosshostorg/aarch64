<script lang="ts">
    export let vm: VM;

    let options: DropdownItem[] = [
        {label: "CONSOLE", icon: "airplay", action: e => {alert(`ssh ${vm.uuid}@${vm.host}.rescue.arm-64.com`)}},
        {label: 'SHUTDOWN', icon: 'power_settings_new', action: (e) => {}},
        {label: 'REBOOT', icon: 'refresh', action: (e) => {}},
        {label: 'STOP', icon: 'stop', action: (e) => {}},
        {label: 'RESET', icon: 'sync_problem', action: (e) => {}},
        {label: 'DELETE', icon: 'delete', action: (e) => {}}
    ]

</script>

<div class="action-options">
    <div class="action-title">
        ACTIONS
    </div>
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
    }

    span.action-option span {
        padding: 0px 4px;
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