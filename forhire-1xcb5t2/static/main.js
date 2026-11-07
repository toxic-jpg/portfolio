// Contact form: client-side validation + fetch POST to /api/contact.
// Renders all server text via textContent / createElement — never innerHTML —
// so a malicious submission can't inject markup.
(() => {
  "use strict";

  const form = document.getElementById("contact-form");
  const status = document.getElementById("form-status");
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
  if (!form) return;

  const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$/;
  const FIELDS = ["name", "email", "message"];

  const fieldWrap = (input) => input.closest(".field");

  const setError = (name, msg) => {
    const input = form.elements[name];
    const slot = form.querySelector(`[data-err="${name}"]`);
    if (!input || !slot) return;
    slot.textContent = msg || "";
    fieldWrap(input).classList.toggle("invalid", Boolean(msg));
    input.setAttribute("aria-invalid", msg ? "true" : "false");
  };

  const clearErrors = () => FIELDS.forEach((f) => setError(f, ""));

  const validate = () => {
    clearErrors();
    let ok = true;
    const data = {};

    for (const name of FIELDS) {
      const value = form.elements[name].value.trim();
      data[name] = value;
      if (!value) {
        setError(name, "This field is required.");
        ok = false;
      }
    }

    if (data.email && !EMAIL_RE.test(data.email)) {
      setError("email", "That email address doesn't look right.");
      ok = false;
    }

    return { ok, data };
  };

  // Live-clear a field's error once the user starts fixing it.
  form.addEventListener("input", (ev) => {
    if (ev.target.name) setError(ev.target.name, "");
  });

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    status.textContent = "";
    status.className = "form-status";

    const { ok, data } = validate();
    if (!ok) {
      status.textContent = "Please fix the highlighted fields.";
      status.classList.add("fail");
      return;
    }

    const submit = form.querySelector('button[type="submit"]');
    submit.disabled = true;
    submit.textContent = "Sending…";

    try {
      const res = await fetch(form.action || "/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data),
      });
      const body = await res.json().catch(() => ({}));

      if (res.ok && body.ok) {
        form.reset();
        clearErrors();
        status.textContent = body.message || "Sent. Thanks!";
        status.classList.add("ok");
      } else {
        for (const [field, msg] of Object.entries(body.errors || {})) {
          setError(field, msg);
        }
        status.textContent = body.message || "Something went wrong — please try again.";
        status.classList.add("fail");
      }
    } catch (err) {
      status.textContent = "Network error — check your connection and retry.";
      status.classList.add("fail");
    } finally {
      submit.disabled = false;
      submit.textContent = "Send";
    }
  });
})();