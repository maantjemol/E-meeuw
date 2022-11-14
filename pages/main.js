let text = document.getElementById("addText");
let count = 0;

document.getElementById("addButton").addEventListener("click", function () {
  count++;
  text.innerHTML = count;
});
