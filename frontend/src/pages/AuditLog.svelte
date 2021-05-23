<script lang="ts">
  import AuditLogCard from '../components/AuditLogCard.svelte';
  import {location} from "svelte-spa-router";
  import { onMount } from 'svelte';
  import Spinner from '../components/Spinner.svelte';

  export let admin: boolean;
  export let params: any;

  let logs: Log[] = null;

  let isProjectLevel = $location.includes("project");

  const getLogs = async () => {
    fetch(`__apiRoute__/project/${params.project_id}/audit`)
    .then(res => res.json())
    .then(data => {
      if (data.meta.success) {
        logs = data.data;
      }
    })
    .catch(err => {
      console.error(err);
    })
  }

  onMount(() => {
    getLogs();
  })
</script>

<main>
  {#if logs == null}
    <div>
      <Spinner />
    </div>
  {:else}
  {#each logs as log}
    <AuditLogCard {log} {isProjectLevel} />
  {/each}
  {/if}
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    padding-left: 1rem;
  }

  div {
    margin: 2rem auto;
  }
</style>
