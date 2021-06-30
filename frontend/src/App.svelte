<script lang="ts">
    import Router, { location, push } from 'svelte-spa-router';
    import { wrap } from 'svelte-spa-router/wrap';
    import Index from './pages/Index.svelte';
    import { onMount } from 'svelte';
    import {
        consoleWelcomeMessage,
        getUserInfoAndProjects,
        getUserProjects
    } from './utils';
    import { Projects, User, Snackbars } from './stores';
    import Dashboard from './Dashboard.svelte';
    import NotFound from './pages/NotFound.svelte';
    import MDPWrapper from 'rollup-plugin-mdsvex-pages/src/components/MDPWrapper.svelte';
    import Snackbar from './components/Snackbar.svelte';
    import LoginOrSignup from './pages/LoginOrSignup.svelte';

    const dashboardWrap = wrap({
        component: Dashboard,
        conditions: [
            async () => {
                return await authenticate();
            }
        ]
    });

    const routes = {
        '/': Index,
        '/login': wrap({
            component: LoginOrSignup,
            props: {
                isLogin: true
            }
        }),
        '/signup': wrap({
            component: LoginOrSignup,
            props: {
                isLogin: false
            }
        }),
        '/dashboard': dashboardWrap,
        '/dashboard/*': dashboardWrap,
        '*': NotFound
    };

    let updateInterval: number | null = null;

    //TODO: This might not work perfectly, need to do more testing. -SETH
    function updateProjects() {
        if ($User !== null) {
            void getUserProjects().then(data => {
                // eslint-disable-next-line no-undef
                $Projects = data as Project[];
            });
            if (updateInterval == null) {
                updateInterval = setInterval(updateProjects, 15000);
            }
        }
    }

    async function authenticate() {
        let res = await getUserInfoAndProjects();
        if (res.user == null) {
            return false;
        }
        $User = res.user;
        $Projects = res.projects;
        updateProjects();
        return true;
    }

    function conditionsFailed() {
        // Authentication has failed.
        void push('/login');
    }

    onMount(() => {
        consoleWelcomeMessage();
    });
</script>

<MDPWrapper>
    <main class:width-styles={!$location.includes('/docs')}>
        <Router {routes} on:conditionsFailed={conditionsFailed} />
    </main>
</MDPWrapper>

<div>
    {#each $Snackbars as sb}
        <Snackbar {...sb} />
    {/each}
</div>

<style>
    main.width-styles {
        width: 100%;
        display: flex;
        min-width: 1300px;
        padding: 0px;
    }

    main {
        padding: 1rem;
    }

    div {
        position: fixed;
        bottom: 1rem;
        left: 50%;
        transform: translate(-50%, 0%);
    }
</style>
