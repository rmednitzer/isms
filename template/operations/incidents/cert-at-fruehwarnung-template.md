---
doc_id: TMPL-001
doc_type: record
title: CERT.at Fruehwarnung template (NISG 2026 Paragraph 32)
revision: 1
status: approved
approved_date: 2026-04-19
approved_by: role:CISO
owner: role:CISO
classification: internal
supersedes_revision: null
next_review: 2027-04-19
language: de
framework_refs:
  - nisg2026:§32
signature_ref: null
interim_signature: true
---

# CERT.at Fruehwarnung Vorlage (NISG 2026 Paragraph 32)

**TMPL-001 Revision 1 - 2026-04-19**

*Status: approved. Owner: role:CISO. Next review: 2027-04-19.*

*Interim: legal signature pending QES integration. Approved via git-level only.*

## Zweck

Vorgefuellte Vorlage zur Abgabe einer Fruehwarnung nach NISG 2026 Paragraph 32 (3) ueber das Meldeportal des Computer Emergency Response Team (CERT.at). Die Fruehwarnung ist binnen 24 Stunden ab Kenntnis eines erheblichen Cybersicherheitsvorfalls abzugeben.

Meldeportal: https://nis2.cert.at

## Ablauf

1. Bei Erkennen eines erheblichen Cybersicherheitsvorfalls: Stoppuhr (24 Stunden) starten.
2. Inhalte dieser Vorlage ausfuellen.
3. Am Meldeportal anmelden (qualifizierte Signatur oder Buergerkarte).
4. Formular ausfuellen und abschicken.
5. Bestaetigungsnummer sichern; im Vorfallsdatensatz (INC-YYYY-NNN) eintragen.

## Inhalte der Fruehwarnung

### 1. Unternehmensangaben

- Rechtstraeger: {{entity.legal_name}}
- Kurzbezeichnung: {{entity.short_name}}
- Firmenbuchnummer: {{entity.register_number}}
- NISG 2026 Klassifizierung: {{classification.nisg2026_category}}
- Registrierungskennung (nach Paragraph 34): {{classification.nisg2026_registration_id}}

### 2. Kontakt

- Ansprechperson Vorfall (24/7 erreichbar): TODO Name, Funktion, Telefon, E-Mail
- Stellvertretung: TODO

### 3. Vorfall (Fruehwarnung nach Paragraph 32 Absatz 3)

Laut NISG 2026 beinhaltet die Fruehwarnung folgende Angaben:

- Zeitpunkt des Erkennens des Vorfalls
- Kurzbeschreibung des Vorfalls
- Einschaetzung, ob der Vorfall vermutlich auf rechtswidrige oder boeswillige Handlungen zurueckzufuehren ist oder grenzueberschreitende Auswirkungen haben koennte

#### Zeitpunkt

- Erkannt am: YYYY-MM-DDTHH:MM:SSZ
- Beginn der Auswirkungen (falls abweichend): YYYY-MM-DDTHH:MM:SSZ

#### Kurzbeschreibung

- Was ist passiert (1 bis 3 Saetze):
- Betroffene Dienste:
- Betroffene Systeme (kategorisch, nicht-sensitiv):

#### Einschaetzung

- Rechtswidrige oder boeswillige Handlung vermutet: ja / nein / unklar
- Grenzueberschreitende Auswirkungen moeglich: ja / nein / unklar
- Erste Hypothese zur Ursache (falls vorhanden, sonst "unklar"):

### 4. Bereits getroffene Massnahmen (sofern verfuegbar)

- Containment:
- Benachrichtigte interne Rollen:

### 5. Geplante naechste Schritte

- Meldung nach Paragraph 32 Absatz 4 wird innerhalb 72 Stunden folgen.
- Abschlussbericht nach Paragraph 32 Absatz 5 wird innerhalb eines Monats folgen.

## Nachbereitung im Repository

- Diese ausgefuellte Version wird in `instance/operations/incidents/active/INC-YYYY-NNN/fruehwarnung.de.md` abgelegt.
- Bestaetigungsnummer von CERT.at eintragen.
- INC-YYYY-NNN Feld `cert_at_fruehwarnung.submitted=true`, `submitted_at`, `reference` aktualisieren.

## Hinweise

- Formulierungen knapp und sachlich halten.
- Keine sensiblen Inhalte (Zugangsdaten, Schluessel, personenbezogene Inhalte) in der Fruehwarnung uebermitteln.
- Falls Angaben unsicher sind: als "unklar" markieren statt zu spekulieren.

## Revisionshistorie

| Rev | Datum | Status | Aenderung |
|---|---|---|---|
| 1 | 2026-04-19 | approved | Initialversion |
