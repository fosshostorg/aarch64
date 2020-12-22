export const getUserInfo = async () => {
    const res = await fetch('__apiRoute__/user/info', {
        method: 'GET',
    })
    .catch(err => console.log(err))

    let body = res.json();
    return body;
}

export const getUserProjects = async () => {
    const res = await fetch('__apiRoute__/projects', {
        method: 'GET',
    })
    .catch(err => console.log(err))

    let body = res.json();
    return body;
}

export const updateUserInfo = async (user) => {
    console.log('Would have updated user info, but there is no route to do so >:(')
}

export const addNewProject = async (data) => {
    const res = await fetch('__apiRoute__/projects', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .catch(err => console.log(err))

    let body = res.json();
    return body;
}

export const login = async (data) => {
    await fetch('__apiRoute__/user/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .catch(err => console.log(err))
    
    let body = res.json();
    return body;
}