<script lang="ts">
  let userClasses: string = "";
  export { userClasses as class };
  export let labelClasses: string = "";
  export let placeholder: string = "";
  export let label: string = "";
  export let error: string = null;
  export let disabled: boolean = false;
  export let icon: string = null;
  export let value: string = "";
  export let fixErrorHeight: boolean = false;

  let focus: boolean;
  const handleFocus = () => {
    focus = true;
  }
  const handleBlur = () => {
    focus = false;
  }

</script>

<!-- svelte-ignore a11y-label-has-associated-control -->
<label class={labelClasses} class:error={$$slots.error || error}>
  {label}
  <div>
    {#if icon}
    <span class="icon material-icons">{icon}</span>
    {/if}
    <input
      class:disabled
      class:icon
      class={userClasses}
      {placeholder}
      {disabled}
      {...$$restProps}
      on:focus={handleFocus}
      on:blur={handleBlur}
      on:input
      on:change
      bind:value
    />
  </div>
  {#if error || fixErrorHeight}
  <span class="error-wrapper">{error ? error : ""}</span>
  {/if}
  <slot name="error"></slot>
</label>

<style>
  input {
    height: 38px;
    margin: 0px;
    border: 1px solid #0e0d0d;
    color: #0e0d0d;
    padding: 0 0 0 1rem;
    font-size: 18px;
    transition: ease background-color 0.2s;
    width: 100%;
  }

  input:focus {
    outline: none;
    background-color: #f4f4f4;
  }

  input.disabled {
    pointer-events: none;
    color: #555;
    background-color: white;
  }

  input.icon {
    padding-left: 38px;
  }

  span.icon {
    position: absolute;
    top: 0;
    left: 1px;
    width: 38px;
    height: 100%;
    max-height: 40px; 
    /* This might glitch w/ adding margin to bottom of input */
    font-size: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  div {
    width: 100%;
    display: flex;
    position: relative;
  }

  label {
    width: 100%;
    display: inline-flex;
    flex-direction: column;
  }

</style>