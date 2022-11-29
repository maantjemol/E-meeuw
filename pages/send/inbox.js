let email_list = document.getElementById("InboxContent");
let loadButton = document.getElementById("loadButton");

const addEmail = (subject, content, toemail) => {
  var entry = document.createElement("details");
  content = content.replaceAll("\n", "<br>");
  var summary = document.createElement("summary");
  var emailtext = document.createElement("p");
  emailtext.innerHTML = content;
  summary.innerText = `${subject} | ${toemail}`;
  entry.appendChild(summary);
  entry.appendChild(emailtext);
  email_list.appendChild(entry);
};

let logout_button = document.getElementById("logout");
async function logout() {
  document.cookie = "id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  window.setTimeout(function () {
    document.location.href = "/inbox/inbox.html";
  }, 500);
}
logout_button.addEventListener("click", async function (e) {
  await logout(e);
});

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
      addEmail(email.subject, email.contents, email.to_email);
    }
  }
}

loadButton.addEventListener("click", async function (e) {
  await getEmails(e);
});

document.addEventListener("DOMContentLoaded", async function () {
  await getEmails();
});
