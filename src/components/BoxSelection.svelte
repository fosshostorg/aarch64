<script>
    import RadioButton from './RadioButton.svelte';

    let data = [
        {title: 'Debian', img: './img/debian.svg', version: 'latest'},
        {title: 'Ubuntu', img: './img/ubuntu.svg', version: 'latest'},
        {title: 'CentOS', img: './img/centos.svg', version: 'latest'}
    ]

    let current = '1';
</script>

<main>
    {#each data as option}
    <RadioButton id={option.title} bind:group={current}>
        <div class="selection-card" class:selected={current == option.title}>
            <img src={option.img} alt={option.title + ' Logo'} />
            <span class="selection-card-header">
                {option.title}
            </span>
            <divider></divider>
            <span class="selection-card-text">
                {option.version}
            </span>
        </div>
    </RadioButton>
    {/each}
</main>

<style>

    main {
        display: flex;
    }

    .selection-card {
        width: 123px;
        height: 123px;
        border: 1px solid #0e0d0d;
        background-color: #0e0d0d;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        margin-left: 15px;
        
    }

    .selection-card.selected {
        background-color: white;
    }

    img {
        padding-top: 6px;
        width: 48px;
        filter: invert(1);
    }

    .selected img {
        filter: none;
    }

    .selection-card-header {
        color: white;
        font-weight: 500;
        font-size: 22px;
    }

    .selected .selection-card-header  {
        color: #0e0d0d;
    }

    .selection-card-text {
        font-size: 18px;
        color: white;
        opacity: .6;
    }

    .selected .selection-card-text {
        color: #0e0d0d;
    }

    divider {
        width: 125px;
        height: 1px;
        background-color: white;
        margin-left: -1px;
    }

    .selected divider {
        background-color: #0e0d0d;
    }
</style>

