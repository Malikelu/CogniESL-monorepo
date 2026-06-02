## Worksheet Compatibility Rules (DOCX)

When creating documents that will be converted to DOCX:

### Two-Column Sidebar Layout
If using a two-column layout with a sidebar, the `<table>` MUST end where the sidebar content ends. All content below that point flows in a single full-width column. Structure:

```html
<!-- Page 1: two-column panel (sidebar + intro) -->
<table style="width:100%; border-collapse:collapse;">
  <tr>
    <td style="width:200pt; vertical-align:top;"><!-- sidebar --></td>
    <td style="vertical-align:top;"><!-- intro --></td>
  </tr>
</table>
<!-- Rest of document: single-column, full-width -->
<div><!-- sections, charts, tables -- no sidebar ghost space --></div>
```

### Unsupported CSS in DOCX
The DOCX converter does NOT reliably handle:
- flex or grid layout (display: flex/grid)
- position: absolute/fixed/relative
- ::before / ::after pseudo-elements
- background-image (use solid background-color instead)
- box-shadow, border-radius (not supported in older converters)
- em/rem/% units (use pt only for page-accurate layout)
