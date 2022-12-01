const form = document.getElementById("email_form");
let subject_text = document.getElementById("subject");
let recp_email_text = document.getElementById("recipient");
let content_text = document.getElementById("content");
let success_text = document.getElementById("success");
let error_text = document.getElementById("error");
let butt = document.getElementById("submit_button");

form.addEventListener("submit", async function (e) {
  await submitForm(e);
  butt.disabled = true;

  let headersList = {
    Accept: "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Content-Type": "application/json",
  };

  let bodyContent = JSON.stringify({
    uid: document.cookie.split("id=")[1],
    to_email: recp_email_text.value,
    subject: subject_text.value,
    contents: content_text.value,
  });

  let response = await fetch("/api/sendmail", {
    method: "POST",
    body: bodyContent,
    headers: headersList,
  });

  let data = await response.json();
  if (data.success) {
    butt.disabled = false;
    success_text.style.display = "block";
    error_text.style.display = "none";
  } else {
    butt.disabled = false;
    success_text.style.display = "none";
    error_text.style.display = "block";
  }
  console.log(data);
});

async function submitForm(e) {
  e.preventDefault();
}
