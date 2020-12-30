<script lang="ts">

    export let vm: VM;

</script>

<table>
    <thead>
        <tr>
            <th>IP ADDRESS</th>
            <th>GATEWAY</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>{vm.ipv4}</td>
            <td>Managed Automatically</td>
        </tr>
        <tr>
            <td>{vm.ipv6}</td>
            <td>Managed Automatically</td>
        </tr>
    </tbody>
</table>

<style>
    table {
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

    tbody tr :not(:first-child) {
        opacity: .7;
    }

    tr th:not(:first-child) {
        color: rgba(255, 255, 255, .7)
    }

</style>