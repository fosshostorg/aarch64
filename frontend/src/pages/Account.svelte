<script>
    import PageHeader from "../components/PageHeader.svelte";
    import Navbar from "../components/Navbar.svelte";
    import {User, Projects} from "../stores";
    import Button from "../components/Button.svelte";
    import { checkMeta } from "../utils";

    $: console.log($User);
    $: console.log($Projects);

    const handlePasswordReset = async () => {
        await fetch("__apiRoute__/auth/start_password_reset", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: $User.email })
        }).then(res => res.json())
        .then(body => {
            checkMeta(body);
        })
    }
</script>

<Navbar
    breadcrumbs={[
        { label: 'Dashboard', path: '/dashboard' },
        { label: 'Account', path: `/dashboard/account` }
    ]}
/>
<PageHeader>Account Information</PageHeader>
<main>
    <div class="field">
        <b>Email:</b> {$User.email}
    </div>
    <div class="field">
        <b>Projects: </b> {$Projects.length}
    </div>
    <div class="password">
        <Button on:click={handlePasswordReset} outline={true} color="#aa1717">RESET PASSWORD</Button>
    </div>
</main>


<style>
    main {
        padding: 2rem;
    }

    div {
        margin: 1rem 0rem;
    }

    .password {
        padding-top: 2rem;
        border-top: 1px solid black;
    }

    .field {
        font-size: 1.1rem;
    }
</style>