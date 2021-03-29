import {push} from "svelte-spa-router";

export function dropdownItems(vm: any): DropdownItem[] {
    return [
        {
            label: "CONSOLE",
            icon: "airplay",
            action: (e) => {
                alert(`ssh -p 2222 ${vm._id}@${vm.pop}${vm.host}.aarch64.com`);
            },
        },
        // { label: "SHUTDOWN", icon: "power_settings_new", action: (e) => {} },
        // { label: "REBOOT", icon: "refresh", action: (e) => {} },
        // { label: "STOP", icon: "stop", action: (e) => {} },
        // { label: "RESET", icon: "sync_problem", action: (e) => {} },
        {
            label: "DELETE", icon: "delete", action: (e) => {
                deleteVM(vm._id).then(() => {
                    push("/")
                });
            }
        },
    ]
}

const checkMeta = (body: any): void => {
    // if (body !== null && !body.meta.success) {
    // 	console.warn(
    // 		"Failed request: " + body.meta.message,
    // 	)
    // }
};

export const getUserInfo = async () => {
    let body: any = null;
    await fetch("__apiRoute__/auth/user", {
        method: "GET",
    })
        .then(async (res) => {
            if (!res.ok) {
                console.log("User not logged in, redirecting...");
                // push("/login");
                // body = null;
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
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({project, hostname, plan, os, pop}),
    })
        .then(async (res) => {
            body = await res.json();
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
            },
            projects: [
                {
                    _id: "605d1fbc361f9e55eec97986",
                    name: "Test Project",
                    "users": [
                        "user1@example.com",
                        "user2@example.com"
                    ],
                    vms: [
                        {
                            "hostname": "testvm1",
                            "vcpus": 4,
                            "memory": 8,
                            "disk": 16,
                            "pop": "dfw",
                            "project": "605d1fbc361f9e55eec97986",
                            "host": 0,
                            "os": "debian",
                            "index": 0,
                            "prefix": "2001:db8:ffff::/64",
                            "gateway": "2001:db8:ffff::1",
                            "address": "2001:db8:ffff::2/64",
                            "_id": "605d1fea3c05da2790ea3dbb",
                            "password": "3c05da2790ea3d3c05da2790ea3d3c05da2790ea3d",
                            "phoned_home": true
                        },
                    ],
                },
            ],
        };
    }

    const user: any = await getUserInfo();
    const projects: any = await getUserProjects();

    return {user: user, projects};
};

export async function deleteVM(id: string) {
    let body;

    if (prompt("Are you sure you want to delete this VM?")) {
        await fetch("__apiRoute__/vms/delete", {
            method: "DELETE",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({vm: id})
        })
            .then(resp => resp.json())
            .then(data => {
                body = data.data;
            })
            .catch((err) => alert(err));
    }

    return body;
}

export const consoleWelcomeMessage = () => {
    console.log(
        "%c \n\
                           AAA                 RRRRRRRRRRRRRRRRR     MMMMMMMM               MMMMMMMM                             66666666           444444444  \n\
                          A:::A                R::::::::::::::::R    M:::::::M             M:::::::M                            6::::::6           4::::::::4  \n\
                         A:::::A               R::::::RRRRRR:::::R   M::::::::M           M::::::::M                           6::::::6           4:::::::::4  \n\
                        A:::::::A              R::::::R     R:::::R  M:::::::::M         M:::::::::M                          6::::::6           4::::44::::4  \n\
                       A:::::::::A             R::::::R     R:::::R  M::::::::::M       M::::::::::M                         6::::::6           4::::4 4::::4  \n\
                      A:::::A:::::A            R::::::R     R:::::R  M:::::::::::M     M:::::::::::M                        6::::::6           4::::4  4::::4  \n\
                     A:::::A A:::::A           R::::::RRRRRR:::::R   M:::::::M::::M   M::::M:::::::M                       6::::::6           4::::4   4::::4  \n\
                    A:::::A   A:::::A          R:::::::::::::::RR    M::::::M M::::M M::::M M::::::M   ---------------    6::::::::66666     4::::444444::::444\n\
                   A:::::A     A:::::A         R::::::RRRRRR:::::R   M::::::M  M::::M::::M  M::::::M   -:::::::::::::-   6::::::::::::::66   4::::::::::::::::4\n\
                  A:::::AAAAAAAAA:::::A        R::::::R     R:::::R  M::::::M   M:::::::M   M::::::M   ---------------   6::::::66666:::::6  4444444444:::::444\n\
                 A:::::::::::::::::::::A       R::::::R     R:::::R  M::::::M    M:::::M    M::::::M                     6:::::6     6:::::6           4::::4  \n\
                A:::::AAAAAAAAAAAAA:::::A      R::::::R     R:::::R  M::::::M     MMMMM     M::::::M                     6:::::6     6:::::6           4::::4  \n\
               A:::::A             A:::::A     R::::::R     R:::::R  M::::::M               M::::::M                     6::::::66666::::::6           4::::4  \n\
              A:::::A               A:::::A    R::::::R     R:::::R  M::::::M               M::::::M                      66:::::::::::::66            4::::4  \n\
             A:::::A                 A:::::A   R::::::R     R:::::R  M::::::M               M::::::M                        66:::::::::66              4::::4  \n\
            AAAAAAA                   AAAAAAA  RRRRRRRR     RRRRRRR  MMMMMMMM               MMMMMMMM                          666666666                444444  \n ",
        "font-size: .4rem; display: flex; overflow: hidden;"
    );
};

export const getMockSystemData = () => {
    return {
        "pops": [
            {
                "_id": "605a8ee1cdf6bb6559de1cb7",
                "name": "dfw",
                "provider": "Equinix Metal",
                "location": "Dallas, TX",
                "peeringdb_id": 4
            }
        ],
        "plans": {
            "v1.xsmall": {
                "vcpus": 1,
                "memory": 1,
                "disk": 4
            },
            "v1.small": {
                "vcpus": 2,
                "memory": 4,
                "disk": 8
            },
            "v1.medium": {
                "vcpus": 4,
                "memory": 8,
                "disk": 16
            },
            "v1.large": {
                "vcpus": 8,
                "memory": 16,
                "disk": 32
            },
            "v1.xlarge": {
                "vcpus": 16,
                "memory": 32,
                "disk": 64
            }
        },
        "oses": {
            "debian": {
                "version": "10.8",
                "url": "https://cdimage.debian.org/cdimage/openstack/current/debian-10-openstack-arm64.qcow2"
            },
            "ubuntu": {
                "version": "20.10",
                "url": "https://cloud-images.ubuntu.com/groovy/current/groovy-server-cloudimg-arm64.img"
            }
        }
    }
}
