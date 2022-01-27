type DropdownItem = {
    label: string;
    icon: string;
    action: (e: MouseEvent) => void;
};

type Snackbar = {
    color?: string;
    status?: string | number;
    message?: string;
    grouped?: boolean;
    timeout?: number;
};

type User = {
    email: string;
    projects: Project[];
    admin: boolean;
};

type Project = {
    _id: string;
    name: string;
    vms: VM[];
    users: string[];
    budget: number;
    budget_used: number;
};

type VM = {
    _id: string;
    hostname: string;
    pop: string;
    project: string;
    prefix: string;
    os: string;
    host: number;
    vcpus: number;
    memory: number;
    ssd: number;
    password: string;
    phoned_home: boolean;
    address: string;
    gateway: string;
    creator: string;
    nat?: {
        host: string;
        vm: string
    },
    state: number; // https://libvirt.org/html/libvirt-libvirt-domain.html#virDomainState
    created: { by: string; at: number };
};

type System = {
    pops: Pop[];
    plans: { [key: string]: Plan };
    oses: { [key: string]: OS };
};

type OS = {
    version: string;
    image: string;
};

type Pop = {
    _id: string;
    name: string;
    provider: string;
    location: string;
    peeringdb_id: number;
    ui_disable: boolean;
};

type Plan = {
    vcpus: number;
    memory: number;
    ssd: number;
};

type Log = {
    _id: string;
    time: number;
    title: string;
    user_id: string;
    user_name: string;
    project_id: string;
    project_name: string;
    proxy_id: string;
    proxy_name: string;
    vm_id: string;
    vm_name: string;
};

type APIResponse<Type> = {
    meta: {
        success: boolean;
        message: string;
    };
    data: Type;
};

type ProxyItem = {
    hostname: string;
    vm: {
        hostname: string;
        _id: string;
    };
    icon: {
        value: string;
        id: string;
    };
};

type Proxy = {
    _id: string;
    project: string;
    label: string;
    vm: string;
};
