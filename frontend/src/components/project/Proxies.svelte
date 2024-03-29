<script lang="ts">
    /*global Project, VM , ProxyItem, APIResponse */
    import Table from '../Table.svelte';
    import { link } from 'svelte-spa-router';
    import Input from '../Input.svelte';
    import Button from '../Button.svelte';
    import Select from 'svelte-select';
    import Spinner from '../Spinner.svelte';
    import { checkMeta } from '../../utils';

    /* The project we are currently viewing */
    export let project: Project = null;

    /* Table headers */
    let headers = [
        { value: 'HOSTNAME', key: 'hostname' },
        { value: 'VM', key: 'vm' },
        { value: '', key: 'icon' }
    ];

    /* The proxies to show in the table */
    let proxies: ProxyItem[] = null;

    /* The hostname and VM to add from the new proxy form */
    let hostname = '';
    let currentVM = null;

    /* Sets the VMs of our project for the dropdown */
    let vms = setVMS(project);

    /* Gets the VMs of a project for the dropdown options */
    function setVMS(project: Project): { value: VM; label: string }[] {
        getProxies();
        currentVM = null;
        return project.vms.map(vm => {
            return {
                value: vm,
                label: vm.hostname
            };
        });
    }

    /* Gets the name of a VM from a VM object, for use in the dropdown */
    function findVMName(id: string): string {
        for (const vm of project.vms) {
            if (vm._id === id) {
                return vm.hostname;
            }
        }
        return '';
    }

    /* Gets the project's proxies (as they are not returned in the larger project object) */
    function getProxies() {
        fetch(`__apiRoute__/proxies/${project._id}`, {
            method: 'GET'
        })
            .then(resp => resp.json())
            .then((data: APIResponse<Proxy[]>) => {
                if (data.meta.success) {
                    proxies = [];
                    proxies = data.data.map(rec => {
                        return {
                            hostname: rec.label,
                            vm: { hostname: findVMName(rec.vm), _id: rec.vm },
                            icon: {
                                value: 'delete_outline',
                                id: rec._id
                            }
                        };
                    });
                } else {
                    checkMeta(data);
                }
            })
            .catch(err => alert(err));
    }

    /* Adds a new proxy */
    function addProxy() {
        fetch('__apiRoute__/proxy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ vm: currentVM.value._id, label: hostname })
        })
            .then(resp => resp.json())
            .then(data => {
                if (checkMeta(data)) {
                    getProxies();
                }
            })
            .catch(err => alert(err));
    }

    /* Deletes a given proxy */
    function deleteProxy(proxy_id: string) {
        fetch('__apiRoute__/proxy', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ proxy: proxy_id })
        })
            .then(resp => resp.json())
            .then(data => {
                if (checkMeta(data)) {
                    getProxies();
                }
            })
            .catch(err => alert(err));
    }
</script>

<main>
    {#if proxies == null}
        <span class="loading">
            <Spinner />
        </span>
    {:else}
        {#if proxies.length > 0}
            <div>
                <Table {headers} rows={proxies}>
                    <span class="cell-slot" slot="cell" let:row let:cell>
                        {#if cell.key !== 'icon'}
                            <span class="cell">
                                {#if cell.key === 'vm'}
                                    {cell.value.hostname}
                                    <a
                                        class="material-icons vm-link"
                                        use:link
                                        href={`/dashboard/projects/${project._id}/resources/${cell.value._id}`}
                                    >
                                        open_in_new
                                    </a>
                                {:else}
                                    {cell.value}
                                {/if}
                            </span>
                        {:else}
                            <span
                                class="material-icons icon-cell"
                                on:click={() => deleteProxy(cell.value.id)}
                            >
                                {cell.value.value}
                            </span>
                        {/if}
                    </span>
                </Table>
            </div>
        {/if}
        <span class="form-header">Add a new proxy:</span>
        <span class="form-wrapper">
            <span class="form-inputs">
                <Input
                    class="hostname-input"
                    labelClasses="hostname-input-label"
                    type="text"
                    bind:value={hostname}
                    placeholder="Hostname"
                />
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
