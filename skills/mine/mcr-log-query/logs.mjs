import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

// node ./logs.mjs — list log files; node ./logs.mjs <path> — read one log file.
const baseUrl = process.env.MCR_BASE_URL || "http://127.0.0.1:3456";
const target = process.argv[2];

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

const url = target
  ? `${baseUrl}/api/logs?file=${encodeURIComponent(target)}`
  : `${baseUrl}/api/logs/files`;

const res = await fetch(url, { headers: { "X-API-Key": apiKey } });

if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
console.log(JSON.stringify(await res.json(), null, 2));
