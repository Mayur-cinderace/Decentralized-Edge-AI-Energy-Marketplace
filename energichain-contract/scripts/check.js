async function main() {
  const provider = new ethers.JsonRpcProvider("http://127.0.0.1:7545");
  const block = await provider.getBlockNumber();
  console.log("Connected! Current block:", block);
}
main();