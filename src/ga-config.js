/** GA4 Property-ID (Admin → Property-Einstellungen). */
export const GA4_PROPERTY_ID = "443927742";

const raw = import.meta.env.VITE_GA4_MEASUREMENT_ID || "G-443927742";

/** Mess-ID aus GA4 → Datenstreams (Format G-…). Über .env überschreibbar. */
export function getMeasurementId() {
  const id = String(raw).trim();
  if (/^(G-|GT-|AW-)/.test(id)) return id;
  if (/^\d+$/.test(id)) return `G-${id}`;
  return id;
}

export function isAnalyticsEnabled() {
  return import.meta.env.PROD || import.meta.env.VITE_GA_ENABLE_DEV === "true";
}