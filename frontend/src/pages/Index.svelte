<script>
    import { onMount } from 'svelte';
    import { push } from 'svelte-spa-router';

    onMount(() => {
        void push('/dashboard');
    });
</script>

<main />

<style>
    main {
        width: 100%;
        min-height: 100vh;
    }
</style>
