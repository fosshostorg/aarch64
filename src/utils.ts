export const getUserInfo = async () => {
    let body: any = null;
    await fetch('__apiRoute__/user/info', {
        method: 'GET',
    })
    .then(res => body = res.json())
    .catch(err => console.log(err))

    return body;
}

export const getUserProjects = async () => {
    let body: any = null;
    const res = await fetch('__apiRoute__/projects', {
        method: 'GET',
    })
    .then(res => body = res.json())
    .catch(err => console.log(err))

    return body;
}

export const updateUserInfo = async (user: {email: string}) => {
    console.log('Would have updated user info, but there is no route to do so >:(')
}

export const addNewProject = async (data: {name: string}) => {
    let body: any = null;
    await fetch('__apiRoute__/projects', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(res => body = res.json())
    .catch(err => console.log(err))

    return body;
}

export const requestNewResources = async (project_id: string, data: {hostname: string, plan: string, os: string, location: string}) => {
    let body: any = null;
    await fetch('__apiRoute__/projects/' + project_id + '/request', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(res => body = res.json())
    .catch(err => console.log(err))

    return body;
}

export const login = async (data: {email: string, password: string}) => {
    let body: any = null;
    await fetch('__apiRoute__/user/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(res => body = res.json())
    .catch(err => console.log(err))
    
    return body;
}

export const getUserInfoAndProjects = async (): Promise<{user: any, projects: any}> => {
    // @ts-ignore
    if (!__production__) {
        return {
            user: {
                meta: {
                    success: true,
                    message: 'development variable is set to true'
                },
                data: {
                    email: 'dev@dev.dev'
                }
            },
            projects: {
                meta: {
                    success: true,
                    message: 'development variable is set to true'
                },
                data: [
                    {
                        "_id": "5fe427dd7354646035cd74cf",
                        "name": "Dev Project",
                        "vms": [
                          {
                            "uuid": "11111111-66ba-1111-1111-9a3db3111a21",
                            "hostname": "11111111-1111-4ecc-b989-0022d2415136",
                            "tier": 1,
                            "os": "Debian",
                            "host": "pdx0",
                            "ipv4": "11.111.11.1/24",
                            "ipv6": "1a0e:1f00:fe01::1/24",
                            "enabled": true
                          }
                        ],
                        "keys": []
                    }
                  ]
            }
        }
    }
    
    const user: any = await getUserInfo();
    const projects: any = await getUserProjects();

    return {user, projects}
}

export const consoleWelcomeMessage = () => {
    console.log('%c \n\
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
            AAAAAAA                   AAAAAAA  RRRRRRRR     RRRRRRR  MMMMMMMM               MMMMMMMM                          666666666                444444  \n\ ', 'font-size: .4rem; display: flex; overflow: hidden;')
}