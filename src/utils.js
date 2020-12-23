export const getUserInfo = async () => {
    let body = null;
    const res = await fetch('__apiRoute__/user/info', {
        method: 'GET',
    })
    .then(res => body = res.json())
    .catch(err => console.log(err))

    return body;
}

export const getUserProjects = async () => {
    let body = null;
    const res = await fetch('__apiRoute__/projects', {
        method: 'GET',
    })
    .then(res => body = res.json())
    .catch(err => console.log(err))

    return body;
}

export const updateUserInfo = async (user) => {
    console.log('Would have updated user info, but there is no route to do so >:(')
}

export const addNewProject = async (data) => {
    let body = null;
    const res = await fetch('__apiRoute__/projects', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(res => body = res.json())
    .catch(err => console.log(err))

    return body;
}

export const requestNewResources = async (project_id, data) => {
    let body = null;
    const res = await fetch('__apiRoute__/projects/' + project_id + '/request', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(res => body = res.json())
    .catch(err => console.log(err))

    return body;
}

export const login = async (data) => {
    let body = null;
    const res = await fetch('__apiRoute__/user/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(res => body = res.json())
    .catch(err => console.log(err))
    
    // let body = res.json();
    return body;
}

export const getUserInfoAndProjects = async () => {
    const user = await getUserInfo();
    const projects = await getUserProjects();
    return {user, projects}
}