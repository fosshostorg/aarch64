import {replace} from "svelte-spa-router";
import { Snackbars, Projects } from "./stores";

function vmControl(vm: any, command: any) {
	fetch('api/vms/'+command, {
		method: 'POST',
		headers: {
		  'Accept': 'application/json',
		  'Content-Type': 'application/json'
		},
		body: JSON.stringify({"vm":vm._id})
	  }).then((d)=>d.json()).then((r)=>{
		  alert(r.meta.message)
	  })
}

export function dropdownItems(vm: any): DropdownItem[] {
	return [
		{
			label: "CONSOLE",
			icon: "airplay",
			action: (e) => {
				alert(`ssh -p 2222 ${vm._id}@${vm.pop}${vm.host}.infra.aarch64.com`);
			},
		},
		{ label: "START", icon: "play_arrow", action: (e) => {
			vmControl(vm, "start")
		} },
		{ label: "SHUTDOWN", icon: "power_settings_new", action: (e) => {
			vmControl(vm, "shutdown")
		} },
		{ label: "REBOOT", icon: "refresh", action: (e) => {
			vmControl(vm, "reboot")
		} },
		{ label: "STOP", icon: "stop", action: (e) => {
			vmControl(vm, "stop")
		} },
		{ label: "RESET", icon: "sync_problem", action: (e) => {
			vmControl(vm, "reset")
		} },
		{
			label: "DELETE",
			icon: "delete",
			action: (e) => {
				deleteVM(vm._id).then(() => {
					Projects.update((projects: Project[]) => {
						return projects.map((p: Project) => {
							if (p._id == vm.project) {
								p.vms = p.vms.filter(v => v._id !== vm._id)
							}
							return p;
						})
					})
					replace("/dashboard/projects/" + vm.project)
				});
			},
		},
	];
}

export const checkMeta = (body: any): boolean => {
	if (body !== null && !body.meta.success) {
		console.error("Failed request: " + body.meta.message);
		Snackbars.update((s) => [
			...s,
			{
				color: "red",
				status: "error",
				message: body.meta.message,
				grouped: true,
			},
		]);
	} else if (body !== null && body.meta.success) {
		Snackbars.update((s) => [
			...s,
			{
				color: "green",
				status: "200",
				message: body.meta.message,
				grouped: true,
			},
		]);
	}
	return body.meta.success;
};

export const getUserInfo = async () => {
	let body: any = null;
	await fetch("__apiRoute__/auth/user", {
		method: "GET",
	})
		.then(async (res) => {
			if (!res.ok) {
				console.log("User not logged in, redirecting...");
			} else {
				body = await res.json();
				body = body.data;
			}
		})
		.catch((err) => console.log(err));

	return body;
};

export const getUserProjects = async () => {
	let body: any = null;
	const res = await fetch("__apiRoute__/projects", {
		method: "GET",
	})
		.then(async (res) => {
			body = await res.json();
			body = body.data;
		})
		.catch((err) => console.log(err));

	return body;
};

export const updateUserInfo = async (user: { email: string }) => {
	console.log(
		"Would have updated user info, but there is no route to do so >:("
	);
};

export const createVM = async (
	project: string,
	hostname: string,
	plan: string,
	os: string,
	pop: string
) => {
	let body: any = null;
	await fetch("__apiRoute__/vms/create", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ project, hostname, plan, os, pop }),
	})
		.then(async (res) => {
			body = await res.json();
			checkMeta(body);
			body = body.data;
		})
		.catch((err) => console.log(err));

	return body;
};

export const getUserInfoAndProjects = async (): Promise<{
	user: any;
	projects: any;
}> => {
	// @ts-ignore
	if (!__production__) {
		return {
			user: {
				email: "dev@dev.dev",
				admin: true
			},
			projects: [
				{
					_id: "605d1fbc361f9e55eec97986",
					name: "Test Project",
					users: ["user1@example.com", "user2@example.com"],
					budget: 10,
					vms: [
						{
							hostname: "testvm1",
							vcpus: 4,
							memory: 8,
							ssd: 16,
							pop: "dfw",
							project: "605d1fbc361f9e55eec97986",
							host: 0,
							os: "debian",
							index: 0,
							prefix: "2001:db8:ffff::/64",
							gateway: "2001:db8:ffff::1",
							address: "2001:db8:ffff::2/64",
							_id: "605d1fea3c05da2790ea3dbb",
							password: "3c05da2790ea3d3c05da2790ea3d3c05da2790ea3d",
							phoned_home: true,
							creator: "user@example.com",
							created: {
								by: "605d1fea3c05da2790ea3fff",
								at: 1617394497
							}
						},
					],
				}, {
					_id: "605d1fbc361f9e55eec97987",
					name: "Test Project 2",
					budget: 8,
					users: ["user1@example.com", "user2@example.com"],
					vms: [
						{
							hostname: "testvm2",
							vcpus: 4,
							memory: 8,
							ssd: 16,
							pop: "dfw",
							project: "605d1fbc361f9e55eec97987",
							host: 0,
							os: "debian",
							index: 0,
							prefix: "2001:db8:fffe::/64",
							gateway: "2001:db8:fffe::1",
							address: "2001:db8:fffe::2/64",
							_id: "605d1fea3c05da2790ea3dbc",
							password: "3c05da2790ea3d3c05da2790ea3d3c05da2790ea3d",
							phoned_home: true,
							creator: "user@example.com",
							created: {
								by: "605d1fea3c05da2790ea3fff",
								at: 1617394497
							}
						},
					],
				},
			],
		};
	}

	const user: any = await getUserInfo();
	const projects: any = await getUserProjects();

	return { user: user, projects };
};

export async function deleteVM(id: string) {
	let body;

	if (confirm("Are you sure you want to delete this VM?")) {
		await fetch("__apiRoute__/vms/delete", {
			method: "DELETE",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ vm: id }),
		})
			.then((resp) => resp.json())
			.then((data) => {
				body = data.data;
			})
			.catch((err) => alert(err));
	}

	return body;
}

export const consoleWelcomeMessage = () => {
	console.log("Welcome to AArch64!");
};

export const getMockSystemData = () => {
	return {
		pops: [
			{
				_id: "605a8ee1cdf6bb6559de1cb7",
				name: "dfw",
				provider: "Equinix Metal",
				location: "Dallas, TX",
				peeringdb_id: 4,
			},
		],
		plans: {
			"v1.xsmall": {
				vcpus: 1,
				memory: 1,
				ssd: 4,
			},
			"v1.small": {
				vcpus: 2,
				memory: 4,
				ssd: 8,
			},
			"v1.medium": {
				vcpus: 4,
				memory: 8,
				ssd: 16,
			},
			"v1.large": {
				vcpus: 8,
				memory: 16,
				ssd: 32,
			},
			"v1.xlarge": {
				vcpus: 16,
				memory: 32,
				ssd: 64,
			},
		},
		oses: {
			debian: {
				version: "10.8",
				url:
					"https://cdimage.debian.org/cdimage/openstack/current/debian-10-openstack-arm64.qcow2",
			},
			ubuntu: {
				version: "20.10",
				url:
					"https://cloud-images.ubuntu.com/groovy/current/groovy-server-cloudimg-arm64.img",
			},
		},
	};
};
