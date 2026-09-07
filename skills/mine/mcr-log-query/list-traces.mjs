import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const baseUrl = process.env.MCR_BASE_URL || "http://127.0.0.1:3456";

function resolveConfigApiKey() {
  const candidates = [
    process.env.MCR_CONFIG_PATH,
    join(homedir(), ".mcr-router", "config.json"),
  ].filter(Boolean);
  for (const path of candidates) {
    try {
      const apiKey = JSON.parse(readFileSync(path, "utf8"))?.APIKEY;
      if (apiKey) return apiKey;
    } catch {}
  }
  return undefined;
}

const apiKey =
  process.env.MCR_API_KEY ||
  process.env.ANTHROPIC_AUTH_TOKEN ||
  process.env.OPENAI_API_KEY ||
  resolveConfigApiKey();

if (!apiKey) {
  throw new Error(
    "Missing MCR proxy API key. Inject MCR_API_KEY, or let the script fall back to ANTHROPIC_AUTH_TOKEN, OPENAI_API_KEY, or the APIKEY field in ~/.mcr-router/config.json (override with MCR_CONFIG_PATH)."
  );
}

const params = new URLSearchParams({
  page: process.env.PAGE || "1",
  pageSize: process.env.PAGE_SIZE || "20",
});

for (const key of ["provider", "model", "protocol", "status"]) {
  const value = process.env[key.toUpperCase()];
  if (value) params.set(key, value);
}

const res = await fetch(`${baseUrl}/api/traces?${params}`, {
  headers: { "X-API-Key": apiKey },
});

if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
console.log(JSON.stringify(await res.json(), null, 2));
