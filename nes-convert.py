#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import sys
import pdfkit

if len(sys.argv) < 3:
    print("Usage: python3 nessus_report.py scan.nessus report.html")
    sys.exit(1)

nessus_file = sys.argv[1]
html_file = sys.argv[2]
pdf_file = html_file.replace('.html', '.pdf')

tree = ET.parse(nessus_file)
root = tree.getroot()

html = ['<html><head><title>Nessus Report</title></head><body>']
html.append('<h1>Nessus Scan Report</h1>')

for report_host in root.iter('ReportHost'):
    hostname = report_host.attrib.get('name', 'Unknown Host')
    html.append(f'<h2>{hostname}</h2>')
    html.append('<ul>')

    for report_item in report_host.iter('ReportItem'):
        plugin_name = report_item.attrib.get('pluginName', 'Unknown Plugin')
        severity = report_item.attrib.get('severity', '0')
        port = report_item.attrib.get('port', 'N/A')
        html.append(f'<li><strong>{plugin_name}</strong> (Port: {port}, Severity: {severity})</li>')

    html.append('</ul>')

html.append('</body></html>')

# Save HTML
with open(html_file, 'w') as f:
    f.write('\n'.join(html))

print(f"[+] HTML report saved to {html_file}")

# Convert to PDF
try:
    pdfkit.from_file(html_file, pdf_file)
    print(f"[+] PDF report saved to {pdf_file}")
except Exception as e:
    print(f"[!] PDF conversion failed: {e}")
