import { useState } from "react";
import { bootstrap } from "../lib/api";

export default function Home() {
  const [orgName, setOrgName] = useState("Didone World");
  const [orgSlug, setOrgSlug] = useState("didoneworld");
  const [apiKey, setApiKey] = useState<string | null>(null);

  async function handleBootstrap() {
    const res = await bootstrap(orgName, orgSlug);
    setApiKey(res.api_key);
  }

  return (
    <main style={{ padding: 40, fontFamily: "sans-serif" }}>
      <h1>Agent DID Web App</h1>

      <section style={{ marginTop: 20 }}>
        <h2>Bootstrap Organization</h2>
        <input
          value={orgName}
          onChange={(e) => setOrgName(e.target.value)}
          placeholder="Organization Name"
        />
        <br />
        <input
          value={orgSlug}
          onChange={(e) => setOrgSlug(e.target.value)}
          placeholder="Organization Slug"
        />
        <br />
        <button onClick={handleBootstrap}>Create Org</button>

        {apiKey && (
          <div style={{ marginTop: 20 }}>
            <h3>API Key</h3>
            <code>{apiKey}</code>
          </div>
        )}
      </section>
    </main>
  );
}
