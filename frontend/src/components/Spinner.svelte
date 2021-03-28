<script>

</script>

<div>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
</div>

<h1>😉 not bad, eh</h1>

<style>
  div {
    width: 4rem;
    height: 3rem;
    display: flex;
    align-items: center;


    /* for display purposes */
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }

  span {
    display: flex;
    flex-grow: 1;
    height: 100%;
    background-color: black;
    margin-right: 2px;
    animation: loading ease-in-out 0.5s infinite alternate;
  }

  span:last-child {
    margin: 0px;
  }

  span:nth-child(1) {animation-delay: 0.0s;}
  span:nth-child(2) {animation-delay: 0.2s;}
  span:nth-child(3) {animation-delay: 0.4s;}
  span:nth-child(4) {animation-delay: 0.6s;}
  span:nth-child(5) {animation-delay: 0.8s;}

  @keyframes loading {
    from {height: 100%;}
    to {height: 30%;}
  }

  h1 {
    font-size: 24px;

    /* for display purposes */
    position: fixed;
    left: 50%;
    top: 60%;
    opacity: 0;
    transform: translate(-50%, -50%);
    animation: text ease 2s forwards;
    animation-delay: 3s;
  }

  @keyframes text {
    from {opacity: 0;}
    to {opacity: 1;}
  }

</style>