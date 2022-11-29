let text = document.getElementById("addText");
let count = 0;

document.getElementById("addButton").addEventListener("click", function () {
  count++;
  text.innerHTML = count;
});

let headersList = {
  Accept: "*/*",
  "User-Agent": "Thunder Client (https://www.thunderclient.com)",
  "Content-Type": "application/json",
};

let bodyContent = JSON.stringify({
  username: "maantje",
  password: "lolhaha",
});

fetch("/api/login", {
  method: "POST",
  body: bodyContent,
  headers: headersList,
})
  .then((response) => response.text())
  .then((data) => {
    console.log(data);
  });
