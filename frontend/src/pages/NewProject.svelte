<script>
    import PageHeader from "../components/PageHeader.svelte";
    import Navbar from "../components/Navbar.svelte";
    import {push} from "svelte-spa-router";
    import {Projects} from "../stores";
    import PageTitle from "../components/PageTitle.svelte";

    let name = "";

    const handleSubmit = async (e) => {
        if (__production__) {
            await fetch("__apiRoute__/project", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({name}),
            })
                .then(resp => resp.json())
                .then((data) => {
                    if (data.meta.success) {
                        $Projects = data.data;
                        push("/dashboard/projects/" + data);
                    } else {
                        alert(data.meta.message);
                    }
                })
                .catch((err) => console.log(err));
        } else {
            console.log(
                "%cRequest would have been sent with name: " + name,
                "color: lightgreen"
            );
        }
    };
</script>

<PageTitle title="New Project"/>

<main>
    <Navbar breadcrumbs={[
		{label:'Dashboard', path: '/dashboard/projects/create'},
		{label:'Add New Project', path:'/dashboard/projects/create'},
		]}/>
    <PageHeader>Add New Project</PageHeader>
    <div class="content">
        <form on:submit|preventDefault={handleSubmit}>
            <label for="name">Name your project:</label>
            <input
                    autocomplete="off"
                    bind:value={name}
                    name="name"
                    placeholder="Name..."
                    type="text"/>
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
