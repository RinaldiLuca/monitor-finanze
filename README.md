# 📍 Roadmap di sviluppo – Expense Tracker Personale

---

## 🔹 FASE 1: Fondamenta (Data Ingestion e Normalizzazione)
⏱️ Tempo stimato: 1–2 settimane

🎯 **Obiettivo**: recuperare e standardizzare le transazioni

- [ ] Definire schema transazione standard (data, importo, descrizione, categoria, conto, tipo_movimento, id_transazione)
- [ ] Sviluppare modulo per API bancarie
- [ ] Normalizzare formato dati bancari
- [ ] Sviluppare modulo OCR per PDF (pdfplumber)
- [ ] Estrarre righe transazioni e normalizzarle
- [ ] Persistenza locale SQLite
- [ ] Esportazione opzionale su Google Sheets

---

## 🔹 FASE 2: Backend API e Task Schedulati
⏱️ Tempo stimato: 1–2 settimane

🎯 **Obiettivo**: separare raccolta dati e UI via API

- [ ] Set up ambiente Python con FastAPI o Flask
- [ ] Endpoint REST: /transactions, /categories, /summary, /sync
- [ ] Scheduler (cron o APScheduler) per sync giornaliero
- [ ] Logging dei job schedulati

---

## 🔹 FASE 3: Analisi Dati e Categorizzazione
⏱️ Tempo stimato: 1 settimana

🎯 **Obiettivo**: categorizzare e aggregare i dati

- [ ] Categorizzazione automatica (regex, keyword)
- [ ] Classificazione manuale fallback
- [ ] Analisi principali: spesa mensile, per categoria, bilancio
- [ ] Rilevamento anomalie (spese fuori media)
- [ ] Esportazione PDF / CSV report mensile

---

## 🔹 FASE 4: Frontend in Next.js
⏱️ Tempo stimato: 2–3 settimane

🎯 **Obiettivo**: dashboard interattiva

- [ ] Setup progetto Next.js con Tailwind CSS
- [ ] Autenticazione (NextAuth / Clerk, opzionale)
- [ ] Pagina transazioni (tabella, filtro, ricerca)
- [ ] Pagina spese/budget (grafici torta, barre)
- [ ] Reportistica e riepilogo
- [ ] Collegamento al backend (fetch API REST)

---

## 🔹 FASE 5: Hosting e Deployment
⏱️ Tempo stimato: 1 settimana

🎯 **Obiettivo**: rendere l'app accessibile online

- [ ] Hosting frontend su Vercel
- [ ] Hosting backend Python su Render o Railway
- [ ] Database su Supabase / PlanetScale / ElephantSQL
- [ ] Gestione variabili ambiente e sicurezza

---

## 🔹 FASE 6: Miglioramenti e Scalabilità
⏱️ Tempo stimato: ongoing

🎯 **Obiettivo**: stabilizzare e ampliare

- [ ] Tag automatico spese (ML?)
- [ ] Multi-account / multi-utente
- [ ] Mobile-friendly design
- [ ] Grafici avanzati (es. cash flow, risparmi)
- [ ] Import/export CSV manuale
