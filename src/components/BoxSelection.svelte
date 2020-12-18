<script>
    import RadioButton from './RadioButton.svelte';

    let current = '1';
</script>

<main>
    <RadioButton id="1" bind:group={current}>
        <div class="selection-card" class:selected={current == '1'}>
            <img src="./img/debian.svg" alt="Logo" />
            <span class="selection-card-header">
                Debian
            </span>
            <divider></divider>
            <span class="selection-card-text">
                latest
            </span>
        </div>
    </RadioButton>
    <RadioButton id="2" bind:group={current}>
        <div class="selection-card" class:selected={current == '2'}>
            <img src="./img/ubuntu.svg" alt="Logo" />
            <span class="selection-card-header">
                Ubuntu
            </span>
            <divider></divider>
            <span class="selection-card-text">
                latest
            </span>
        </div>
    </RadioButton>
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
        transition: ease background-color .1s;
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

