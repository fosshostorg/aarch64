type DropdownItem = {
	label: string;
	icon: string;
	action: (e: MouseEvent) => void;
};


// NEW TYPES

type User = {
	email: string;
	projects: Project[];
}

type Project = {
	"_id": string;
	name: string;
	vms: VM[];
}

type VM = {
	"_id": string;
	hostname: string;
	pop: string;
	project: string;
	prefix: string;
	os: string;
	host: number;
	vcpus: number;
	memory: number;
	disk: number;
}