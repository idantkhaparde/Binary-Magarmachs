<main class="flex flex-col font-mono w-full h-full bg-black">
  <div class="h-screen bg-[url(/magarnobg.webp)] bg-no-repeat bg-center bg-black">
    <nav class="text-2xl flex w-full h-[10vh] justify-around p-6 font-medium">
      <a href="">Home</a>
      <a href="">How it works?</a>
      <a href="">Create Wallet</a>
      <a href="">Lookup</a>
      <a href="">Sign</a>
      <a href="">Create Wallet</a>
    </nav>
    <p class="text-4xl text-center italic mx-auto mt-64 w-full py-6 bg-neutral/20 border-y-2 border-neutral">guard your documents with our magarmach</p>
  </div>
  <div class="com-div">
  </div>
  <div class="com-div flex flex-col cw" >
    <div class="m-auto gap-8 flex flex-col">
      <p class="text-5xl text-white text-center mb-8">Create Wallet</p>
      <input type="text" placeholder="Username" class="cw-inn" ref={uname} />
      <input type="text" placeholder="Name" class="cw-inn" ref={name} />
      <input type="text" placeholder="Phone No." class="cw-inn" ref={pno} />
      <input type="text" placeholder="Sign URL" class="cw-inn" ref={sig} />
      <button class="btn btn-lg border border-white" on:click={createwallet}>Create Wallet</button>
    </div>
  </div>

  <div class="com-div flex flex-col cw" >
    <div class="m-auto gap-8 flex flex-col">
      <p class="text-5xl text-white text-center mb-8">Lookup</p>
      <input type="text" placeholder="Tx" class="cw-inn" ref={tx} />
      <button class="btn btn-lg border border-white" on:click={lookup}>Lookup</button>
    </div>
  </div>
</main>

<script>

  let uname, name, pno, sig;


  const createwallet = () => {
    const obj = {username: uname, name: name, phone: pno, sign: sig};

    fetch(`127.0.0.1:8080/createwallet?data=${obj}`)
      .then(response => response.json())
      .then((data) => alert(`here is your wallet save it somewhere safe: ${data}`))
  }

  const lookup = () => {

    fetch(`127.0.0.1:8080/createwallet?tx=${xt}`)
      .then(response => response.json())
      .then((data) => alert(`here is your wallet save it somewhere safe: ${data}`))
  }
</script>

<style>
.com-div {
  @apply border-t-2 border-neutral h-screen p-6;
}

.cw > * {
  @apply w-[50vh];
}

.cw-inn {
  @apply input input-lg input-bordered w-full;
}
</style>
