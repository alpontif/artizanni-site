/* artizanni.com — every enquiry ends in a prefilled WhatsApp chat (or email) carrying a reference number.
   Nothing is sent to a server: the visitor sends the message themselves. Hand-written; no build step. */
(() => {
  "use strict";
  const A = window.ART || {};
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const LS = {
    get(k, d) { try { const v = localStorage.getItem("art." + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem("art." + k, JSON.stringify(v)); } catch (e) { /* private mode */ } }
  };
  const toast = msg => { const t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); t.textContent = msg; document.body.appendChild(t); setTimeout(() => t.remove(), 2600); };

  /* ---------------------------------------------------------- navigation */
  const mb = $(".menu-btn"), nav = $("#nav");
  if (mb && nav) {
    mb.addEventListener("click", () => { const o = nav.classList.toggle("open"); mb.setAttribute("aria-expanded", o); });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); mb.setAttribute("aria-expanded", "false"); mb.focus(); } });
  }

  /* ---------------------------------------------------------- reference numbers + WhatsApp */
  const pad = n => String(n).padStart(2, "0");
  function makeRef(type) {
    const d = new Date(), ch = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
    let r = ""; for (let i = 0; i < 4; i++) r += ch[Math.floor(Math.random() * ch.length)];
    return `ART-${type}-${String(d.getFullYear()).slice(2)}${pad(d.getMonth() + 1)}${pad(d.getDate())}-${r}`;
  }
  const waUrl = text => `https://wa.me/${A.wa}?text=${encodeURIComponent(text)}`;
  const mailUrl = (subj, text) => `mailto:${A.email}?subject=${encodeURIComponent(subj)}&body=${encodeURIComponent(text)}`;

  // plain WhatsApp links get a page-aware opening line
  $$("[data-wa-quick]").forEach(a => {
    const topic = a.dataset.waQuick || document.title.split("|")[0].trim();
    a.href = waUrl(`Hello Artizanni, I'm contacting you from your website (${topic}).`);
  });

  /* ---------------------------------------------------------- enquiry forms → message */
  function readForm(form) {
    const lines = [], seen = new Set();
    $$("[name]", form).forEach(el => {
      const n = el.name; if (seen.has(n) || el.type === "submit" || el.dataset.skip != null) return;
      let v;
      if (el.type === "radio") { seen.add(n); const c = $(`[name="${n}"]:checked`, form); v = c ? c.value : ""; }
      else if (el.type === "checkbox") { seen.add(n); v = $$(`[name="${n}"]:checked`, form).map(c => c.value).join(", "); }
      else { seen.add(n); v = el.value.trim(); }
      if (!v) return;
      const box = el.closest("[data-label]"); const lab = (box && box.dataset.label) || el.dataset.label || n;
      lines.push([lab, v]);
    });
    return lines;
  }
  $$("form[data-wa]").forEach(form => {
    const out = $("[data-out]", form.parentElement) || $("[data-out]");
    form.addEventListener("submit", ev => {
      ev.preventDefault();
      const bad = $$("[data-need]", form).find(box => !$$("input:checked", box).length);
      $$(".err", form).forEach(e => e.remove());
      if (bad) { const e = document.createElement("p"); e.className = "err"; e.textContent = "Please choose an option here."; bad.appendChild(e); bad.scrollIntoView({ behavior: "smooth", block: "center" }); return; }
      if (!form.reportValidity()) return;
      const type = form.dataset.wa, title = form.dataset.title || "Enquiry";
      const ref = makeRef(type), lines = readForm(form);
      const text = [`Hello Artizanni. ${form.dataset.intro || "I'd like to talk to you about a project."}`, `Reference: ${ref}`, "",
        ...lines.map(([k, v]) => `${k}: ${v}`), "", "(Sent from artizanni.com)"].join("\n");
      const list = LS.get("requests", []);
      list.unshift({ ref, title, date: new Date().toISOString(), text }); LS.set("requests", list.slice(0, 30));
      out.hidden = false;
      out.innerHTML = `<p class="eyebrow">Ready to send</p>
        <h3>Your reference is <span class="ref">${esc(ref)}</span></h3>
        <p class="muted small">Nothing has been sent yet. Tap a button below to send this message from your own WhatsApp or email. Quote the reference in any follow-up.</p>
        <div class="summary" tabindex="0">${esc(text)}</div>
        <div class="btns" style="margin-top:16px">
          <a class="btn btn-wa" href="${waUrl(text)}" target="_blank" rel="noopener">${A.waIcon}Send on WhatsApp</a>
          <a class="btn btn-line" href="${mailUrl(`${title} ${ref}`, text)}">Send by email</a>
          <button class="btn btn-line" type="button" data-copy>Copy text</button>
        </div>`;
      $("[data-copy]", out).onclick = () => navigator.clipboard && navigator.clipboard.writeText(text).then(() => toast("Copied"));
      out.scrollIntoView({ behavior: "smooth", block: "start" });
      if (window.gtag) window.gtag("event", "generate_lead", { form: title });
    });
  });

  // requests saved on this device
  const rq = $("[data-requests]");
  if (rq) {
    const list = LS.get("requests", []);
    rq.innerHTML = list.length ? list.map(r => `<div class="req"><div><span class="ref">${esc(r.ref)}</span><br><b>${esc(r.title)}</b>
      <span class="muted small"> · ${new Date(r.date).toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" })}</span></div>
      <a class="btn btn-wa btn-sm" href="${waUrl(r.text)}" target="_blank" rel="noopener">${A.waIcon}Open in WhatsApp</a></div>`).join("")
      : `<p class="muted">No requests on this device yet. <a href="${A.root}start/">Start a project</a>.</p>`;
  }

  /* ---------------------------------------------------------- register filter */
  const reg = $("[data-register]");
  if (reg) {
    $$("[data-filter]").forEach(b => b.addEventListener("click", () => {
      $$("[data-filter]").forEach(x => x.setAttribute("aria-pressed", x === b));
      const f = b.dataset.filter;
      $$("tbody tr", reg).forEach(tr => { tr.hidden = f !== "all" && tr.dataset.sector !== f; });
    }));
  }

  /* ---------------------------------------------------------- lightbox */
  const shots = $$("[data-lb]");
  if (shots.length && window.HTMLDialogElement) {
    const d = document.createElement("dialog"); d.className = "lb";
    d.innerHTML = `<img alt=""><p></p><button class="x" type="button" aria-label="Close">×</button><button class="nv pv" type="button" aria-label="Previous">‹</button><button class="nv nx" type="button" aria-label="Next">›</button>`;
    document.body.appendChild(d);
    let i = 0;
    const show = k => { i = (k + shots.length) % shots.length; const s = shots[i]; $("img", d).src = s.dataset.lb; $("img", d).alt = s.dataset.cap || ""; $("p", d).textContent = s.dataset.cap || ""; };
    shots.forEach((s, k) => s.addEventListener("click", () => { show(k); d.showModal(); }));
    $(".x", d).onclick = () => d.close(); $(".pv", d).onclick = () => show(i - 1); $(".nx", d).onclick = () => show(i + 1);
    d.addEventListener("click", e => { if (e.target === d) d.close(); });
    d.addEventListener("keydown", e => { if (e.key === "ArrowLeft") show(i - 1); if (e.key === "ArrowRight") show(i + 1); });
  }

  /* ---------------------------------------------------------- analytics only with consent (off unless an ID is configured) */
  document.addEventListener("click", e => {
    const a = e.target.closest("a[href]");
    if (!a || typeof gtag !== "function") return;
    const link_url = a.href;
    if (link_url.includes("wa.me") || link_url.includes("api.whatsapp.com")) gtag("event", "whatsapp_click", { link_url });
    else if (link_url.startsWith("mailto:")) gtag("event", "email_click", { link_url });
  });
  if (A.ga) {
    const load = () => {
      if (document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) return;
      const s = document.createElement("script"); s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + A.ga; document.head.appendChild(s);
      window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); }; gtag("js", new Date()); gtag("config", A.ga, { anonymize_ip: true });
    };
    const c = LS.get("consent", null);
    if (c === "yes") load();
    else if (c == null) {
      const b = document.createElement("div"); b.className = "cookie"; b.setAttribute("role", "dialog"); b.setAttribute("aria-label", "Analytics consent");
      b.innerHTML = `<b>May we count your visit?</b><br>We use Google Analytics only if you agree, to see which pages help people. <a href="${A.root}privacy/">Privacy notice</a>.<div class="btns"><button class="btn btn-ink btn-sm" data-y>Accept</button><button class="btn btn-line btn-sm" data-n>No thanks</button></div>`;
      document.body.appendChild(b);
      $("[data-y]", b).onclick = () => { LS.set("consent", "yes"); b.remove(); load(); };
      $("[data-n]", b).onclick = () => { LS.set("consent", "no"); b.remove(); };
    }
  }
})();
