# After Krypton

**Realization, Uncertainty, and the Uneven Remaking of the Metre, 1983–2000**  
Shivam Gupta · Independent Scholar

A historical research manuscript with an executable reconstruction of international metre-realization recommendations and a Canadian gauge-block uncertainty budget. Prepared for the Seventh AIP Early-Career Conference for Historians of the Physical Sciences, Toronto, 21–25 June 2027.

## Reproduce

The numerical analysis and tests use only Python's standard library (Python 3.9+).

```sh
python3 src/analyze.py
python3 -m unittest discover -s tests -v
```

For figures, install the pinned optional requirements in a virtual environment:

```sh
python3 -m pip install -r requirements-figures.txt
python3 src/figures.py
```

Build the paper and proposal with Tectonic, from this repository root:

```sh
tectonic paper/manuscript.tex --outdir paper
tectonic paper/proposal.tex --outdir paper
```

The supplied PDF versions were compiled and visually checked. `paper/submission_text.json` contains the proposal text and character counts. The conference requests the **proposal PDF only** and explicitly excludes full-paper submissions.

## What is established

- 31 individually numbered assigned regimes in the bounded 1983, 1992 and 1997 enumeration; twelve inherited lamp lines are stored separately.
- Exact equality of twelve separately transcribed 1963 and 1997 legacy wavelengths after unit conversion.
- All 28 printed frequency–wavelength pairs satisfy c/f within the displayed wavelength rounding unit.
- Convention-aware uncertainty ratios distinguish reporting changes from comparisons on the stated standard-deviation basis.
- Methane subdivision, changed calcium conditions, and reclassification of the 576 nm laser are preserved.
- Reconstruction of 25 displayed NRC budget contributions, alongside its separately printed summary, with both kept visible.

This is historical and documentary research. It contains no newly performed optical measurement or claim to a new physical realization of the metre. The nine automated checks validate the specified data and computations; they do not validate historical interpretation by themselves. Neither acceptance nor universal priority is claimed.

## Files

- `data/`: transcriptions, coding protocol and evidence register.
- `src/`: analysis, figures and optional source retrieval.
- `tests/`: nine verification checks.
- `results/`: computed results and test log.
- `figures/`: vector PDF and raster PNG figures.
- `paper/`: full manuscript, conference proposal and editable LaTeX.
- `source_catalogue.json`: source URLs, retrieval hashes and source status.
- `RESEARCH_NOTES.txt`: related work, contribution boundaries and practical applications.

Original third-party source documents are not redistributed here. Retrieval hashes record the copies inspected; dynamic web pages can change. Use source locators and official proceedings to check transcription differences. The 1992 online methane unit discrepancy is documented in `data/README.md`.

## Citation

Gupta, Shivam. 2026. *After Krypton: Realization, Uncertainty, and the Uneven Remaking of the Metre, 1983–2000*. Research manuscript. https://github.com/shi1720/metre-afterlife

This is a research manuscript, not a claim of conference acceptance or a journal publication.

## License

Code: MIT. Original manuscript, original figures, and original dataset organization: CC BY 4.0. Numerical facts remain available for independent reuse. Third-party sources retain their own rights and are accessed through the original institutional providers.
