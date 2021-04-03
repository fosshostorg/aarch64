<script lang="ts">
  // @ts-nocheck
  import Navbar from "../components/Navbar.svelte";
  import PageHeader from "../components/PageHeader.svelte";
  import PageTitle from "../components/PageTitle.svelte";
  import Table from '../components/Table.svelte';
  import { link } from 'svelte-spa-router';
  import Input from "../components/Input.svelte";
  import Button from "../components/Button.svelte";
  import Select from "svelte-select";
  import { Projects, Snackbars } from '../stores';
  import { onMount } from "svelte";
import Spinner from "./Spinner.svelte";

  export let project;

  let headers = [
    {value: 'HOSTNAME', key: 'hostname'},
    {value: 'VM', key: 'vm'},
    {value: '', key: 'icon'}
  ]

  let rows = null;

  let hostname = "";
  let currentVM;
  let vms = [];

  function findVMName(id: string): string {
    for (const vm of project.vms) {
      if (vm._id === id) {
        return vm.hostname;
      }
    }
  }
  
  function getProxies() {
    fetch(`__apiRoute__/proxies/${project._id}` , {
			method: "GET"
		})
			.then(resp => resp.json())
			.then(data => {
				if (data.meta.success) {
						rows = [];
            rows = data.data.map(rec => {
              return {
                hostname: rec.label,
                vm: {hostname: findVMName(rec.vm), _id: rec.vm,},
                icon: 'delete_outline',
              }
            })
					} else {
						$Snackbars.push({
								color: "red",
								status: "ERROR",
								message: data.meta.message,
								grouped: true,        	
						})
						$Snackbars = $Snackbars;
					}
			})
			.catch((err) => alert(err));
  }

  $: if (project) {
    getProxies();
    vms = project.vms.map(vm => {
      return {
        value: vm,
        label: vm.hostname,
      }
    })
  }

  function addProxy() {
    console.log(JSON.stringify({vm: currentVM.value._id, label: hostname}));
		fetch("__apiRoute__/proxy", {
			method: "POST",
			headers: {"Content-Type": "application/json"},
			body: JSON.stringify({vm: currentVM.value._id, label: hostname})
		})
			.then(resp => resp.json())
			.then(data => {
				if (data.meta.success) {
						$Snackbars.push({
								color: "green",
								status: 200,
								message: data.meta.message,
								grouped: true,        	
						})
						$Snackbars = $Snackbars;
            getProxies();
					} else {
						$Snackbars.push({
								color: "red",
								status: "ERROR",
								message: data.meta.message,
								grouped: true,        	
						})
						$Snackbars = $Snackbars;
					}
			})
			.catch((err) => console.error(err));
	}

  onMount(() => {
    getProxies();
  })
</script>

<main>
  {#if rows == null}
  <span class="loading">
    <Spinner />
  </span>
  {:else}
  <div>
    <Table {headers} {rows} >
      <span class="cell-slot" slot="cell" let:row let:cell>
        {#if cell.key !== 'icon'}
        <span class="cell">
          {#if cell.key === 'vm'}
          {cell.value.hostname}
          <a class="material-icons vm-link" use:link href={`/dashboard/projects/${project._id}/resources/${cell.value._id}`} >
            open_in_new
          </a>
          {:else}
          {cell.value}
          {/if}
        </span>
        {:else}
        <span class="material-icons icon-cell">
          {cell.value}
        </span>
        {/if}
      </span>
    </Table>
  </div>
  <span class="form-header">Add a new proxy:</span>
  <span class="form-wrapper">
    <span class="form-inputs">
      <Input class="hostname-input" labelClasses="hostname-input-label" type="text" bind:value={hostname} placeholder="Hostname" />
      <span class="select-wrapper">
        <Select
          isClearable={false}
          isSearchable={false}
          items={vms}
          bind:selectedValue={currentVM}
          inputStyles="width: 100%;"
          placeholder="Choose VM"
        />
      </span>
    </span>
    <Button style="margin-top: 1rem;" on:click={() => addProxy()}>CREATE</Button>
  </span>
  {/if}

</main>


<style>
  main {
    width: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  div {
    margin-left: 2rem;
    margin-top: 1rem;
  }

  span.cell {
    display: inline-flex;
    justify-content: space-between;
    font-weight: 500;
    min-width: 300px;
    flex-grow: 1;
  }

  span.cell-slot {
    display: flex;
    width: auto;
  }

  span.icon-cell {
    padding-top: 4px;
    cursor: pointer;
  }

  a.vm-link {
    text-decoration: none;
    color: #0e0d0d;
    font-size: 20px;
    padding-left: 1rem;
  }

  .form-header {
		font-weight: 500;
		opacity: 0.7;
		font-size: 28px;
		padding-left: 25px;
		height: 55px;
		display: flex;
		align-items: center;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
	}

  .form-wrapper {
		width: auto;
		margin-left: 2rem;
	}

  span :global(.hostname-input) {
    width: 308px;
  }

  span :global(.hostname-input-label) {
    width: 325px;
  }

  span.form-inputs {
    display: flex;
    max-width: 700px;
  }

  span.select-wrapper {
		--border: 1px solid #0e0d0d;
		--borderHoverColor: 1px solid #0e0d0d;
		--borderFocusColor: 1px solid #0e0d0d;
		--borderRadius: 0px;
		--height: 38px;
		/* width: auto; */
		--padding: 5px 0px;
		--inputPadding: 0.75rem;
		--listBorderRadius: 0px;
		--itemFirstBorderRadius: 0px;
		--itemIsActiveBG: #0e0d0d;
		--itemHoverBG: #0e0d0d15;
    --placeholderColor: #0e0d0d;
		display: flex;
		flex-direction: column;
    margin-left: -1px;
    flex-grow: 1;
	}

  .loading {
    margin: 4rem auto;
  }
</style>