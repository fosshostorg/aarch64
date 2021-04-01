<script lang="ts">
  /** outlined variant? */
  export let outline: boolean = false;
  /** color of the button, can be any CSS valid string */
  export let color: string = "black";
  /** color of the button's background/text when disabled */
  export let disabledColor: string = "#aaa";
  /** material icon to render */
  export let icon: string = "";
  /** styles passed to the button component */
  export let style: string = "";
  /** disable button? */
  export let disabled: boolean = false;
  /** flip icon and text arrangement */
  export let flipped: boolean = false;
  /** width of the button */
  export let width: string = "";
  /** height of the button */
  export let height: string = "";
  /** href for button to act as link. this will wrap the button with an <a> */
  export let href: string = null;
  
  let userClasses: string = "";
  export {userClasses as class};

  $: isSlotFilled = $$slots["default"];
</script>

{#if href !== null}
  <a href={href}>
      <button class:outline class:flipped class={userClasses} style="--buttonColor:{color};width:{width};height:{height};{style}" disabled={disabled} class:disabled on:click>
          {#if icon != ""}
          <span class="material-icons button-icon" class:flipped class:icon-only={!isSlotFilled}>
              {icon}
          </span>
          {/if}
          {#if isSlotFilled}
          <div class:icon={icon != ""} class:flipped>
              <slot></slot>
          </div>
          {/if}
      </button>
  </a>
{:else}
  <button class:outline class:flipped class={userClasses} style="--buttonColor:{color};width:{width};height:{height};{style}" disabled={disabled} class:disabled on:click>
      {#if icon != ""}
      <span class="material-icons button-icon" class:flipped class:icon-only={!isSlotFilled}>
          {icon}
      </span>
      {/if}
      {#if isSlotFilled}
      <div class:icon={icon != ""} class:flipped>
          <slot></slot>
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

  button:active {
    background-color: #252424;
    border-color: #252424;
  }

  button.outlined {
    background-color: white;
    color: var(--buttonColor);
  }

  button.disabled:not(.outline) {
    background-color: #777;
  }

  button.disabled.outline {
    color: #777;
    border-color: #777;
  }

</style>