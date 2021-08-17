<script lang="ts">
    /** outlined variant? */
    export let outline = false;
    /** color of the button, can be any CSS valid string */
    export let color = 'black';
    /** material icon to render */
    export let icon = '';
    /** styles passed to the button component */
    export let style = '';
    /** disable button? */
    export let disabled = false;
    /** flip icon and text arrangement */
    export let flipped = false;
    /** width of the button */
    export let width = '';
    /** height of the button */
    export let height = '';
    /** href for button to act as link. this will wrap the button with an <a> */
    export let href = '';

    let userClasses = '';
    export { userClasses as class };

    $: isSlotFilled = $$slots['default'];
</script>

{#if href.length > 0}
    <a {href}>
        <button
            class:outline
            class:flipped
            class={userClasses}
            style="--buttonColor:{color};width:{width};height:{height};{style}"
            {disabled}
            class:disabled
            on:click
        >
            {#if icon != ''}
                <span
                    class="material-icons button-icon"
                    class:flipped
                    class:icon-only={!isSlotFilled}
                >
                    {icon}
                </span>
            {/if}
            {#if isSlotFilled}
                <div class:icon={icon != ''} class:flipped>
                    <slot />
                </div>
            {/if}
        </button>
    </a>
{:else}
    <button
        class:outline
        class:flipped
        class={userClasses}
        style="--buttonColor:{color};width:{width};height:{height};{style}"
        {disabled}
        class:disabled
        on:click
    >
        {#if icon != ''}
            <span
                class="material-icons button-icon"
                class:flipped
                class:icon-only={!isSlotFilled}
            >
                {icon}
            </span>
        {/if}
        {#if isSlotFilled}
            <div class:icon={icon != ''} class:flipped>
                <slot />
            </div>
        {/if}
    </button>
{/if}

<style>
    button {
        height: 40px;
        border: 1px solid var(--buttonColor);
        font-weight: bold;
        font-family: inherit;
        font-size: 20px;
        background-color: var(--buttonColor);
        color: white;
        display: flex;
        align-items: center;
        padding: 0rem 1.5rem;
        cursor: pointer;
        justify-content: center;
        transition: ease background-color 0.2s;
    }

    button:active:not(.disabled) {
        background-color: #252424;
        border-color: #252424;
        padding: 0rem 1.5rem;
    }

    button.outline {
        background-color: white;
        color: var(--buttonColor);
    }

    button.disabled:not(.outline) {
        background-color: #777;
        border-color: #777;   
    }

    button.disabled.outline {
        color: #777;
        border-color: #777;
    }

    a {
        text-decoration: none;
        display: inline-flex;
        flex-shrink: 1;
    }
</style>
