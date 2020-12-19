<script>
    import { link } from "svelte-spa-router";


    let email = '';
    let password = '';

    const handleSubmit = async (e) => {
        if (__production__) {
            await fetch('__apiRoute__/user/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    email: 'seth@test.org',
                    password: 'password'
                })
            })
            .then(res => res.json())
            .then(data => {console.log(data); window.location.href = '/#/create'})
            .catch(err => console.log(err))
        } else {
            console.log('%cWould have been posted with email: ' + email, 'color: lightgreen')
        }

    }

</script>

<main>
    <div>
        <img src="./img/ARM-64B.png" alt="ARM-64 Logo">
        <form on:submit|preventDefault={handleSubmit}>
            <input type="email" autocomplete="email" bind:value={email} placeholder="Email" />
            <input type="password" autocomplete="password" bind:value={password} placeholder="Password" />
            <button type="submit">LOGIN</button>
        </form>
        <a href="/signup" use:link>Don't have an account? <b>Sign Up</b></a>
    </div>
</main>


<style>
    main {
        width: 100%;
        min-height: 100vh;
        background-color: #0e0d0d;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    button {
        width: 100%;
        height: 40px;
        border: none;
        color: white;
        background-color: #0e0d0d;
        font-size: 22px;
        font-weight: 500;
        font-family: inherit;
        margin: 0px;
    }

    button:active {
        margin: 0px;
        padding: 0px 8px;
        opacity: .85;
    }

    a {
        color:#0e0d0d;
        font-size: 12px;
        margin-top: 10px;
    }

    div {
        width: 324px;
        height: 368px;
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
        margin-top: 25px;
        padding-top: 25px;
        border-top: 1px solid #0e0d0d4f;
    }

    input {
        width: calc(100% - 12px);
        border: 1px solid #0e0d0d;
        padding: 0px;
        margin: 0px;
        height: 38px;
        color: #0e0d0d;
        padding-left: 10px;
        font-size: 18px;
        margin: 0px 0px 18px 0px;
    }

    img {
        width: calc(100% - 50px);
        margin-top: 25px;
    }
</style>

