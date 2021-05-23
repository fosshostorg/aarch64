<script lang="ts">
  export let log: Log;
  export let isProjectLevel: boolean;

  let time = new Date(log.time);
  let parts = time.toLocaleString("en-US");
  let timeString = parts.split(',').join(' at ');
</script>

<div>
  <span>
    <p class="action"><b>ACTION</b>: {log.title}</p>
    <p class="time">{timeString}</p>
  </span>
  <p><b>USER</b>: {log.user_email}</p>
  {#if !isProjectLevel}
    <p><b>PROJECT</b>: {log.project_name}</p>
  {/if}
  <p><b>DETAILS</b>: {JSON.stringify(log.detail)}</p>
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
