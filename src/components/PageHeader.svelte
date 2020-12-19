<script>

</script>

<span>
    <slot />
    <divider></divider>
</span>

<style>
    span {
        font-weight: bold;
        font-size: 30px;
        margin-left: 25px;
        display: flex;
        flex-direction: column;
    }

    divider {
        height: 1px;
        background-color:#0e0d0d;
        width: calc(100% - 25px);
        margin: 4px 0px;
    }
</style>