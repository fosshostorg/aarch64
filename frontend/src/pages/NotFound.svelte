<script>
	import { link, push } from "svelte-spa-router";
	import PageTitle from "../components/PageTitle.svelte";
</script>

<PageTitle title="404 Not Found" />

<main>
	<div>
		<img alt="AARCH64 Logo" src="./img/AARCH64B.png" />
		<h1>404 Not Found</h1>
		<a href="/" use:link>Back to home</a>
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

	a {
		color: #0e0d0d;
		font-size: 12px;
		margin-top: 10px;
	}

	div {
		width: 324px;
		height: 275px;
		background-color: white;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	img {
		width: calc(100% - 50px);
		margin-top: 25px;
	}
</style>
