<script>
    import PageHeader from '../components/PageHeader.svelte'
    import Navbar from '../components/Navbar.svelte'
    import { push } from 'svelte-spa-router';
    import { addNewProject, getUserProjects} from '../utils';
    import { Projects } from '../stores';
import { onMount } from 'svelte';

    let name = '';

    onMount(() => {console.log('New Project mounted')})

    const handleSubmit = async (e) => {
        if (__production__ && name !== '') {
            let data = {
                name,
            }

            await addNewProject(data)
            .then(async data => {
                if (data.meta.success) {
                    await getUserProjects()
                    .then(body => {
                        $Projects = body.data;
                        push('/dashboard/projects/' + data.data);
                    })
                } else {
                    console.log(data.meta.message)
                }
            })

        } else {
            console.log('%cRequest would have been sent with name: ' + name, 'color: lightgreen');
        }
    }

</script>

<main>
    <Navbar breadcrumbs={['Dashboard', 'Projects', 'Add New Project']}/>
    <PageHeader>Add New Project</PageHeader>
    <div class="content">
        <form on:submit|preventDefault={handleSubmit}>
            <label for="name">Name your project:</label>
            <input type="text" name="name" placeholder="Name..." autocomplete="off" bind:value={name}>
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

    label {
        font-weight: 500;
        padding: 10px 0px;
        opacity: 0.7;
        font-size: 20px;
    }

    form {
        display: flex;
        flex-direction: column;
        width: 400px;
    }

    input {
        height: 40px;
        padding: 0px;
        margin: 0px;
        padding-left: 15px;
        font-size: 18px;
    }


</style>
