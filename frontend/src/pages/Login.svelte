<script>
	import { link, push } from "svelte-spa-router";
	import PageTitle from "../components/PageTitle.svelte";
	import Button from "../components/Button.svelte";
	import { checkMeta } from "../utils";

	let email, password = "";

	const handleSubmit = async (e) => {
		fetch("__apiRoute__/auth/login", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ email, password }),
		})
			.then((resp) => resp.json())
			.then(async (data) => {
				if (checkMeta(data)) {
					push("/dashboard/");
				}
			})
			.catch((err) => console.log(err));
	};
</script>


<PageTitle title="AARCH64 Dashboard Login" />
<main>
	<div>
		<img alt="AARCH64 Logo" src="./img/Fosshost_Light.png" />
		<form on:submit|preventDefault={handleSubmit}>
			<input
				autocomplete="email"
				bind:value={email}
				placeholder="Email"
				type="email"
			/>
			<input
				autocomplete="password"
				bind:value={password}
				placeholder="Password"
				type="password"
			/>
			<Button width="100%" type="submit">LOGIN</Button>
		</form>
		<a href="/signup" use:link>Don't have an account? <b>Sign Up</b></a>
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
		height: 38px;
		color: #0e0d0d;
		padding: 0 0 0 10px;
		font-size: 18px;
		margin: 0 0 18px 0;
	}

	img {
		width: calc(100% - 50px);
		margin-top: 25px;
	}
</style>
