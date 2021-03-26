<script lang="ts">
	export let vm: VM;
</script>

<main>
	<div class="titles">
		<span class="os"> <b>{vm.os}</b> </span>
		<span class="vCPU"> <b>{vm.vcpus}</b> vCPU </span>
		<span class="RAM"> <b>{vm.memory}GB</b> RAM </span>
		<span class="SSD"> <b>{vm.disk}GB</b> SSD </span>
	</div>
	<div class="icons">
		<span>
			<div class="version">latest</div>
			<img
				src={'./img/' + vm.os.toLowerCase() + '.svg'}
				alt={vm.os + ' Logo'} />
		</span>
		<span>
			<div>Ampere eMAG&reg;</div>
			<img src="./img/cpuICON.svg" alt={'cpu icon'} />
		</span>
		<span> 
			<div>DDR4-2666</div>
			<img src="./img/ramICON.svg" alt={'ram icon'} /> 
		</span>
		<span>
			<div class="version">ZFS Raid Z1</div>
			<img src="./img/hddICON.svg" alt={'disk icon'} />
		</span>
	</div>
</main>

<style>
	main {
		width: 650px;
		display: flex;
		flex-direction: column;
		border: 1px solid #0e0d0d;
		box-sizing: border-box;
	}

	div.titles {
		width: 100%;
		height: 35px;
		display: flex;
		align-items: center;
		justify-content: center;
		background-color: #0e0d0d;
		color: white;
		font-size: 20px;
	}

	.titles span {
		font-weight: 300;
		width: 145px;
		text-align: center;
		padding: 0px 0px;
	}

	.titles span b {
		font-weight: bold;
	}

	div.icons {
		width: 100%;
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding-bottom: 20px;
		height: 116px;
	}

	.icons span {
		height: 105px;
		width: 105px;
		display: flex;
		border: 1px solid #0e0d0d;
		border-top: none;
		margin: 0px 20px;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		transition: ease box-shadow 0.2s, ease height 0.2s;
	}

	.icons span:hover {
		box-shadow: 5px 5px 15px #ccc;
	}

	img {
		width: 75px;
		height: 75px;
		transition: ease all 0.2s;
	}

	span div.version {
		font-size: 14px;
	}

	span div {
		height: 0;
		font-size: 12px;
		overflow: hidden;
		transition: ease all 0.2s;
	}

	span:hover {
		height: 125px;
	}

	span:hover div {
		height: 25px;
		padding-bottom: 2px;
	}
</style>
