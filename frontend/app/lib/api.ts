const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function getTransactions() {
  const res = await fetch(`${API_URL}/transactions`);
  if (!res.ok) throw new Error("Errore nel recupero transazioni");
  return res.json();
}
