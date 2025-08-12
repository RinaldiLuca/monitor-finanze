"use client";

import { useEffect, useState } from "react";
import { getTransactions } from "@/app/lib/api";

type Transaction = {
  id: number;
  external_id?: string | null;
  source_file_id?: string | null;
  hash_key: string;
  booking_dt?: string | null;
  value_dt: string;
  amount: number;
  description?: string | null;
  category?: string | null;
  account?: string | null;
  source: "api" | "pdf";
};

const fmtCurrency = new Intl.NumberFormat("it-IT", {
  style: "currency",
  currency: "EUR",
});

function fmtDate(s?: string | null) {
  if (!s) return "—";
  const d = new Date(s);
  return isNaN(d.getTime()) ? s : d.toLocaleDateString("it-IT");
}

export default function HomePage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const data: Transaction[] = await getTransactions();
        if (!alive) return;
        setTransactions(data);
      } catch (e: any) {
        if (!alive) return;
        setError(e?.message ?? "Errore nel recupero delle transazioni");
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
        <h1 className="text-3xl font-bold mb-4">💰 Transazioni</h1>
        <div className="text-sm text-gray-500">Caricamento…</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
        <h1 className="text-3xl font-bold mb-4">💰 Transazioni</h1>
        <div className="text-sm text-red-600">Errore: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">💰 Transazioni</h1>

        {transactions.length === 0 ? (
          <div className="bg-white rounded-xl shadow p-6 text-sm text-gray-500">
            Nessuna transazione trovata.
          </div>
        ) : (
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <table className="min-w-full">
              <thead>
                <tr className="bg-gray-100 text-gray-700">
                  <th className="px-4 py-3 text-left">Data operazione</th>
                  <th className="px-4 py-3 text-left">Data valuta</th>
                  <th className="px-4 py-3 text-left">Descrizione</th>
                  <th className="px-4 py-3 text-right">Importo</th>
                  <th className="px-4 py-3 text-left">Categoria</th>
                  <th className="px-4 py-3 text-left">Conto</th>
                  <th className="px-4 py-3 text-left">Origine</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((t, idx) => {
                  const positive = t.amount >= 0;
                  return (
                    <tr
                      key={t.id}
                      className={`${
                        idx % 2 === 0 ? "bg-white" : "bg-gray-50"
                      } hover:bg-gray-100 transition`}
                    >
                      <td className="px-4 py-3">{fmtDate(t.booking_dt)}</td>
                      <td className="px-4 py-3">{fmtDate(t.value_dt)}</td>
                      <td className="px-4 py-3">{t.description ?? "—"}</td>
                      <td
                        className={`px-4 py-3 text-right font-medium ${
                          positive ? "text-green-600" : "text-red-500"
                        }`}
                      >
                        {fmtCurrency.format(t.amount)}
                      </td>
                      <td className="px-4 py-3">
                        <span className="inline-block px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-700">
                          {t.category ?? "—"}
                        </span>
                      </td>
                      <td className="px-4 py-3">{t.account ?? "—"}</td>
                      <td className="px-4 py-3">
                        <span
                          className={`inline-block px-2 py-1 text-xs rounded-full ${
                            t.source === "api"
                              ? "bg-green-100 text-green-700"
                              : "bg-purple-100 text-purple-700"
                          }`}
                        >
                          {t.source}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
