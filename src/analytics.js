import { GA4_PROPERTY_ID, getMeasurementId, isAnalyticsEnabled } from "./ga-config.js";

function gtag(...args) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push(args);
}

export function trackEvent(eventName, params = {}) {
  if (!isAnalyticsEnabled() || typeof window.gtag !== "function") return;
  window.gtag("event", eventName, {
    ga4_property_id: GA4_PROPERTY_ID,
    ...params,
  });
}

function labelOf(el) {
  const text = (el.getAttribute("aria-label") || el.textContent || "").replace(/\s+/g, " ").trim();
  return text.slice(0, 120);
}

function classifyLink(anchor) {
  const href = anchor.getAttribute("href") || "";
  const params = {
    link_url: href,
    link_text: labelOf(anchor),
    page_path: window.location.pathname,
  };

  if (href.startsWith("tel:")) {
    return ["contact_call", { ...params, phone_number: href.slice(4) }];
  }
  if (href.startsWith("mailto:")) {
    return ["contact_email", params];
  }
  if (anchor.classList.contains("nav-cta") || anchor.classList.contains("btn-primary")) {
    return ["cta_click", { ...params, cta_type: "primary" }];
  }
  if (anchor.classList.contains("btn-ghost")) {
    return ["cta_click", { ...params, cta_type: "secondary" }];
  }
  if (anchor.classList.contains("post-link") || anchor.closest(".posts")) {
    return ["select_content", { ...params, content_type: "blog" }];
  }
  if (anchor.closest(".nav-links")) {
    return ["navigation", { ...params, nav_area: "header" }];
  }
  if (anchor.closest(".site-footer")) {
    return ["navigation", { ...params, nav_area: "footer" }];
  }
  if (anchor.closest(".process-track")) {
    return ["navigation", { ...params, nav_area: "process" }];
  }
  if (href.startsWith("#")) {
    return ["navigation", { ...params, nav_area: "anchor" }];
  }
  if (href === "/" || href.endsWith(".html")) {
    return ["navigation", { ...params, nav_area: "internal" }];
  }
  if (href.startsWith("http")) {
    return ["click", { ...params, outbound: true }];
  }
  return ["click", params];
}

function bindInteractionTracking() {
  document.addEventListener(
    "click",
    (event) => {
      const anchor = event.target instanceof Element ? event.target.closest("a[href]") : null;
      if (!anchor || anchor.getAttribute("href")?.startsWith("javascript:")) return;
      const [name, params] = classifyLink(anchor);
      trackEvent(name, params);
    },
    { capture: true }
  );

  const menu = document.querySelector("[data-menu]");
  if (menu) {
    menu.addEventListener("click", () => {
      const open = menu.getAttribute("aria-expanded") === "true";
      trackEvent("menu_toggle", { menu_state: open ? "close" : "open" });
    });
  }

  const form = document.querySelector("[data-contact-form]");
  if (form) {
    form.addEventListener(
      "focusin",
      () => {
        if (!form.dataset.gaStarted) {
          form.dataset.gaStarted = "1";
          trackEvent("form_start", { form_name: "contact" });
        }
      },
      { once: true }
    );
  }
}

function loadGtag() {
  const measurementId = getMeasurementId();
  window.gtag = gtag;

  gtag("consent", "default", {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    analytics_storage: "granted",
  });

  gtag("js", new Date());
  gtag("config", measurementId, {
    send_page_view: true,
    cookie_flags: "SameSite=None;Secure",
  });
  gtag("set", "user_properties", { ga4_property_id: GA4_PROPERTY_ID });

  const script = document.createElement("script");
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`;
  script.onload = () => {
    trackEvent("page_ready", {
      page_title: document.title,
      page_location: window.location.href,
    });
  };
  document.head.appendChild(script);
}

export function initAnalytics() {
  if (!isAnalyticsEnabled()) return;
  loadGtag();
  bindInteractionTracking();
}