<script lang="ts">
    import { link, push, querystring } from 'svelte-spa-router';
    import { parse } from 'qs';
    import Button from '../components/Button.svelte';
    import Input from '../components/Input.svelte';
    import PageTitle from '../components/PageTitle.svelte';
    import { checkMeta } from '../utils';
import { onMount } from 'svelte';

    export let isLogin: boolean;
    export let isPassReset: boolean = false;

    let email: string;
    let password: string;

    $: query = parse($querystring);

    onMount(() => {
        if (!query.token) {
            push("/login");
        }
    })

    const handleSubmit = async () => {
        if (!isPassReset) {
            await fetch(`__apiRoute__/auth/${isLogin ? 'login' : 'signup'}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            })
            .then(resp => resp.json())
            .then(async data => {
                if (checkMeta(data)) {
                    if (isLogin) {
                        void push('/dashboard');
                    } else {
                        void push('/login');
                    }
                }
            })
            .catch(err => console.log(err));
        } else {
            await fetch("__apiRoute__/auth/password_reset", {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token: query.token, password })
            })
            .then(resp => resp.json())
            .then(async data => {
                if (checkMeta(data)) {
                    void push('/login');
                }
            })
            .catch(err => console.log(err));
        }
    };
</script>

<PageTitle title="AARCH64 Dashboard Signup" />

<main>
    <div>
        <img alt="AARCH64 Logo" src="./img/Fosshost_Light.png" />
        <form on:submit|preventDefault={handleSubmit}>
            {#if !isPassReset}
            <Input
                autocomplete="email"
                bind:value={email}
                placeholder="Email"
                type="email"
                style="margin-bottom: 20px;"
            />
            {/if}
            <Input
                autocomplete="password"
                bind:value={password}
                placeholder={(isPassReset ? "New " : "") + "Password"}
                type="password"
                style="margin-bottom: 20px;"
            />
            <Button width="100%" type="submit">{isLogin ? 'LOGIN' : (isPassReset ? 'RESET' : 'SIGNUP')}</Button>
        </form>
        {#if isLogin || isPassReset}
            <a href="/signup" use:link>Don't have an account? <b>Sign Up</b></a>
        {:else}
            <a href="/login" use:link>Already have an account? <b>Log In</b></a>
        {/if}
    </div>
</main>

<style>
    main {
        width: 100vw;
        min-height: 100vh;
        background-color: #0e0d0d;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    a {
        color: #0e0d0d;
        font-size: 12px;
        margin-top: 15px;
        margin-bottom: 25px;
    }

    div {
        width: 324px;
        /* height: 368px; */
        background-color: white;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    form {
        width: calc(100% - 50px);
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 0 auto;
        margin-top: 25px;
        padding-top: 25px;
        border-top: 1px solid #0e0d0d4f;
    }

    img {
        width: calc(100% - 50px);
        margin-top: 25px;
    }
</style>
