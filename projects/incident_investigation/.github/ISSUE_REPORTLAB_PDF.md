# Feature Request: Add ReportLab PDF Generation Support

## 📋 Issue Summary

Add professional PDF report generation using ReportLab library as an alternative to the current FPDF2 implementation for incident investigation reports.

## 🎯 Motivation

Currently, the incident investigation system generates PDF reports using FPDF2. While functional, ReportLab offers:

- **Better formatting capabilities** - Advanced layout control, tables, images
- **Industry standard** - Widely used in enterprise reporting
- **Rich typography** - Better font handling and styling
- **Complex layouts** - Multi-column, nested tables, headers/footers
- **Better documentation** - Extensive resources and examples

## 📄 Current Implementation

**File**: `tests/convert_to_pdf.py`
**Library**: fpdf2
**Output**: Basic text-based PDF (50+ pages)

## ✨ Proposed Enhancement

Create a new PDF generator using ReportLab that provides:

### Features

1. **Professional Layout**
   - Title page with logo/branding
   - Table of contents with hyperlinks
   - Headers and footers with page numbers
   - Section bookmarks for navigation

2. **Advanced Formatting**
   - Styled tables with alternating row colors
   - Color-coded severity indicators (red, orange, yellow, green)
   - Embedded diagrams and charts
   - Multi-level bullet lists and numbering

3. **Typography**
   - Custom fonts (Helvetica, Times New Roman)
   - Font sizes and weights for hierarchy
   - Text alignment and spacing
   - Line breaks and pagination control

4. **Report Sections** (from BP Texas City example)
   - Executive Summary (1 page)
   - Incident Overview with timeline table
   - Evidence Analysis with formatted witness statements
   - Root Cause Analysis with CCPS framework table
   - Barrier Analysis (Swiss Cheese Model) with visual indicators
   - CAPA Recommendations with cost breakdown table
   - Appendices with references

5. **Regulatory Compliance**
   - OSHA PSM reporting format
   - API RP 754 indicator tables
   - CSB investigation template
   - Company-specific branding options

## 💻 Technical Approach

### Installation

```bash
pip install reportlab
```

### Implementation Structure

```python
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, ListFlowable
)
from reportlab.lib import colors

class IncidentReportPDF:
    """Professional PDF generator for incident investigations."""
    
    def __init__(self, output_path):
        self.doc = SimpleDocTemplate(output_path, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.story = []
        
    def add_title_page(self, incident_data):
        """Create professional title page."""
        pass
        
    def add_table_of_contents(self, sections):
        """Add TOC with hyperlinks."""
        pass
        
    def add_formatted_table(self, data, headers, col_widths):
        """Create styled table with headers."""
        pass
        
    def add_timeline(self, events):
        """Timeline with color-coded severity."""
        pass
        
    def generate(self):
        """Build and save PDF."""
        self.doc.build(self.story)
```

### Usage Example

```python
from tests.reportlab_pdf_generator import generate_investigation_report_pdf

# Generate PDF
pdf_path = generate_investigation_report_pdf(
    incident_data={
        "incident_id": "INC-2005-BP-001",
        "title": "BP Texas City Refinery Explosion",
        # ... more data
    },
    output_path="outputs/reports/BP_Investigation_ReportLab.pdf"
)
```

## 📊 Comparison: FPDF2 vs ReportLab

| Feature | FPDF2 (Current) | ReportLab (Proposed) |
|---------|----------------|----------------------|
| Basic text | ✅ | ✅ |
| Tables | ⚠️ Manual | ✅ Built-in |
| Styling | ⚠️ Limited | ✅ Rich styles |
| Headers/Footers | ⚠️ Manual | ✅ Automatic |
| Hyperlinks | ❌ | ✅ |
| Bookmarks | ❌ | ✅ |
| Images | ⚠️ Basic | ✅ Advanced |
| Page templates | ❌ | ✅ |
| Learning curve | Easy | Moderate |
| Documentation | Good | Excellent |
| Enterprise use | Moderate | High |

