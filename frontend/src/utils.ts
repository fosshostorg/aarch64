import { replace } from 'svelte-spa-router';
import { Snackbars, Projects } from './stores';

async function vmControl(vm: VM, command: string) {
    await fetch('api/vms/' + command, {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ vm: vm._id })
    })
        .then(res => res.json())
        .then(body => {
            checkMeta(body);
            updateProjects();
        });
}

export function dropdownItems(vm: VM): DropdownItem[] {
    return [
        {
            label: 'CONSOLE',
            icon: 'airplay',
            action: () => {
                alert(`ssh -p 2222 ${vm._id}@${vm.pop}${vm.host}.infra.aarch64.com`);
            }
        },
        {
            label: 'START',
            icon: 'play_arrow',
            action: () => {
                void vmControl(vm, 'start');
            }
        },
        {
            label: 'SHUTDOWN',
            icon: 'power_settings_new',
            action: () => {
                void vmControl(vm, 'shutdown');
            }
        },
        {
            label: 'REBOOT',
            icon: 'refresh',
            action: () => {
                void vmControl(vm, 'reboot');
            }
        },
        {
            label: 'STOP',
            icon: 'stop',
            action: () => {
                void vmControl(vm, 'stop');
            }
        },
        {
            label: 'RESET',
            icon: 'sync_problem',
            action: () => {
                void vmControl(vm, 'reset');
            }
        },
        {
            label: 'SETUP NAT',
            icon: 'cloud',
            action: () => {
                void vmControl(vm, 'nat');
            }
        },
        {
            label: 'DELETE',
            icon: 'delete',
            action: async () => {
                await deleteVM(vm._id).then(() => {
                    Projects.update((projects: Project[]) => {
                        return projects.map((p: Project) => {
                            if (p._id == vm.project) {
                                p.vms = p.vms.filter(v => v._id !== vm._id);
                            }
                            return p;
                        });
                    });
                    void replace('/dashboard/projects/' + vm.project);
                });
            }
        }
    ];
}

export const checkMeta = (body: {
    meta: { success: boolean; message: string };
}): boolean => {
    if (body !== null && !body.meta.success) {
        console.error('Failed request: ' + body.meta.message);
        Snackbars.update((s: Snackbar[]) => [
            ...s,
            {
                color: 'red',
                status: 'error',
                message: body.meta.message,
                grouped: true
            }
        ]);
    } else if (body !== null && body.meta.success) {
        Snackbars.update((s: Snackbar[]) => [
            ...s,
            {
                color: 'green',
                status: '200',
                message: body.meta.message,
                grouped: true
            }
        ]);
    }
    return body.meta.success;
};

export const getUserInfo = async (): Promise<User> => {
    let body: User = null;
    await fetch('__apiRoute__/auth/user', {
        method: 'GET'
    })
        .then(async res => {
            if (!res.ok) {
                console.log('User not logged in, redirecting...');
            } else {
                const response: APIResponse<User> =
                    (await res.json()) as APIResponse<User>;
                body = response.data;
            }
        })
        .catch(err => console.log(err));

    return body;
};

export const getUserProjects = async (): Promise<Project[] | null> => {
    let body: Project[] | null = null;
    await fetch('__apiRoute__/projects', {
        method: 'GET'
    })
        .then(async res => {
            const response: APIResponse<Project[]> = (await res.json()) as APIResponse<
                Project[]
            >;
            body = response.data;
        })
        .catch(err => console.log(err));

    return body;
};

export const updateProjects = async (): Promise<void> => {
    const data = await getUserProjects();
    Projects.set(data as Project[]);
};

export const createVM = async (
    project: string,
    hostname: string,
    plan: string,
    os: string,
    pop: string
): Promise<void> => {
    await fetch('__apiRoute__/vms/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ project, hostname, plan, os, pop })
    })
        .then(async res => {
            const body: APIResponse<VM> = (await res.json()) as APIResponse<VM>;
            checkMeta(body);
        })
        .catch(err => console.log(err));
};

export const getUserInfoAndProjects = async (): Promise<{
    user: User;
    projects: Project[];
}> => {
    const user: User = await getUserInfo();
    const projects: Project[] = (await getUserProjects()) as Project[];
    return { user, projects };
};

export async function deleteVM(id: string): Promise<void> {
    if (confirm('Are you sure you want to delete this VM?')) {
        await fetch('__apiRoute__/vms/delete', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ vm: id })
        })
            .then(resp => resp.json())
            .then(data => {
                checkMeta(data);
            })
            .catch(err => alert(err));
    }
}

export const consoleWelcomeMessage = (): void => {
    console.log('Welcome to AArch64!');
};
