type VM = {
	hostname: string;
	os: string;
	prefix: string;
	gateway: string;
	host: string;
	uuid: string;
	online: boolean;
	vcpus: number;
	memory: number;
	disk: number;
	enabled: boolean;
};

type DropdownItem = {
	label: string;
	icon: string;
	action: (e: MouseEvent) => void;
};
