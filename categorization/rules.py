import re
from dataclasses import dataclass

# from typing import Optional


@dataclass
class MacroResult:
    macro: str  # "bonifico" | "bancomat" | "carta_credito" | "stipendio" | "altro"
    confidence: float  # 0..1
    reason: str  # spiega la regola che ha scattato


PATTERNS = {
    "bonifico": [r"\bSEPA\b", r"\bBONIFICO\b", r"\bTRF\b", r"\bB.TRANSF\b"],
    "bancomat": [r"\bPOS\b", r"\bBANCOMAT\b", r"\bPAGOBANCOMAT\b"],
    "carta_credito": [r"\b(CARTA|CB|ADDEBITO\s+CARTA)\b"],
    "stipendio": [r"\b(STIPENDIO|SALARIO|PAGA|EMOLUMENTI|ACCREDITO\s+STIPENDIO)\b"],
}


def macro_classify(
    description: str | None, source: str, amount: float  # Optional[str],
) -> MacroResult:
    text = (description or "").upper()
    # 1) pattern forti
    for macro, regs in PATTERNS.items():
        for rx in regs:
            if re.search(rx, text):
                return MacroResult(macro=macro, confidence=0.95, reason=f"regex:{rx}")
    # 2) euristiche leggere
    # if source == "api" and "PDF" not in text and amount < 0 and ("POS" in text or "BANCOMAT" in text):
    #    return MacroResult(macro="bancomat", confidence=0.7, reason="euristica: source+amount+token")
    # 3) fallback
    return MacroResult(macro="altro", confidence=0.4, reason="no_rules")
