<script>
	import { link } from "svelte-spa-router";
	import active from "svelte-spa-router/active";
	import { Projects } from "../stores";

	// let projects = [{name: "vela's Project", route: '/projects/1'}, {name: "nqdrt1's Long Project Name", route: '/projects/2'}]

	let sidebar = [
		{ header: "Projects", items: [], open: true },
		{
			header: "Manage",
			items: [{ name: "Create New VM", route: "/dashboard/create" }],
			open: true,
		},
		{
			header: "Account",
			items: [
				// { name: "Settings", route: "/account/settings" },
				// { name: "API", route: "https://github.com/", isGlobal: true },
				{ name: "Docs", route: "/docs" },
			],
			open: true,
		},
	];
</script>

<nav>
	<img class="logo" src="./img/ARM-64.png" alt="ARM-64 Logo" />
	<ul class="sidebar-categories">
		{#each sidebar as category}
			<divider />
			<li class="sidebar-category">
				<span
					class="sidebar-category-header noselect"
					on:click={() => {
						category.open = !category.open;
					}}>
					{category.header.toUpperCase()}
					<span
						class="material-icons dropdown"
						class:rotate={!category.open}>
						expand_more
					</span>
				</span>
				<ul
					class="sidebar-category-items"
					class:closed={!category.open}>
					{#if category.header == 'Projects'}
						{#each $Projects as project}
							<a
								class="sidebar-category-item"
								href={'/dashboard/projects/' + project._id}
								use:link
								use:active={{ path: new RegExp('/dashboard/projects/' + project._id + '/*'), className: 'sidebar-item-active' }}>
								<span> {project.name} </span>
							</a>
						{/each}
						<a
							class="sidebar-category-item"
							href={'/dashboard/projects/create'}
							use:link
							use:active={{ path: '/dashboard/projects/create', className: 'sidebar-item-active' }}>
							<span
								class="material-icons project-add-button">add</span>
							<span class="project-add-button">
								New Project
							</span>
						</a>
					{:else}
						{#each category.items as item}
							{#if item.isGlobal}
							<a
								class="sidebar-category-item"
								href={item.route}
								>
								<span> {item.name} </span>
							</a>
							{:else}
							<a
								class="sidebar-category-item"
								href={item.route}
								use:link
								use:active={{ path: item.route + '*', className: 'sidebar-item-active' }}>
								<span> {item.name} </span>
							</a>
							{/if}
						{/each}
					{/if}
				</ul>
			</li>
		{/each}
	</ul>
</nav>

<style>
	nav {
		background-color: #0e0d0d;
		width: var(--sidebar-width);
		height: 100vh;
		position: sticky;
		top: 0;
		left: 0;
		display: flex;
		flex-flow: column nowrap;
		align-items: center;
	}

	.logo {
		width: calc(var(--sidebar-width) - 100px);
		margin: 25px 0px;
	}

	divider {
		display: block;
		width: calc(var(--sidebar-width) - 50px);
		height: 1px;
		background-color: white;
		opacity: 0.3;
	}

	li,
	ul {
		list-style-type: none;
	}

	.project-add-button {
		opacity: 0.75;
	}

	.sidebar-categories {
		width: calc(var(--sidebar-width) - 50px);
		height: auto;
		color: white;
		margin: 0px;
		padding: 0px;
	}

	.sidebar-category {
		display: flex;
		flex-direction: column;
		margin-bottom: 20px;
	}

	.sidebar-category-header {
		width: auto;
		font-size: 20px;
		font-weight: bold;
		padding: 0px;
		margin: 0px;
		margin-left: 7px;
		margin-top: 15px;
		padding-bottom: 5px;
		cursor: pointer;
	}

	.sidebar-category-items {
		font-size: 18px;
		width: 100%;
		margin: 0px;
		padding: 0px;
		padding-left: 25px;
	}

	.sidebar-category-item {
		width: calc(100% - 25px);
		height: 40px;
		margin: 0px;
		padding: 0px;
		display: flex;
		align-items: center;
		text-decoration: none;
	}

	.sidebar-category-item span {
		color: white;
		text-decoration: none;
		text-overflow: ellipsis;
		overflow: hidden;
		white-space: nowrap;
	}

	.dropdown {
		float: right;
	}

	:global(.sidebar-item-active) {
		font-weight: bold;
	}

	:global(.sidebar-item-active)::before {
		content: " ";
		width: var(--sidebar-width);
		height: 40px;
		background-color: white;
		opacity: 0.25;
		display: block;
		position: absolute;
		left: 0;
	}

	.rotate {
		transform: rotate(90deg);
	}

	.closed {
		display: none;
	}
</style>
