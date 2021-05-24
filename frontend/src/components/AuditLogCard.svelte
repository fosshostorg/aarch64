<script lang="ts">
    export let log: Log;

    let time = new Date(log.time * 1000);
    let parts = time.toLocaleString("en-US");
    let timeString = parts.split(',').join(' at ');

</script>

<div>
  <span>
    <p class="action"><b>ACTION</b>: {log.title}</p>
    <p class="time">{timeString}</p>
  </span>
    {#if !(log.user_name === "" || log.user_name === undefined)}
        <p><b>USER</b>: {log.user_name}</p>
    {/if}
    {#if !(log.project_name === "" || log.project_name === undefined)}
        <p><b>PROJECT</b>: <a href="https://console.aarch64.com/#/dashboard/projects/{log.project_id}">{log.project_name}</a></p>
    {/if}
    {#if !(log.vm_name === "" || log.vm_name === undefined)}
        <p><b>VM</b>: <a href="https://console.aarch64.com/#/dashboard/projects/{log.project_id}/resources/{log.vm_id}">{log.vm_name}</a></p>
    {/if}
    {#if !(log.proxy_name === "" || log.proxy_name === undefined)}
        <p><b>PROXY</b>: {log.proxy_name}</p>
    {/if}
</div>

<style>
    div {
        width: 100%;
        max-width: 800px;
        border: 1px solid black;
        padding: 0.5rem 1rem;
        margin: 1rem auto 0rem;
    }

    p {
        margin: 0px;
    }

    span {
        display: flex;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #ccc;
        margin-bottom: 0.5rem;
        width: 100%;
        justify-content: space-between;
    }

    p.time {

    }
</style>
