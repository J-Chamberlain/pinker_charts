# Figure 15-4 source discovery log

## Queries attempted

- `US Bureau of Justice Statistics National Crime Victimization Survey Victimization Analysis Tool rape domestic violence 1993 2014 Jennifer Truman`
- `BJS intimate partner violence attributes victimization 1993 2011 CSV`
- `BJS NCVS API rape sexual assault female victims data`
- `BJS person population NCVS workbook`
- `BJS NCVS Dashboard historical rape sexual assault female rate`

## Sources investigated

- BJS *Intimate Partner Violence: Attributes of Victimization, 1993-2011* (NCJ 243300), accepted for the official intimate-partner definition and published tables.
- BJS *Intimate Partner Violence, 1993-2010* (NCJ 239203), accepted as a corroborating historical release.
- Current BJS NCVS Select personal victimization API, accepted as the machine-readable source for the plotted book-period definitions and the extension.
- Official BJS person population workbook, accepted as the denominator source.
- The historical NVAT URL in the book citation, investigated but no archived export was found.

## Remaining uncertainties

- The exact NVAT export and additional values provided by Jennifer Truman are not publicly archived in this package.
- Current API releases may revise historical estimates or weights, although the derived 1993-2014 trajectory matches the supplied reference at the plotted landmarks.
- The source note calls the gray line intimate partner violence, while the black line's original NVAT query settings are inferred from the matching female rape/sexual-assault series.

## Recommended next steps

Locate an archived NVAT query/export or the original Jennifer Truman handoff if exact byte-level replication is required. Preserve this current API snapshot as a successor source in the meantime.
