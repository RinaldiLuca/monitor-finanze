---

# 📍 Roadmap di sviluppo – Monitor Finanze

---

## 🔹 **FASE 1: Fondamenta (Data Ingestion e Normalizzazione)**

🎯 **Obiettivo**: Recuperare e standardizzare le transazioni

* [x] Definito schema transazione standard (`external_id`, date, importo, descrizione, categoria, conto, tipo movimento, hash riga OCR)
* [x] Modulo per API bancarie GoCardless
* [x] Modulo OCR per estratti conto PDF (`pdfplumber`)
* [x] Normalizzazione formato transazioni API / OCR
* [x] Persistenza locale su SQLite con SQLAlchemy Async
* [ ] Integrazione esportazione opzionale su Google Sheets

---

## 🔹 **FASE 2: Backend API (FastAPI)**

🎯 **Obiettivo**: Separare logica di raccolta dati e UI

* [x] Setup progetto FastAPI con SQLAlchemy Async
* [x] Endpoint REST `/transactions` (lista transazioni)
* [ ] Endpoint `/categories` (lista categorie)
* [ ] Endpoint `/summary` (riepilogo aggregato)
* [ ] Endpoint `/sync` (avvio manuale sincronizzazione)
* [ ] Scheduler (APScheduler) per sync giornaliero
* [ ] Logging job schedulati

---

## 🔹 **FASE 3: Categorizzazione e Analisi Dati**

🎯 **Obiettivo**: Classificare automaticamente e analizzare le spese

* **Macro-classificazione (regex / regole)**

  * [ ] Bonifico
  * [ ] Transazione bancomat
  * [ ] Carta di credito
  * [ ] Stipendio / entrata ricorrente

* **Classificazione di dettaglio**

  * [ ] Regole keyword (es. “COOP” → “Spesa”)
  * [ ] Matching esercente via ricerca web / API esterne
  * [ ] Modello ML supervisionato (allenato su storico)
  * [ ] Fallback manuale

* **Analisi base**

  * [ ] Spesa mensile
  * [ ] Spesa per categoria
  * [ ] Bilancio entrate/uscite
  * [ ] Rilevamento anomalie (spese fuori media)
  * [ ] Esportazione PDF / CSV report

---

## 🔹 **FASE 4: Frontend Next.js**

🎯 **Obiettivo**: Dashboard interattiva minimale

* [x] Setup progetto Next.js + Tailwind CSS
* [x] Pagina transazioni (tabella, layout responsive)
* [ ] Filtro / ricerca transazioni
* [ ] Grafico spese per macro-categoria
* [ ] Pagina riepilogo mensile
* [ ] Collegamento al backend tramite API REST

---

## 🔹 **FASE 5: Hosting e Deployment**

🎯 **Obiettivo**: Rendere l’app accessibile online

* [ ] Hosting frontend su Vercel
* [ ] Hosting backend su Render / Railway
* [ ] Database remoto (Supabase / ElephantSQL)
* [ ] Gestione variabili ambiente e sicurezza

---

## 🔹 **FASE 6: Miglioramenti Futuri**

🎯 **Obiettivo**: Stabilizzare e ampliare

* [ ] Mobile-friendly design avanzato
* [ ] Multi-account / multi-utente
* [ ] Grafici avanzati (cash flow, trend risparmio)
* [ ] Import/export CSV manuale
* [ ] Notifiche spese rilevanti / alert budget

---
