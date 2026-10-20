// BESYN — kleine, afhankelijkheidsvrije interacties (geen cookies, geen trackers)
// Wordt in <head> geladen zodat de "js"-klasse er is vóór de eerste weergave.
document.documentElement.classList.add("js");
document.addEventListener("DOMContentLoaded", function () {

  // Mobiel menu
  var toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Menu sluiten" : "Menu openen");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  // Onderwerp vooraf invullen via ?onderwerp=coaching|mediation|teamcoaching
  var select = document.getElementById("onderwerp");
  if (select && window.URLSearchParams) {
    var o = (new URLSearchParams(window.location.search).get("onderwerp") || "").replace(/[^a-z]/g, "");
    if (o && select.querySelector('option[value="' + o + '"]')) select.value = o;
  }

  // Ontbrekende foto's netjes verbergen (het vlak blijft in huisstijlkleur staan)
  var imgs = document.querySelectorAll(".media img, .drop img");
  function hide(img) { if (img.parentNode) img.parentNode.classList.add("is-empty"); }
  for (var m = 0; m < imgs.length; m++) {
    (function (img) {
      if (img.complete && img.naturalWidth === 0) hide(img);
      img.addEventListener("error", function () { hide(img); });
    })(imgs[m]);
  }

  // Herkomst van advertenties (SEA) zonder cookies: komt iemand binnen via een advertentie
  // (Google Ads voegt ?gclid=… toe, of utm-parameters), dan gaan die parameters mee naar het
  // contactformulier en vult het verborgen veld "herkomst" zich, bijv. "Google Ads · naam-campagne".
  if (window.URLSearchParams && window.URL) {
    var params = new URLSearchParams(window.location.search);
    var keys = ["gclid", "utm_source", "utm_medium", "utm_campaign"];
    var carry = [];
    for (var n = 0; n < keys.length; n++) {
      var val = params.get(keys[n]);
      if (val) carry.push([keys[n], val.slice(0, 100)]);
    }
    if (carry.length) {
      var contactLinks = document.querySelectorAll('a[href^="/contact/"]');
      for (var c = 0; c < contactLinks.length; c++) {
        var u = new URL(contactLinks[c].getAttribute("href"), window.location.origin);
        for (var d = 0; d < carry.length; d++) u.searchParams.set(carry[d][0], carry[d][1]);
        contactLinks[c].setAttribute("href", u.pathname + u.search + u.hash);
      }
      var herkomst = document.getElementById("herkomst");
      if (herkomst) {
        var bron = params.get("gclid") ? "Google Ads" : (params.get("utm_source") || "");
        var extra = [params.get("utm_medium"), params.get("utm_campaign")].filter(Boolean).join(" / ");
        herkomst.value = (bron + (extra ? " · " + extra : "")).replace(/[^\w .·/-]/g, "").slice(0, 120) || "website";
      }
    }
  }

  // Jaartal in footer
  var y = document.querySelectorAll("[data-year]");
  for (var i = 0; i < y.length; i++) y[i].textContent = new Date().getFullYear();

  // Rustige fade-in bij scrollen
  var items = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    for (var j = 0; j < items.length; j++) items[j].classList.add("is-visible");
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  for (var k = 0; k < items.length; k++) io.observe(items[k]);
});
