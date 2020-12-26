<script>
    import Sidebar from '../components/Sidebar.svelte';
    import {onMount} from "svelte";
    import {push} from "svelte-spa-router";

    onMount(() => {
        push("/dashboard")
    })
</script>

<main>
    
</main>


<style>
    main {
        width: 100%;
        min-height: 100vh;
    }
</style>

