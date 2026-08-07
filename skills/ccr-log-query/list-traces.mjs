const baseUrl = process.env.CCR_BASE_URL || "http://127.0.0.1:3456";
const apiKey =
  process.env.CCR_API_KEY ||
  process.env.ANTHROPIC_AUTH_TOKEN ||
  process.env.OPENAI_API_KEY;

if (!apiKey) {
  throw new Error(
    "Missing CCR proxy API key. Caller should reuse the same key currently used for model calls and inject it as CCR_API_KEY, or resolve it from CCR_API_KEY, ANTHROPIC_AUTH_TOKEN, OPENAI_API_KEY, or Codex experimental_bearer_token."
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
