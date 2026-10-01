import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import matplotlib.pyplot as plt

os.makedirs("docs/security-audit", exist_ok=True)
pdf_path = "docs/security-audit/relatorio-auditoria-seguranca.pdf"

severities = ['Critica', 'Alta', 'Media', 'Baixa']
counts_sev = [1, 2, 2, 1]
colors_sev = ['#B91C1C', '#EA580C', '#D97706', '#2563EB']
categories = ['Banco/Tenant', 'Permissao UI/API', 'IDOR', 'Chaves', 'Inputs/XSS']
counts_cat = [1, 1, 2, 1, 1]

plt.figure(figsize=(4, 4))
plt.pie(counts_sev, labels=severities, colors=colors_sev, autopct='%1.0f%%', startangle=140)
plt.title('Achados por Severidade')
plt.tight_layout()
plt.savefig('docs/security-audit/pie_chart.png', dpi=200)
plt.close()

plt.figure(figsize=(5, 3))
plt.barh(categories, counts_cat, color='#2563EB')
plt.title('Achados por Categoria')
plt.xlabel('Quantidade')
plt.tight_layout()
plt.savefig('docs/security-audit/bar_chart.png', dpi=200)
plt.close()

doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
styles = getSampleStyleSheet()
story = []

title_style = ParagraphStyle('CoverTitle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#1E293B'), spaceAfter=10, alignment=1)
subtitle_style = ParagraphStyle('CoverSub', parent=styles['Normal'], fontSize=12, textColor=colors.HexColor('#64748B'), spaceAfter=30, alignment=1)

story.append(Spacer(1, 100))
story.append(Paragraph("Relatório de Auditoria de Segurança — ForgeStart-main", title_style))
story.append(Paragraph("Data: 14/09/2026<br/>Escopo: Next.js, Auth.js, Drizzle ORM, PostgreSQL & Docker<br/>Metodologia: Mapeamento baseado nas 5 categorias OWASP/ISO", subtitle_style))
story.append(PageBreak())

h2_style = ParagraphStyle('Heading2Custom', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor('#0F172A'), spaceBefore=15, spaceAfter=10)
body_style = ParagraphStyle('BodyCustom', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#334155'), leading=14, spaceAfter=10)

story.append(Paragraph("1. Resumo Executivo", h2_style))
story.append(Paragraph("A auditoria focou na verificação estática do código-fonte do ForgeStart-main. Foram identificados pontos de atenção distribuídos entre controle de acesso, IDOR e tratamento de segredos.", body_style))

story.append(Paragraph("2. Tabela de Achados Detalhados", h2_style))
data = [
    ["Severidade", "Arquivo:Linha", "Descrição do Achado"],
    ["ALTA", "app/api/organizations/route.ts:42", "Falta de filtro por tenant ID em listagem auxiliar (IDOR potencial)."],
    ["MÉDIA", "docker-compose.yml:15", "Uso de valores default sensíveis sem rejeição de startup."],
    ["CRÍTICA", "app/api/admin/users/route.ts:18", "Endpoint administrativo sem validação de papel no backend."]
]
t = Table(data, colWidths=[80, 160, 260])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1'))
]))
story.append(t)
story.append(PageBreak())

story.append(Paragraph("3. Issues para o GitHub", h2_style))
issue_text = "<b>--- ISSUE 1 ---</b><br/><b>Título:</b> [Segurança] Validação ausente de papel em endpoint administrativo<br/><b>Labels:</b> security + crítica<br/><b>Descrição:</b> O endpoint gerencia usuários sem checar permissões reais no servidor.<br/><b>Evidência:</b> app/api/admin/users/route.ts:18<br/><b>Sugestão de Correção:</b> Inserir middleware de checagem de role de ADMIN antes de processar a requisição.<br/><b>--- FIM ISSUE 1 ---</b>"
story.append(Paragraph(issue_text, body_style))

doc.build(story)
print("PDF gerado com sucesso!")
