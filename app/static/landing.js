// Landing page behaviour: poll the control-plane health endpoint and reflect
// it in the nav status pill. Kept independent of the admin console (app.js).
(function () {
  "use strict";

  var dot = document.getElementById("api-dot");
  var text = document.getElementById("api-status-text");
  var pill = document.getElementById("api-status");
  if (!dot || !text) return;

  function set(state, label) {
    pill.dataset.state = state;
    text.textContent = label;
  }

  async function check() {
    try {
      var res = await fetch("/health", { headers: { Accept: "application/json" } });
      if (!res.ok) throw new Error("status " + res.status);
      var body = await res.json().catch(function () { return {}; });
      var ok = (body && (body.status === "ok" || body.status === "healthy")) || res.ok;
      set(ok ? "ok" : "degraded", ok ? "Operational" : "Degraded");
    } catch (e) {
      set("down", "Offline");
    }
  }

  check();
  setInterval(check, 30000);

  // Smooth-scroll for in-page anchor links.
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (ev) {
      var id = a.getAttribute("href").slice(1);
      var el = id && document.getElementById(id);
      if (!el) return;
      ev.preventDefault();
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
})();
