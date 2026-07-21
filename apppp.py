import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Her Kuyumculuk - Matbaa Uyumlu Değişken Basım", page_icon="🧾", layout="centered")

st.title("🧾 Matbaa Uyumlu Değişken Veri Basımı")
st.write("Matbaa kağıdını yazıcıya takın; sadece değişken veriler tam koçandaki yerlerine basılsın!")

uploaded_file = st.file_uploader("Gider Pusulası Excel Dosyasını Yükle (.xlsx)", type=["xlsx", "xls"])

if uploaded_file is not None:
    with open("temp_excel.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    df = pd.read_excel("temp_excel.xlsx", sheet_name="Sayfa1")
    df_valid = df[df['İSİM'].notna() & (df['İSİM'] != 0) & (df['İSİM'] != '0') & (df['İSİM'] != '')].copy()
    
    st.success(f"Excel yüklendi! Toplam **{len(df_valid)}** adet kayıt işleme hazır.")
    
    st.dataframe(df_valid[['SATILAN CİNSİ', 'İSİM', 'TC', 'GİDEN HAVALE TUTARI', 'ÖDEME ŞEKLİ', 'ALTIN GRAM', 'BİRİM FİYAT']])
    
    if st.button("🚀 Sadece Değişken Bilgileri Üret", type="primary"):
        html_icerik = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    @page { size: A4 landscape; margin: 8mm; }
    @media print { body { -webkit-print-color-adjust: exact; } .page-break { page-break-after: always; } }
    *, *::before, *::after { box-sizing: border-box; }
    body { margin: 0; padding: 0; font-family: Arial, sans-serif; font-size: 8.5pt; color: #000; background-color: transparent; }
    .container { display: table; width: 100%; table-layout: fixed; margin-bottom: 20px; }
    .panel { display: table-cell; width: 50%; padding: 8px 15px; vertical-align: top; position: relative; height: 180mm; }
    
    .header-top { position: relative; height: 75px; margin-bottom: 10px; }
    
    .details-box { margin-top: 35px; padding: 6px; min-height: 50px; position: relative; margin-bottom: 12px; }
    .name-val { font-size: 10.5pt; font-weight: bold; text-align: center; margin-bottom: 3px; margin-top: 2px; }
    .tc-val { font-size: 9.5pt; text-align: center; letter-spacing: 0.5px; font-weight: bold; }
    
    .table-area { width: 100%; border-collapse: collapse; margin-bottom: 12px; }
    .table-area td { font-size: 8.5pt; padding: 6px 0; vertical-align: top; border-bottom: none; font-weight: bold; }
    
    .payment-row { font-size: 9pt; font-weight: bold; margin-bottom: 12px; }
    .total-row { font-size: 9.5pt; font-weight: bold; margin-bottom: 25px; }
    
    .signature-area { position: absolute; bottom: 20px; right: 15px; width: 200px; text-align: center; }
    .signature-line { height: 20px; margin-bottom: 4px; }
    .contact-info-area { font-size: 8pt; text-align: left; line-height: 1.4; margin-top: 4px; font-weight: bold; }
</style>
</head>
<body>
"""
        
        for index, row in df_valid.iterrows():
            musteri_adi = str(row['İSİM'])
            tc_no = str(row['TC'])
            urun_adi = str(row['SATILAN CİNSİ'])
            miktar = float(row['ALTIN GRAM'])
            birim_fiyat = float(row['BİRİM FİYAT'])
            toplam_tutar = float(row['GİDEN HAVALE TUTARI'])
            odeme_turu = str(row['ÖDEME ŞEKLİ'])
            
            tek_panel = f"""
            <div class="panel">
                <div class="header-top"></div>
                
                <div class="details-box">
                    <div class="name-val">{musteri_adi}</div>
                    <div class="tc-val">{tc_no}</div>
                </div>
                
                <table class="table-area">
                    <tbody>
                        <tr>
                            <td style="width: 38%;">{urun_adi}</td>
                            <td style="width: 22%;">{miktar:,.2f}</td>
                            <td style="width: 20%;">{birim_fiyat:,.2f}₺</td>
                            <td style="width: 20%; text-align: right;">{toplam_tutar:,.2f}₺</td>
                        </tr>
                    </tbody>
                </table>
                <div style="height: 15px;"></div>
                <div class="payment-row" style="margin-top: 18px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{odeme_turu}</div>
                <div class="total-row">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{toplam_tutar:,.2f}₺</div>
                <div class="signature-area">
                    <div class="signature-line"></div>
                    <div class="contact-info-area">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    </div>
                </div>
            </div>
            """
            
            html_icerik += '<div class="container">' + (tek_panel * 2) + '</div>'
            if index < len(df_valid) - 1:
                html_icerik += '<div class="page-break"></div>'
                
        html_icerik += "</body></html>"
        
        with open("gider_pusulasi_ciktisi.html", "w", encoding="utf-8") as f:
            f.write(html_icerik)
            
        st.success("İşlem tamam! Sadece değişken alanların basılacağı katman hazır.")
        
        with open("gider_pusulasi_ciktisi.html", "rb") as file:
            st.download_button(
                label="📥 Değişken Veri Çıktısını İndir",
                data=file,
                file_name="gider_pusulasi_ciktisi.html",
                mime="text/html"
            )