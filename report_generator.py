from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_cam_report(data, score, category, decision):

    styles = getSampleStyleSheet()
    file_path = "cam_report.pdf"

    story = []

    story.append(Paragraph("Credit Appraisal Memo (CAM)", styles['Title']))
    story.append(Spacer(1,20))

    story.append(Paragraph(f"Company: {data.get('company','Unknown')}", styles['BodyText']))
    story.append(Spacer(1,10))

    story.append(Paragraph("Financial Summary", styles['Heading2']))

    story.append(Paragraph(f"Revenue: {data.get('revenue_by_year',{})}", styles['BodyText']))
    story.append(Paragraph(f"Profit: {data.get('profit_by_year',{})}", styles['BodyText']))
    story.append(Paragraph(f"Debt: {data.get('debt_by_year',{})}", styles['BodyText']))

    story.append(Spacer(1,20))

    story.append(Paragraph("Risk Analysis", styles['Heading2']))
    story.append(Paragraph(f"Risk Score: {score}", styles['BodyText']))
    story.append(Paragraph(f"Risk Category: {category}", styles['BodyText']))

    story.append(Spacer(1,20))

    story.append(Paragraph("Loan Recommendation", styles['Heading2']))
    story.append(Paragraph(f"Decision: {decision['decision']}", styles['BodyText']))
    story.append(Paragraph(f"Suggested Loan Amount: {decision['loan_amount']} crore", styles['BodyText']))
    story.append(Paragraph(f"Interest Rate: {decision['interest_rate']}%", styles['BodyText']))

    doc = SimpleDocTemplate(file_path)
    doc.build(story)

    return file_path