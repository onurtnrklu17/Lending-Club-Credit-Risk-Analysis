import pandas as pd
import sqlite3

print("--- SQL VERİTABANI OLUŞTURMA OPERASYONU BAŞLIYOR ---")


df = pd.read_csv('accepted_2007_to_2018Q4.csv.gz',
                 compression='gzip',
                 nrows=100000,
                 low_memory=False)


df['loan_id'] = range(1, len(df) + 1)

print("Veri yüklendi, tablolara bölünüyor...")
customer_cols = ['loan_id', 'emp_title', 'emp_length', 'home_ownership', 'annual_inc', 'addr_state']
df_customers = df[customer_cols].copy()

loan_cols = ['loan_id', 'loan_amnt', 'term', 'int_rate', 'installment', 'grade', 'purpose', 'title', 'issue_d']
df_loans = df[loan_cols].copy()


profile_cols = ['loan_id', 'dti', 'delinq_2yrs', 'fico_range_low', 'fico_range_high', 'inq_last_6mths']
df_profile = df[profile_cols].copy()


payment_cols = ['loan_id', 'loan_status', 'total_pymnt', 'total_rec_int', 'last_pymnt_d', 'recoveries']
df_payments = df[payment_cols].copy()

print("Tablolar hafızada ayrıldı. Şimdi SQL veritabanına yazılıyor...")

conn = sqlite3.connect('LendingClub_FullStack.db')
cursor = conn.cursor()


df_customers.to_sql('Customers', conn, if_exists='replace', index=False)
df_loans.to_sql('Loans', conn, if_exists='replace', index=False)
df_profile.to_sql('Credit_Profile', conn, if_exists='replace', index=False)
df_payments.to_sql('Payments', conn, if_exists='replace', index=False)

print("✅ BAŞARILI! 'LendingClub_FullStack.db' dosyası oluşturuldu.")
print("Artık elimizde ilişkisel bir veritabanı var.")

sql_query = """
SELECT 
    c.annual_inc, 
    l.grade, 
    l.loan_amnt 
FROM Customers c
JOIN Loans l ON c.loan_id = l.loan_id
WHERE c.annual_inc > 100000 AND l.grade = 'A'
LIMIT 5;
"""

print("\n--- SQL TEST SORGUSU SONUCU ---")
test_sonuc = pd.read_sql(sql_query, conn)
print(test_sonuc)

conn.close()