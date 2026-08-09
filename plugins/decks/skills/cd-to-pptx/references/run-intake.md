# Run Intake - answer once per run

These are the only things the skill can't figure out by inspecting the files. Answer them once at the start of a run and they apply to every deck in that run, unless you flag a specific deck as different. Everything else (canvas size, slide count, font, TTF presence, chart locations) the skill reads from the files itself.

Keep this short on purpose. The whole point is that you answer five things, hand over the folders, and walk away until there's a file to review.

---

## The five questions

1. **Design system folder** - where is the Claude Design System folder these decks were built from? (The one with the tokens, the TTF fonts, and the logo PNGs.) The skill pulls assets and canonical token values from here. Point to it once for the run.

2. **Fidelity bar** - same for the whole run unless you say otherwise:
   - "Exact visual reproduction" - match the PDF as closely as native shapes allow
   - "Faithful, on-brand native rebuild" - editable always wins over pixel-matching

3. **Output naming** - the pattern for finished files:
   - Customer-facing: `<YourOrg>_<Customer>_<Doctype>.pptx` (swap in the org name the user actually goes by)
   - Internal: descriptive, your call
   - Default: new version (`_v2`), never overwrite an existing file

4. **Speaker notes** - include them or not. (Yes/No, applies to all decks in the run.)

5. **Standalone or section** - per deck, but you can set a run default:
   - Standalone - each deck is its own finished presentation
   - Section of a master - merges into a larger deck later. If so, point to the master deck/section to inherit slide masters and layouts from. If you don't give one, sections built in the same run share a master with each other (but you can't safely add a section in a later run without pointing at one).

---

## What you do NOT answer

- Which HTML file is the source (skill detects; only asks if there are multiple)
- Canvas dimensions, slide count, font variable (skill reads from the export)
- Whether TTFs are present (skill checks the design system folder)
- Charts data-accurate vs representative (not built - they become placeholders)
- Where each chart goes (skill detects and reports for your confirmation)

---

## Folder shape the skill expects

Drop decks like this so recon is deterministic - no hunting:

```
<run-folder>/
├── fonts/                      <- TTFs, shared by all decks (or point to the design system folder)
├── deck-01-<name>/
│   ├── *-print.html            <- the source HTML export
│   └── *.pdf                   <- the reference PDF (REQUIRED - run stops without it)
├── deck-02-<name>/
│   ├── *-print.html
│   └── *.pdf
└── ...
```

The PDF is required per deck. The skill checks for all of them at preflight and stops before starting if any deck is missing one - so you fix everything up front, not mid-run on deck 3.
