from fpdf import FPDF
from datetime import datetime
import io

class PDFReportService:
    @staticmethod
    def generate_report(location, climate_data, assessment):
        """
        Generates a professional drought risk assessment report in PDF format.
        Uses modern fpdf2 API.
        """
        try:
            # Create PDF instance
            pdf = FPDF(orientation="P", unit="mm", format="A4")
            pdf.add_page()
            
            # 1. Header Bar (Dark Forest Green)
            pdf.set_fill_color(27, 94, 32)
            pdf.rect(0, 0, 210, 50, 'F')
            
            # Title & Subtitle
            pdf.set_font("helvetica", "B", 30)
            pdf.set_text_color(255, 255, 255)
            pdf.set_y(15)
            pdf.cell(0, 15, "DroughtSense AI", align='C', new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font("helvetica", "I", 12)
            pdf.cell(0, 10, "Automated Agricultural Intelligence System", align='C', new_x="LMARGIN", new_y="NEXT")
            
            # Reset text color and position
            pdf.set_text_color(0, 0, 0)
            pdf.set_y(60)
            
            # 2. Location Intelligence Section
            pdf.set_font("helvetica", "B", 16)
            pdf.cell(0, 10, "I. GEOSPATIAL ANALYSIS", new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font("helvetica", "", 11)
            pdf.set_text_color(80, 80, 80)
            
            loc_name = location.get('display_name', 'Unknown Region')
            lat = location.get('lat', 0.0)
            lon = location.get('lon', 0.0)
            date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
            
            pdf.cell(0, 7, f"Resolved Region: {loc_name}", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 7, f"Geospatial Coordinates: {lat}, {lon}", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 7, f"Report Timestamp: {date_str}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(5)
            
            # 3. Risk Level (Visual Badge)
            risk_level = assessment.get('risk_level', 'Unknown')
            risk_colors = {
                "Low": (76, 175, 80),
                "Medium": (255, 152, 0),
                "High": (244, 67, 54),
                "Critical": (183, 28, 28)
            }
            r, g, b = risk_colors.get(risk_level, (100, 100, 100))
            
            pdf.set_fill_color(r, g, b)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("helvetica", "B", 14)
            # Draw a badge-like cell
            pdf.cell(70, 12, f"VULNERABILITY: {risk_level.upper()}", align='C', fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(10)
            
            # 4. Climate Indicators
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("helvetica", "B", 14)
            pdf.cell(0, 10, "II. ENVIRONMENTAL SENSOR DATA (30-DAY AVG)", new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font("helvetica", "", 12)
            temp = climate_data.get('temperature', '--')
            precip = climate_data.get('precipitation', '--')
            soil = climate_data.get('soil_moisture', 0.0)
            
            pdf.cell(0, 8, f"- Average Temperature: {temp} degrees C", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 8, f"- Total Precipitation: {precip} mm", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 8, f"- Soil Water Index: {int(float(soil) * 100)}%", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(10)
            
            # 5. AI Reasoning Summary
            pdf.set_font("helvetica", "B", 14)
            pdf.cell(0, 10, "III. AGENTIC REASONING SUMMARY", new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font("helvetica", "", 11)
            explanation = assessment.get('explanation', 'No explanation provided.')
            pdf.multi_cell(0, 7, explanation, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(10)
            
            # 6. Operational Directives
            pdf.set_font("helvetica", "B", 14)
            pdf.cell(0, 10, "IV. OPERATIONAL DIRECTIVES", new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font("helvetica", "", 11)
            recs = assessment.get('recommendations', [])
            for rec in recs:
                pdf.multi_cell(0, 7, f"- {rec}", new_x="LMARGIN", new_y="NEXT")
            
            pdf.ln(10)
            
            # 7. Scientific Citations
            citations = assessment.get('citations')
            if citations and citations != "None":
                pdf.set_font("helvetica", "B", 12)
                pdf.cell(0, 10, "SCIENTIFIC CITATIONS", new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("helvetica", "I", 9)
                pdf.set_text_color(100, 100, 100)
                pdf.multi_cell(0, 5, citations, new_x="LMARGIN", new_y="NEXT")

            # 8. Footer
            pdf.set_y(-25)
            pdf.set_font("helvetica", "I", 8)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 10, "Generated by DroughtSense AI on AMD Instinct Accelerator. For agricultural advisory only.", align='C')
            
            # Return as bytes
            return pdf.output()
            
        except Exception as e:
            print(f"PDF_SERVICE_ERROR: {e}")
            raise e
