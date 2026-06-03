import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const api = axios.create({
  baseURL: API_URL,
});

export async function getHealth() {
  const res = await api.get("/health");
  return res.data;
}

export async function bootstrap(orgName: string, orgSlug: string) {
  const res = await api.post("/v1/bootstrap", {
    organization_name: orgName,
    organization_slug: orgSlug,
    api_key_label: "web-app"
  });
  return res.data;
}

export async function listAgentRecords(apiKey: string) {
  const res = await api.get("/v1/agent-records", {
    headers: { "X-API-Key": apiKey }
  });
  return res.data;
}