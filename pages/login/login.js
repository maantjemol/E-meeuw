email_text = document.getElementById("email");
password_text = document.getElementById("password");

const checkInputs = () => {};

// button.onclick = async () => {};

async function submitForm(e) {
  e.preventDefault();
  const submit_button = document.getElementById("submit_button");
  submit_button.disabled = true;

  let headersList = {
    "Content-Type": "application/json",
  };

  let bodyContent = JSON.stringify({
    username: email_text.value,
    password: password_text.value,
  });

  let response = await fetch("/api/login", {
    method: "POST",
    body: bodyContent,
    headers: headersList,
  });

  if (response) {
    submit_button.disabled = false;
  }

  if (response.status === 200) {
    let data = await response.json();

    if (data.error) {
      console.log(data.error);
      return;
    }

    document.cookie = `id=${data.cookie};path=/`;
    // setTimeout((document.location.href = "/inbox/inbox.html"), 1000);
    window.setTimeout(function () {
      document.location.href = "/inbox/inbox.html";
    }, 1000);
  }
}

const form = document.getElementById("formmmm");

form.addEventListener("submit", async function (e) {
  await submitForm(e);
});
