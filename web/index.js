import { message, updateHeader } from "./components/UI.js";

let bar = document.getElementById("prompt");
let roomId = document.getElementById("roomId");
const btn = document.getElementById("send");
const chat = document.getElementById("chat");
const stats = document.getElementById("stats");
const username = document.getElementById("username");
let source = null;

// alert

const url = ["localhost", "127.0.0.1"].includes(location.hostname)
  ? "http://localhost:8000"
  : "/api";

function connect() {
  const rid = roomId.value === "" ? 1 : roomId.value;

  if (!username.value) {
    // alert("Provide a username first");
    return;
  }

  if (source) source.close();

  source = new EventSource(
    `${url}/room/${rid}/messages?user_name=${encodeURIComponent(username.value)}`,
  );
  source.addEventListener("message", (event) => {
    try {
      const data = JSON.parse(event.data);
      // Append the message text to your chat textarea

      if (data.msg && data.user_name) {
        const m = `${data.user_name} : ${data.msg}`;
        const current_user = data.user_name == username.value;
        chat.append(message(m, current_user));
      }
    } catch (err) {
      // Fallback if the data is a plain string

      chat.append(message(event.data));
    }
  });

  // source.onmessage = (event) => {};
  source.addEventListener("presence", (event) => {
    try {
      const data = JSON.parse(event.data);
      const { count, members } = data;
      stats.replaceChildren(updateHeader({ count, members }));
    } catch (err) {}
  });
}

setInterval(async () => {
  try {
    const resp = await fetch(
      `${url}/room/${roomId.value == "" ? 1 : roomId.value}/check_presence`,
    ).then((data) => data.json());
    console.log(resp);
    const { members, count } = { ...resp };
    // console.log(count);
    stats.replaceChildren(updateHeader({ count, members }));
  } catch (err) {
    console.log(err);
  }
}, 3000);

setInterval(async () => {
  await fetch(
    `${url}/room/${roomId.value == "" ? 1 : roomId.value}/heartbead?user_name=${encodeURIComponent(username.value)}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    },
  );
}, 2000);

roomId.addEventListener("change", connect);
username.addEventListener("change", connect);
connect();
async function send_msg(msg) {
  const resp = await fetch(
    `${url}/room/${roomId.value}/messages?msg=${String(msg)}&user_id=${1}&user_name=${username.value}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    },
  ).then((data) => data.json());
}

btn.addEventListener("click", async () => {
  const msg = bar.value;
  await send_msg(msg);
});

bar.addEventListener("change", async (e) => {
  try {
    if (e.target.value == null) {
      // alert("Message must not be empty");
      return;
    }
    await send_msg(e.target.value);
  } catch (err) {
    console.log(err);
  }
  bar.value = "";
});
