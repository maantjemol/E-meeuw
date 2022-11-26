let email_list = document.getElementById("InboxContent");
let loadButton = document.getElementById("loadButton");

const addEmail = (subject, content) => {
  var entry = document.createElement("details");

  var summary = document.createElement("summary");
  summary.innerText = subject;
  entry.appendChild(summary);
  entry.appendChild(document.createTextNode(content));

  email_list.appendChild(entry);
};

async function getEmails() {
  let headersList = {
    Accept: "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Content-Type": "application/json",
  };

  let bodyContent = JSON.stringify({
    uid: document.cookie.split("id=")[1],
  });

  let response = await fetch("https://localhost:1115/api/getsendmail", {
    method: "POST",
    body: bodyContent,
    headers: headersList,
  });

  let data = await response.json();
  console.log(data);
  if (data.success) {
    email_list.innerHTML = "";
    for (let i = 0; i < data.emails.length; i++) {
      const email = data.emails[i];
      console.log(email);
      addEmail(email.subject, email.contents);
    }
  }
}

loadButton.addEventListener("click", async function (e) {
  await getEmails(e);
});

document.addEventListener("DOMContentLoaded", async function () {
  await getEmails();
});
