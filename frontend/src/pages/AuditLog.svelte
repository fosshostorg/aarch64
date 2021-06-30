<script lang="ts">
    import AuditLogCard from '../components/AuditLogCard.svelte'
    import { location, push } from 'svelte-spa-router'
    import { onMount } from 'svelte'
    import Spinner from '../components/Spinner.svelte'
    import PageHeader from '../components/PageHeader.svelte'
    import Navbar from '../components/Navbar.svelte'
    import { User } from '../stores'

    export let admin: boolean
    export let params: any

    let logs: Log[] = null
    let isProjectLevel = $location.includes('project')

    const getLogs = async () => {
        const route = admin ? `/admin/audit` : `/project/${params.project_id}/audit`
        fetch(`__apiRoute__${route}`)
            .then(res => res.json())
            .then(data => {
                if (data.meta.success) {
                    logs = data.data
                }
            })
            .catch(err => {
                console.error(err)
            })
    }

    onMount(() => {
        // @ts-ignore
        if (admin && !$User.admin) {
            push('/dashboard')
        } else {
            getLogs()
        }
    })
</script>

{#if admin}
    <Navbar
        breadcrumbs={[
            { label: 'Dashboard', path: '/dashboard' },
            { label: 'Audit Log', path: `/dashboard/auditlog` }
        ]}
    />
    <PageHeader>Global Audit Log</PageHeader>
{/if}
<main>
    {#if logs == null}
        <div>
            <Spinner />
        </div>
    {:else}
        {#each logs as log}
            <AuditLogCard {log} />
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
