<script lang="ts">
    export let headers: { value: string; key: string; [key: string]: any }[] = [];
    export let rows: { value: string; [key: string]: any }[] = [];

    $: headerKeys = headers.map(({ key }) => key);
    $: rows = rows.map(row => ({
        ...row,
        cells: headerKeys.map(key => ({ key, value: row[key] }))
    }));
</script>

<table>
    <tr class="header">
        {#each headers as header}
            <th>{header.value}</th>
        {/each}
    </tr>
    {#each rows as row, i}
        <tr>
            {#each row.cells as cell, i}
                <td>
                    <slot name="cell" {row} {cell} />
                </td>
            {/each}
        </tr>
    {/each}
</table>

<style>
    table {
        border-collapse: collapse;
    }

    tr.header {
        height: 34px;
        background-color: #0e0d0d;
        color: white;
        border: 1px solid #0e0d0d;
    }

    th {
        /* display: block; */
        flex-grow: 1;
        text-align: left;
        padding: 0rem 0.75rem;
        font-weight: 500;
    }

    td {
        border: 1px solid #0e0d0d;
        height: 40px;
        padding: 0px 0.75rem;
    }
</style>
