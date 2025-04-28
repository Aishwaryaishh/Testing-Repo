let count = 0;

function incrementCounter() {
  count++;
  const message = `You clicked ${count} time${count === 1 ? "" : "s"}.`;
  document.getElementById("clickCount").innerText = message;
}
