import test from "node:test";
import assert from "node:assert/strict";
import { readdir, readFile, stat } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
const ROOT = dirname(fileURLToPath(import.meta.url));
const FORBIDDEN = [/17a73ce3-6eaf-4434-88ae-675fc0eeef0f/, /primedev-pm\.up\.railway\.app/, /mempalace/i, /C:\\Users/, /\/Users\/PC\//, /C--Users-PC/];
async function walk(d, out = []) { for (const n of await readdir(d)) { if (n === "node_modules" || n === ".git") continue; const p = join(d, n); const s = await stat(p); if (s.isDirectory()) await walk(p, out); else out.push(p); } return out; }
test("dev-team pack ships no personal secrets/paths", async () => {
  for (const f of await walk(ROOT)) {
    if (f.endsWith("scrub-check.test.mjs")) continue;
    const txt = await readFile(f, "utf8").catch(() => "");
    for (const re of FORBIDDEN) assert.ok(!re.test(txt), `${re} found in ${f}`);
  }
});
