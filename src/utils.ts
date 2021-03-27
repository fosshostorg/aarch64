const checkMeta = (body: any): void => {
	if (!body.meta.success) {
		console.warn(
			"Failed request: " + body.meta.message,
		)
	}
}

export const getUserInfo = async () => {
	let body: any = null;
	await fetch("__apiRoute__/auth/user", {
		method: "GET",
	})
		.then((res) => (body = res.json()))
		.catch((err) => console.log(err));

	checkMeta(body);
	return body.data;
};

export const getUserProjects = async () => {
	let body: any = null;
	const res = await fetch("__apiRoute__/projects", {
		method: "GET",
	})
		.then((res) => (body = res.json()))
		.catch((err) => console.log(err));

	checkMeta(body);
	return body.data;
};

export const updateUserInfo = async (user: { email: string }) => {
	console.log(
		"Would have updated user info, but there is no route to do so >:("
	);
};

export const addNewProject = async (data: { name: string }) => {
	let body: any = null;
	await fetch("__apiRoute__/project", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(data),
	})
		.then((res) => (body = res.json()))
		.catch((err) => console.log(err));

	checkMeta(body);
	return body.data;
};

export const createVM = async (project: string, hostname: string, plan: string, os: string, pop: string) => {
	let body: any = null;
	await fetch("__apiRoute__/vms/create", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({project, hostname, plan, os, pop}),
	})
		.then((res) => (body = res.json()))
		.catch((err) => console.log(err));
	
	checkMeta(body);
	return body.data;
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
					_id: "5fe427dd7354646035cd74cf",
					name: "Dev Project",
					vms: [
						{
							uuid: "11111111-66ba-1111-1111-9a3db3111a21",
							hostname: "11111111-1111-4ecc-b989-0022d2415136",
							tier: 1,
							os: "Debian",
							host: "pdx0",
							prefix: "2001:db8:18fc:184::/64",
							gateway: "2001:db8:18fc:184::1",
							enabled: true,
							vcpus: 1,
							memory: 1,
							disk: 10,
						},
					],
					keys: [],
				},
			],
		};
	}

	const user: any = await getUserInfo();
	const projects: any = await getUserProjects();

	return { user: user, projects };
};

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
