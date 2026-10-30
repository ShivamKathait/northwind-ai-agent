# Clarifying questions (email before starting; max 3)

Subject: Northwind take-home (NWG-D0BC): three clarifying questions

1. **GBP/SGD closing rate.** `fx_rates.csv` gives GBP/SGD opening and FY average rates only, and no USD/SGD rate
   to derive a cross rate. Is the closing rate intentionally unavailable, in which case I'd report `sgd_bank_gbp` as null
   with a reason and leave the balance at its booked amount (flagged), or can you supply one?

2. **Control figure format.** `intercompany_difference` asks for a split into causes, and `journals` for three counts.
   May these two values be JSON objects (for example `{"total": …, "in_transit": …, "fx_retranslation": …}` and
   `{"posted": …, "rejected": …, "held": …}`), or must every key hold a single number?

3. **Journal and subledger treatment.** Policy 6 covers journals that are invalid for FY2024. For entries that are
   valid in form but look like duplicates of something already booked, or that would push a balance to the
   wrong side, should I hold them for review (not posted, reported separately) or reject them? And for the UK
   debtors and creditors control accounts, which differ from their subledgers, should I leave the ledger
   unadjusted and flag the differences?
