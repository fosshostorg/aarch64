<script>
    import {onDestroy} from 'svelte';
    export let title = '';

    let prev = document.title;
    onDestroy(() => {
        document.title = prev;
    })

</script>

<svelte:head>
    <title>
        {title}
    </title>
</svelte:head>