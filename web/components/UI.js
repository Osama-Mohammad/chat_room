function h(tag, props = {}, ...children) {
  const el = document.createElement(tag);
  Object.assign(el, props);
  el.append(...children);
  return el;
}

export function message(msg, shift_RL) {
  const date = new Date();
  return h(
    "div",
    { className: shift_RL ? "message mine" : "message" },
    ...[
      h("p", { className: "msg-text", textContent: msg }),
      h("span", {
        className: "msg-time",
        textContent: date.toLocaleTimeString(),
      }),
    ],
  );
}

export function updateHeader({ count, members }) {
  return h(
    "div",
    { className: "header" },
    h("span", {
      className: "header-count",
      textContent: `🟢
       Online: ${count}`,
    }),
    h("span", {
      className: "header-members",
      textContent: (members ?? []).join(", "),
    }),
  );
}