## 🎨 Sample Output Features

### Title Page
```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         INCIDENT INVESTIGATION REPORT                     ║
║                                                           ║
║     BP Texas City Refinery Explosion                     ║
║                                                           ║
║     Date: March 23, 2005                                 ║
║     Severity: CATASTROPHIC                                ║
║     Fatalities: 15 | Injuries: 180+                      ║
║                                                           ║
║     [Company Logo]                                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Timeline Table (Color-Coded)
| Time | Event | Severity |
|------|-------|----------|
| 13:15 | Relief valve opens | 🟠 Critical |
| 13:20 | **EXPLOSION** | 🔴 **Catastrophic** |
| 13:30 | Emergency response | 🟡 Emergency |

### CAPA Table
| ID | Action | Priority | Cost | Target |
|----|--------|----------|------|--------|
| CAPA-001 | Replace blowdown stacks | 🔴 CRITICAL | $15M | 90 days |
| CAPA-002 | Redundant instrumentation | 🔴 CRITICAL | $2M | 60 days |

## 🔧 Implementation Tasks

- [ ] Create `tests/reportlab_pdf_generator.py`
- [ ] Implement title page with styling
- [ ] Add table of contents with hyperlinks
- [ ] Create formatted timeline table
- [ ] Implement evidence section with multi-column layout
- [ ] Add root cause analysis with CCPS table
- [ ] Create barrier analysis section
- [ ] Implement CAPA recommendations table
- [ ] Add headers/footers with page numbers
- [ ] Create styling templates for different report types
- [ ] Add unit tests for PDF generation
- [ ] Update documentation
- [ ] Add example usage in README

## 📦 Dependencies

```txt
reportlab>=4.0.0
Pillow>=10.0.0  # For image handling
```

## 🎯 Success Criteria

- [ ] PDF generated with professional formatting
- [ ] All tables properly styled and aligned
- [ ] Color-coded severity indicators working
- [ ] Hyperlinked table of contents
- [ ] Page numbers in headers/footers
- [ ] File size < 5MB for typical report
- [ ] Generation time < 10 seconds
- [ ] Compatible with Adobe Reader, Preview, Chrome

## 📚 References

- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [ReportLab GitHub](https://github.com/rstlab/reportlab)
- [Platypus User Guide](https://www.reportlab.com/software/documentation/)
- [Sample PDF Reports](https://www.reportlab.com/examples/)

## 💡 Additional Ideas

### Future Enhancements
- Export to different page sizes (A4, Letter, Legal)
- Add watermarks for draft/confidential reports
- Generate executive summary separately (1-2 pages)
- Create template library for different industries
- Support for custom company branding
- Multi-language report generation
- Digital signatures for regulatory compliance

### Integration
- Could integrate with existing `generate_real_incident_report.py`
- Use same data structures as Word document generator
- Provide format selection: `--format pdf-reportlab` or `--format pdf-fpdf2`

## 🐛 Known Limitations

Current FPDF2 implementation has:
- No table formatting options
- Manual page break handling
- Limited font options
- No hyperlink support
- No bookmarks for navigation
- Basic styling only

ReportLab would address all of these limitations.

## 🔗 Related Issues

- #XXX - Word document generation (completed)
- #XXX - Test suite implementation (completed)
- #XXX - Multi-format export support

## 👥 Assignees

@developer - PDF generation expert
@qa-team - Testing and validation

## 🏷️ Labels

`enhancement` `reporting` `pdf` `high-priority` `good-first-issue`

## ⏰ Timeline

- **Week 1**: Setup and title page
- **Week 2**: Tables and timeline
- **Week 3**: Full report sections
- **Week 4**: Testing and documentation

**Estimated Effort**: 40-60 hours

---

**Priority**: High  
**Type**: Feature Enhancement  
**Component**: Reporting  
**Affects Version**: 1.0.0  
**Fix Version**: 1.1.0
