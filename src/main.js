const nav = document.querySelector("[data-nav]");
const toggle = document.querySelector("[data-menu]");

if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
  });
}

const year = document.querySelector("[data-year]");
if (year) {
  year.textContent = String(new Date().getFullYear());
}

const form = document.querySelector("[data-contact-form]");
if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const status = form.querySelector("[data-form-status]");
    const submit = form.querySelector("button[type='submit']");
    const data = new FormData(form);

    if (data.get("website")) {
      form.reset();
      return;
    }

    submit.disabled = true;
    status.className = "form-status";
    status.hidden = true;

    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: data,
        headers: { Accept: "application/json" },
      });

      const contentType = response.headers.get("content-type") || "";
      if (!response.ok || !contentType.includes("application/json")) {
        throw new Error("send-failed");
      }

      const payload = await response.json();
      if (!payload.ok) {
        throw new Error("send-failed");
      }

      form.reset();
      status.textContent =
        "Danke. Ihre Nachricht ist angekommen. Wir melden uns in der Regel innert eines Werktags.";
      status.className = "form-status ok";
      status.hidden = false;
    } catch {
      status.textContent =
        "Der Versand ist lokal nicht aktiv. Schreiben Sie uns direkt an nicole.straehl@learnbox.ch oder rufen Sie +41 79 323 56 23 an.";
      status.className = "form-status err";
      status.hidden = false;
    } finally {
      submit.disabled = false;
    }
  });
}
