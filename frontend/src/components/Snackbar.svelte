<script lang="ts">
  // Taken from https://github.com/knightss27/seth-js

  import { fly } from 'svelte/transition'
  import { sineInOut } from 'svelte/easing'
  import { onMount, createEventDispatcher } from 'svelte'
  // import { validateHTMLColor, validateHTMLColorName } from "validate-color";

  /** should the snackbar be visible */
  export let open: boolean = false;
  /** status code for the snackbar */
  export let status: string | number = "200";
  /** message to be displayed */
  export let message: string = "";
  
  /** snackbar color */
  export let color: string = "green";
  /** callback function for when the close button is clicked.
   *  **PLEASE NOTE**: This will override the default close management function.
   *  If you do not want a controlled snackbar, use `on:close`.
   */
  export let handleClose: (e: Event) => any = null;
  /** number of ms before snackbar is removed */
  export let timeout: number = 2000;
  /** is this snackbar part of a snackbar group? designed for internal use */
  export let grouped: boolean = false;
  /** styles passed on to the snackbar */
  export let style: string = "";
  const dispatch = createEventDispatcher();
  const internalHandleClose = (e: Event) => {
      // Dispatch close event
      dispatch('close', {event: e, open});
      
      // Call handleClose if it has been set
      if (handleClose !== null) {
          handleClose(e);
          return;
      }
      open = false;
  }
  onMount(() => {
      
      if (grouped) {
          open = true;
      }
      if (timeout !== null) {
          const autoClose = setTimeout(internalHandleClose, timeout);
          return () => {clearTimeout(autoClose);}
      }
      
  })
  
  // $: if (!(validateHTMLColorName(color) || validateHTMLColor(color))) {
  //     color = "green"
  //     console.warn("<Snackbar> component was created with invalid value for 'color'")
  // }
</script>

{#if open}
  <main 
  transition:fly="{{delay: 50, duration: 400, y:100, easing: sineInOut }}" style="--mainColor:{color};"
  class:grouped={grouped} class:ungrouped={!grouped}
  >
      <div class="wrapper" style={style}>
          <div class="status">{status}</div>
          <div class="message">{message.toLowerCase()}</div>
          <span class="material-icons" on:click={internalHandleClose} style="--mainColor:{color};">
              close
          </span>
      </div>
  </main>
{/if}

<style>
  main {
      background: white;
      border: 2px solid var(--mainColor);
      margin: 1px 0px;
  }
  main.ungrouped div.wrapper {
      position: fixed;
      bottom: 10px;
      left: 50%;
      transform: translatex(-50%);
  }
  main div.wrapper {
      color: white;
      background: var(--mainColor);
      opacity: 0.8;
      display: flex;
      align-items: center;
      overflow: hidden;
      justify-content: space-between;
  }
  div.message, div.status {
      display: flex;
      align-items: center;
      margin: 4px;
      padding: 0px;
      padding-bottom: 2px;
  }
  div.status {
      background: rgba(0, 0, 0, 0.4) !important;
      padding: 1px 4px 2px 4px;
      border-radius: 2px;
      margin-left: 7px;
  }
  span {
      font-size: 16px;
      margin: 6px 7px 6px 5px;
      background: rgba(255, 255, 255, 0.3);
      color: white;
      /* border-radius: 25px; */
      /* border: 2px solid var(--mainColor); */
      padding: 2px;
      display: flex;
      align-items: center;
      justify-content: center;
  }
  span:hover {
      background: rgba(255, 255, 255, 0.4);
      cursor: pointer;
  }
</style>