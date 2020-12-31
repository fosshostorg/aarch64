<script lang="ts">
	export let id: string = "";
	export let group: string = "";
</script>

<label class="container" on:click>
	<input type="radio" value={id} bind:group />
	<slot />
</label>

<style>
	label {
		display: flex;
	}

	.container input {
		opacity: 0;
		cursor: default;
		position: absolute;
	}
</style>
