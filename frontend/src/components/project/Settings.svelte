<script lang="ts">
    import { push } from 'svelte-spa-router'
    import { User } from '../../stores'
    import { checkMeta, updateProjects } from '../../utils'
    import Button from '../Button.svelte'
    import Input from '../Input.svelte'

    /* URL parameters and the current project, passed down from the Project page */
    export let params: any = {}
    export let project: Project

    /* Variables bound to form inputs for adding emails and chaning budget */
    let newUserEmail = ''
    let newBudget = 0

    /* Adds a new user to the project */
    const submitAddUser = () => {
        fetch('__apiRoute__/project/adduser', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project: params.project_id, email: newUserEmail })
        })
            .then(resp => resp.json())
            .then(data => {
                if (checkMeta(data)) {
                    updateProjects()
                }
            })
            .catch(err => console.error(err))
    }

    /* Changes the project's budget */
    const changeBudget = () => {
        fetch('__apiRoute__/project/changebudget', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project: params.project_id, budget: newBudget })
        })
            .then(resp => resp.json())
            .then(data => {
                if (checkMeta(data)) {
                    updateProjects()
                }
            })
            .catch(err => console.error(err))
    }

    /* Deletes the project and forwards the user to the dashboard */
    const deleteProject = () => {
        if (
            confirm(
                'Are you sure you want to delete this project? This action cannot be undone.'
            )
        ) {
            fetch('__apiRoute__/project', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ project: params.project_id })
            })
                .then(resp => resp.json())
                .then(data => {
                    if (checkMeta(data)) {
                        push('/dashboard')
                    }
                })
                .catch(err => console.error(err))
        }
    }
</script>

<div>
    <span class="title">Settings</span>
    <div class="user-form-container">
        <span class="user-form-subheader">Users:</span>
        <ul>
            {#each project.users as user}
                <li>{user}</li>
            {/each}
        </ul>
    </div>

    <div class="user-form-container">
        <span class="user-form-subheader">Add user to project:</span>
        <span class="user-form-subtitle"
            >Enter a user's email. Make sure they already have signed up for an account.</span
        >
        <Input
            bind:value={newUserEmail}
            autocomplete="off"
            type="text"
            class="user-input"
            placeholder="user@example.com"
        />
        <Button width="150px" on:click={() => submitAddUser()}>ADD USER</Button>
        {#if $User.admin}
            <span style="margin-top: 2rem" class="user-form-subheader"
                >Set project budget:</span
            >
            <span class="user-form-subtitle"
                >Current usage is {project.budget_used}/{project.budget}</span
            >
            <Input
                bind:value={newBudget}
                autocomplete="off"
                type="number"
                class="user-input"
                placeholder="2"
            />
            <Button width="220px" on:click={() => changeBudget()}>CHANGE BUDGET</Button>
        {/if}
        <!-- TODO: SHOULD THIS ONLY SHOW FOR PROJECT CREATOR (OR OWNER?) -->
        <Button
            width="250px"
            color="#aa1717"
            style="margin-top: 3rem;"
            on:click={deleteProject}>DELETE PROJECT</Button
        >
    </div>
</div>

<style>
    .title {
        color: #0e0d0d;
        opacity: 0.7;
        padding: 15px;
        font-size: 22px;
        font-weight: 500;
    }

    .user-form-container {
        display: flex;
        flex-direction: column;
        margin-top: 25px;
        padding-left: 15px;
    }

    .user-form-subheader {
        font-size: 22px;
        font-weight: 500;
    }

    .user-form-subtitle {
        font-size: 16px;
        opacity: 0.5;
        padding-bottom: 10px;
    }

    div :global(.user-input) {
        margin: 0 0 10px 0;
        width: 350px;
    }
</style>
