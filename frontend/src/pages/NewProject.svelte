<script>
    import PageHeader from '../components/PageHeader.svelte'
    import Navbar from '../components/Navbar.svelte'
    import { push } from 'svelte-spa-router'
    import { Projects } from '../stores'
    import PageTitle from '../components/PageTitle.svelte'
    import Input from '../components/Input.svelte'

    let name = ''
    let budget = 2

    const handleSubmit = async e => {
        if (__production__) {
            await fetch('__apiRoute__/project', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, budget })
            })
                .then(resp => resp.json())
                .then(data => {
                    if (data.meta.success) {
                        push('/dashboard/projects/' + data.data)
                    } else {
                        alert(data.meta.message)
                    }
                })
                .catch(err => console.log(err))
        } else {
            console.log(
                '%cRequest would have been sent with name: ' + name,
                'color: lightgreen'
            )
        }
    }
</script>

<PageTitle title="New Project" />

<main>
    <Navbar
        breadcrumbs={[
            { label: 'Dashboard', path: '/dashboard/projects/create' },
            { label: 'Add New Project', path: '/dashboard/projects/create' }
        ]}
    />
    <PageHeader>Add New Project</PageHeader>
    <div class="content">
        <form on:submit|preventDefault={handleSubmit}>
            <Input
                label="Project name:"
                labelClasses="name-label"
                class="name-input"
                autocomplete="off"
                bind:value={name}
                name="name"
                placeholder="Name..."
                type="text"
            />
            <Input
                label="Project core budget:"
                labelClasses="name-label"
                class="budget-input"
                autocomplete="off"
                bind:value={budget}
                name="budget"
                placeholder="2"
                type="number"
            />
            <button type="submit">CREATE</button>
        </form>
    </div>
</main>

<style>
    main {
        width: 100%;
        min-height: 100vh;
    }

    .content {
        width: calc(100% - 50px);
        margin-left: 25px;
    }

    button {
        height: 40px;
        padding: 0px 8px;
        margin: 5px 0px;
        background-color: #0e0d0d;
        color: white;
        border: none;
        font-size: 20px;
    }

    button:active {
        background-color: #0e0d0dcc;
    }

    form :global(.name-label) {
        font-weight: 500;
        padding: 10px 0px;
        color: rgba(0, 0, 0, 0.7);
        font-size: 20px;
    }

    form {
        display: flex;
        flex-direction: column;
        width: 400px;
    }

    form :global(.name-input) {
        margin-top: 0.5rem;
        width: 100%;
    }
</style>
