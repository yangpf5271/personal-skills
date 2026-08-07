const baseUrl = process.env.CCR_BASE_URL || "http://127.0.0.1:3456";
const apiKey =
  process.env.CCR_API_KEY ||
  process.env.ANTHROPIC_AUTH_TOKEN ||
  process.env.OPENAI_API_KEY;
const traceKey = process.argv[2];

if (!apiKey) {
  throw new Error(
    "Missing CCR proxy API key. Caller should reuse the same key currently used for model calls and inject it as CCR_API_KEY, or resolve it from CCR_API_KEY, ANTHROPIC_AUTH_TOKEN, OPENAI_API_KEY, or Codex experimental_bearer_token."
  );
}

if (!traceKey) {
  console.error("Usage: node ./get-trace.mjs <traceKey>");
  process.exit(1);
}

const res = await fetch(`${baseUrl}/api/trace/${encodeURIComponent(traceKey)}`, {
  headers: { "X-API-Key": apiKey },
});

if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
console.log(JSON.stringify(await res.json(), null, 2));
