<script lang="ts">
    export let vm: VM;
</script>

<table>
    <thead>
    <tr>
        <th>Created By</th>
        <th>Created On</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>{vm.creator}</td>
        <td>{new Date(vm.created.at*1000)}</td>
    </tr>
    </tbody>
</table>

<style>
    table {
        margin-top: 15px;
        width: 650px;
        border: 1px solid #0e0d0d;
        border-collapse: collapse;
        box-sizing: border-box;
    }

    tr th {
        height: 30px;
        background-color: #0e0d0d;
        color: white;
        font-size: 16px;
        text-align: left;
        padding-left: 15px;
        font-weight: 500;
        width: 50%;
    }

    tbody tr {
        border: 1px solid #0e0d0d;
        height: 40px;
        font-size: 18px;
        font-weight: 500;
    }

    tbody tr td {
        padding-left: 15px;
    }
</style>
