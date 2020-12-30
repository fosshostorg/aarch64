type VM = {
    hostname: string,
    os: string,
    ipv4: string,
    ipv6: string,
    host: string,
    uuid: string,
    online: boolean;
    vcpus: number;
    memory: number;
    disk: number;
}

type DropdownItem = {
    label: string;
    icon: string;
    action: (e: MouseEvent) => void;
}