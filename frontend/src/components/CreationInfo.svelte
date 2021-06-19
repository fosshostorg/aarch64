<script lang="ts">
    // @ts-nocheck
    import Table from "./Table.svelte";

    export let vm: VM;

    let headers = [
        {value: "Created By", key: "creator"},
        {value: "Created On", key: "created_at"}
    ]

    let rows = [
        {creator: vm.creator, created_at: new Date(vm.created.at*1000)},
    ]

</script>

<div>
    <Table {headers} {rows}>
        <span class="cell-slot" slot="cell" let:row let:cell>
            {cell.value}
        </span>
    </Table>
</div>

<style>
    div {
        margin-top: 15px;
        width: 650px;
    }

    div :global(table) {
        width: 100%;
    }
</style>
