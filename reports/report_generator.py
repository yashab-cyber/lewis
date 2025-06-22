#!/usr/bin/env python3
"""
LEWIS Report Generator
Generates security reports, certificates, and audit documentation
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import base64
import hashlib

# PDF generation libraries
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.lineplots import LinePlot
    from reportlab.graphics.charts.piecharts import Pie
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# HTML/CSS generation
from jinja2 import Template
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

from config.settings import Settings
from utils.logger import Logger

@dataclass
class ReportSection:
    title: str
    content: str
    charts: List[str] = None
    tables: List[Dict] = None
    severity: str = "info"

@dataclass
class SecurityFinding:
    title: str
    description: str
    severity: str
    cvss_score: float
    affected_systems: List[str]
    recommendations: List[str]
    evidence: List[str] = None

class ReportGenerator:
    """Generates comprehensive security reports and certificates"""
    
    def __init__(self, settings: Settings, logger: Logger):
        self.settings = settings
        self.logger = logger
        self.output_dir = Path(settings.get("reports", {}).get("output_dir", "outputs/reports"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Report templates
        self.templates_dir = Path("reports/templates")
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Create default templates if they don't exist
        self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default report templates"""
        
        # HTML report template
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ report_title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }
        .section { margin: 30px 0; }
        .finding { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .critical { border-left: 5px solid #dc3545; }
        .high { border-left: 5px solid #fd7e14; }
        .medium { border-left: 5px solid #ffc107; }
        .low { border-left: 5px solid #28a745; }
        .info { border-left: 5px solid #17a2b8; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f2f2f2; }
        .chart { text-align: center; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ report_title }}</h1>
        <p>Generated on: {{ generation_date }}</p>
        <p>Report ID: {{ report_id }}</p>
    </div>
    
    <div class="section">
        <h2>Executive Summary</h2>
        <p>{{ executive_summary }}</p>
    </div>
    
    {% for section in sections %}
    <div class="section">
        <h2>{{ section.title }}</h2>
        <p>{{ section.content }}</p>
        
        {% if section.charts %}
        <div class="chart">
            {% for chart in section.charts %}
            <img src="data:image/png;base64,{{ chart }}" alt="Chart">
            {% endfor %}
        </div>
        {% endif %}
        
        {% if section.tables %}
        {% for table in section.tables %}
        <table>
            <thead>
                <tr>
                    {% for header in table.headers %}
                    <th>{{ header }}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for row in table.rows %}
                <tr>
                    {% for cell in row %}
                    <td>{{ cell }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endfor %}
        {% endif %}
    </div>
    {% endfor %}
    
    {% if findings %}
    <div class="section">
        <h2>Security Findings</h2>
        {% for finding in findings %}
        <div class="finding {{ finding.severity }}">
            <h3>{{ finding.title }}</h3>
            <p><strong>Severity:</strong> {{ finding.severity.upper() }} (CVSS: {{ finding.cvss_score }})</p>
            <p><strong>Description:</strong> {{ finding.description }}</p>
            <p><strong>Affected Systems:</strong> {{ finding.affected_systems | join(', ') }}</p>
            <h4>Recommendations:</h4>
            <ul>
                {% for rec in finding.recommendations %}
                <li>{{ rec }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endfor %}
    </div>
    {% endif %}
    
    <div class="section">
        <h2>Conclusion</h2>
        <p>{{ conclusion }}</p>
    </div>
    
    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd;">
        <p><small>Generated by LEWIS - Linux Environment Working Intelligence System</small></p>
    </footer>
</body>
</html>
        """
        
        template_path = self.templates_dir / "default_report.html"
        if not template_path.exists():
            template_path.write_text(html_template)
    
    async def generate_report(self, 
                            report_type: str = "vulnerability",
                            format: str = "html",
                            filters: Optional[Dict[str, Any]] = None,
                            user_id: str = None) -> Path:
        """Generate a security report"""
        
        try:
            self.logger.info(f"Generating {report_type} report in {format} format")
            
            # Gather data based on report type
            report_data = await self._gather_report_data(report_type, filters, user_id)
            
            # Generate report based on format
            if format.lower() == "pdf":
                return await self._generate_pdf_report(report_data)
            elif format.lower() == "html":
                return await self._generate_html_report(report_data)
            elif format.lower() == "json":
                return await self._generate_json_report(report_data)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            self.logger.error(f"Report generation failed: {str(e)}")
            raise
    
    async def _gather_report_data(self, report_type: str, filters: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Gather data for report generation"""
        
        # This would typically connect to the database and gather actual scan results
        # For now, we'll generate sample data
        
        report_data = {
            "report_id": hashlib.md5(f"{datetime.now().isoformat()}{user_id}".encode()).hexdigest()[:8],
            "report_title": f"LEWIS {report_type.title()} Assessment Report",
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id,
            "report_type": report_type,
            "executive_summary": self._generate_executive_summary(report_type),
            "sections": [],
            "findings": [],
            "statistics": {},
            "conclusion": "The assessment has been completed successfully. Please review the findings and implement the recommended security measures."
        }
        
        # Add sections based on report type
        if report_type == "vulnerability":
            report_data["sections"].extend([
                ReportSection(
                    title="Network Scan Results",
                    content="Network scanning identified several open ports and services running on the target systems.",
                    severity="info"
                ),
                ReportSection(
                    title="Web Application Assessment",
                    content="Web application testing revealed potential security vulnerabilities in the target applications.",
                    severity="medium"
                ),
                ReportSection(
                    title="System Hardening Review",
                    content="System configuration review identified areas for security hardening.",
                    severity="low"
                )
            ])
            
            # Add sample findings
            report_data["findings"] = [
                SecurityFinding(
                    title="Unencrypted HTTP Traffic",
                    description="The application is serving content over unencrypted HTTP connections.",
                    severity="medium",
                    cvss_score=5.3,
                    affected_systems=["web-server-01", "api-gateway"],
                    recommendations=[
                        "Implement HTTPS encryption for all web traffic",
                        "Configure HTTP to HTTPS redirects",
                        "Update security headers"
                    ]
                ),
                SecurityFinding(
                    title="Outdated Software Components",
                    description="Several system components are running outdated versions with known vulnerabilities.",
                    severity="high",
                    cvss_score=7.5,
                    affected_systems=["web-server-01", "database-server"],
                    recommendations=[
                        "Update all software components to latest versions",
                        "Implement automated patching process",
                        "Establish vulnerability management program"
                    ]
                )
            ]
        
        elif report_type == "penetration":
            report_data["sections"].extend([
                ReportSection(
                    title="Reconnaissance",
                    content="Information gathering phase identified target systems and services.",
                    severity="info"
                ),
                ReportSection(
                    title="Vulnerability Exploitation",
                    content="Attempted exploitation of identified vulnerabilities.",
                    severity="high"
                ),
                ReportSection(
                    title="Post-Exploitation",
                    content="Activities performed after successful exploitation.",
                    severity="critical"
                )
            ])
        
        # Generate statistics
        report_data["statistics"] = self._generate_statistics(report_data["findings"])
        
        return report_data
    
    def _generate_executive_summary(self, report_type: str) -> str:
        """Generate executive summary based on report type"""
        
        summaries = {
            "vulnerability": "This vulnerability assessment report provides a comprehensive analysis of the security posture of the target systems. The assessment identified several security issues ranging from low to high severity that require immediate attention.",
            "penetration": "This penetration testing report documents the security assessment performed against the target environment. The testing identified exploitable vulnerabilities that could be leveraged by malicious actors.",
            "compliance": "This compliance assessment report evaluates the organization's adherence to relevant security standards and regulations. The assessment identifies gaps and provides recommendations for achieving compliance.",
            "incident": "This incident response report documents the analysis and containment of a security incident. The report provides a timeline of events and recommendations for preventing similar incidents."
        }
        
        return summaries.get(report_type, "This security assessment report provides analysis and recommendations for improving the security posture.")
    
    def _generate_statistics(self, findings: List[SecurityFinding]) -> Dict[str, Any]:
        """Generate statistics from findings"""
        
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        
        for finding in findings:
            severity_counts[finding.severity] += 1
        
        total_findings = len(findings)
        
        return {
            "total_findings": total_findings,
            "severity_breakdown": severity_counts,
            "risk_score": self._calculate_risk_score(findings),
            "completion_time": "2h 15m"
        }
    
    def _calculate_risk_score(self, findings: List[SecurityFinding]) -> float:
        """Calculate overall risk score"""
        
        if not findings:
            return 0.0
        
        total_score = sum(finding.cvss_score for finding in findings)
        return round(total_score / len(findings), 1)
    
    async def _generate_html_report(self, report_data: Dict[str, Any]) -> Path:
        """Generate HTML report"""
        
        template_path = self.templates_dir / "default_report.html"
        template = Template(template_path.read_text())
        
        # Generate charts
        charts = await self._generate_charts(report_data)
        
        # Add charts to sections
        for section in report_data["sections"]:
            section_charts = []
            if section.title == "Statistics":
                section_charts = charts
            section.charts = section_charts
        
        html_content = template.render(**report_data)
        
        # Save HTML report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"lewis_report_{timestamp}.html"
        report_path = self.output_dir / report_filename
        
        report_path.write_text(html_content, encoding="utf-8")
        
        self.logger.info(f"HTML report generated: {report_path}")
        return report_path
    
    async def _generate_pdf_report(self, report_data: Dict[str, Any]) -> Path:
        """Generate PDF report"""
        
        if not REPORTLAB_AVAILABLE:
            self.logger.warning("ReportLab not available, falling back to HTML report")
            return await self._generate_html_report(report_data)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"lewis_report_{timestamp}.pdf"
        report_path = self.output_dir / report_filename
        
        # Create PDF document
        doc = SimpleDocTemplate(str(report_path), pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph(report_data["report_title"], title_style))
        story.append(Spacer(1, 12))
        
        # Report info
        info_data = [
            ["Report ID:", report_data["report_id"]],
            ["Generated:", report_data["generation_date"]],
            ["Type:", report_data["report_type"].title()]
        ]
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", styles['Heading2']))
        story.append(Paragraph(report_data["executive_summary"], styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Sections
        for section in report_data["sections"]:
            story.append(Paragraph(section.title, styles['Heading2']))
            story.append(Paragraph(section.content, styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Findings
        if report_data["findings"]:
            story.append(Paragraph("Security Findings", styles['Heading2']))
            
            for finding in report_data["findings"]:
                story.append(Paragraph(finding.title, styles['Heading3']))
                story.append(Paragraph(f"<b>Severity:</b> {finding.severity.upper()} (CVSS: {finding.cvss_score})", styles['Normal']))
                story.append(Paragraph(f"<b>Description:</b> {finding.description}", styles['Normal']))
                story.append(Paragraph(f"<b>Affected Systems:</b> {', '.join(finding.affected_systems)}", styles['Normal']))
                
                story.append(Paragraph("Recommendations:", styles['Heading4']))
                for rec in finding.recommendations:
                    story.append(Paragraph(f"• {rec}", styles['Normal']))
                
                story.append(Spacer(1, 15))
        
        # Statistics
        if report_data["statistics"]:
            story.append(Paragraph("Statistics", styles['Heading2']))
            
            stats_data = [
                ["Total Findings", str(report_data["statistics"]["total_findings"])],
                ["Risk Score", str(report_data["statistics"]["risk_score"])],
                ["Completion Time", report_data["statistics"]["completion_time"]]
            ]
            
            stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(stats_table)
        
        # Build PDF
        doc.build(story)
        
        self.logger.info(f"PDF report generated: {report_path}")
        return report_path
    
    async def _generate_json_report(self, report_data: Dict[str, Any]) -> Path:
        """Generate JSON report"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"lewis_report_{timestamp}.json"
        report_path = self.output_dir / report_filename
        
        # Convert dataclasses to dictionaries
        json_data = report_data.copy()
        json_data["sections"] = [
            {
                "title": section.title,
                "content": section.content,
                "severity": section.severity
            }
            for section in report_data["sections"]
        ]
        
        json_data["findings"] = [
            {
                "title": finding.title,
                "description": finding.description,
                "severity": finding.severity,
                "cvss_score": finding.cvss_score,
                "affected_systems": finding.affected_systems,
                "recommendations": finding.recommendations
            }
            for finding in report_data["findings"]
        ]
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"JSON report generated: {report_path}")
        return report_path
    
    async def _generate_charts(self, report_data: Dict[str, Any]) -> List[str]:
        """Generate base64 encoded charts for reports"""
        
        charts = []
        
        try:
            # Set style for better looking charts
            plt.style.use('seaborn-v0_8')
            
            # Severity distribution pie chart
            if report_data["statistics"]["severity_breakdown"]:
                severity_data = report_data["statistics"]["severity_breakdown"]
                
                # Filter out zero values
                labels = []
                values = []
                colors_list = []
                color_map = {
                    'critical': '#dc3545',
                    'high': '#fd7e14',
                    'medium': '#ffc107',
                    'low': '#28a745',
                    'info': '#17a2b8'
                }
                
                for severity, count in severity_data.items():
                    if count > 0:
                        labels.append(f"{severity.title()} ({count})")
                        values.append(count)
                        colors_list.append(color_map[severity])
                
                if values:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.pie(values, labels=labels, colors=colors_list, autopct='%1.1f%%', startangle=90)
                    ax.set_title('Findings by Severity', fontsize=16, fontweight='bold')
                    
                    # Convert to base64
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
                    buffer.seek(0)
                    chart_data = base64.b64encode(buffer.getvalue()).decode()
                    charts.append(chart_data)
                    plt.close()
            
            # Risk score trend (mock data)
            fig, ax = plt.subplots(figsize=(10, 6))
            dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
            risk_scores = [report_data["statistics"]["risk_score"] + (x % 5 - 2) for x in range(30)]
            
            ax.plot(dates, risk_scores, marker='o', linewidth=2, markersize=4)
            ax.set_title('Risk Score Trend (Last 30 Days)', fontsize=16, fontweight='bold')
            ax.set_xlabel('Date')
            ax.set_ylabel('Risk Score')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            chart_data = base64.b64encode(buffer.getvalue()).decode()
            charts.append(chart_data)
            plt.close()
            
        except Exception as e:
            self.logger.error(f"Chart generation failed: {str(e)}")
        
        return charts
    
    async def generate_certificate(self, user_id: str, course_name: str, completion_date: datetime = None) -> Path:
        """Generate training certificate"""
        
        if completion_date is None:
            completion_date = datetime.now()
        
        certificate_data = {
            "user_id": user_id,
            "course_name": course_name,
            "completion_date": completion_date.strftime("%B %d, %Y"),
            "certificate_id": hashlib.md5(f"{user_id}{course_name}{completion_date}".encode()).hexdigest()[:12].upper()
        }
        
        # Generate certificate (HTML format for now)
        certificate_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>LEWIS Training Certificate</title>
    <style>
        body {{ font-family: 'Georgia', serif; text-align: center; margin: 0; padding: 50px; }}
        .certificate {{ border: 5px solid #2c3e50; padding: 50px; margin: 50px auto; max-width: 800px; }}
        .header {{ font-size: 36px; color: #2c3e50; margin-bottom: 30px; }}
        .title {{ font-size: 48px; color: #e74c3c; margin: 30px 0; }}
        .content {{ font-size: 24px; line-height: 1.6; margin: 30px 0; }}
        .signature {{ margin-top: 50px; }}
        .date {{ font-size: 18px; color: #666; }}
    </style>
</head>
<body>
    <div class="certificate">
        <div class="header">LEWIS - Linux Environment Working Intelligence System</div>
        <div class="title">Certificate of Completion</div>
        <div class="content">
            This is to certify that<br>
            <strong style="font-size: 32px; color: #2c3e50;">{user_id}</strong><br>
            has successfully completed the course<br>
            <strong style="font-size: 28px; color: #e74c3c;">{course_name}</strong><br>
            on {completion_date}
        </div>
        <div class="signature">
            <p>Certificate ID: {certificate_data['certificate_id']}</p>
            <p style="border-top: 2px solid #2c3e50; padding-top: 20px; margin-top: 50px;">
                LEWIS Training Authority
            </p>
        </div>
        <div class="date">Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
    </div>
</body>
</html>
        """
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cert_filename = f"lewis_certificate_{user_id}_{timestamp}.html"
        cert_path = self.output_dir / cert_filename
        
        cert_path.write_text(certificate_html, encoding="utf-8")
        
        self.logger.info(f"Certificate generated: {cert_path}")
        return cert_path

# Factory function
def create_report_generator(settings: Settings, logger: Logger) -> ReportGenerator:
    """Create and configure report generator"""
    return ReportGenerator(settings, logger)
