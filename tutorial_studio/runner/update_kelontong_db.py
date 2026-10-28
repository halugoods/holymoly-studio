#!/usr/bin/env python3
import sqlite3
import subprocess
from pathlib import Path

db_file = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/nusa_temp.sqlite")
conn = sqlite3.connect(str(db_file))
cur = conn.cursor()

# Update categories
cur.execute("UPDATE categories SET name='Sembako' WHERE id=1")
cur.execute("INSERT OR REPLACE INTO categories (id, name, created_at) VALUES (2, 'Bumbu Dapur', 1792776899)")

# Update products
cur.execute("UPDATE products SET name='Beras Rojolele 5kg', category='Sembako', sell_price=75000, stock=50 WHERE id=1")
cur.execute("UPDATE products SET name='Minyak Bimoli 2L', category='Sembako', sell_price=38000, stock=50 WHERE id=2")
cur.execute("""
INSERT OR REPLACE INTO products (id, name, sku, barcode, category, buy_price, sell_price, stock, min_stock, is_service, is_online, created_at)
VALUES (3, 'Bawang Merah 500g', 'BMB01', '899123456003', 'Bumbu Dapur', 15000, 20000, 40, 5, 0, 0, 1792776899)
""")
cur.execute("""
INSERT OR REPLACE INTO products (id, name, sku, barcode, category, buy_price, sell_price, stock, min_stock, is_service, is_online, created_at)
VALUES (4, 'Kecap Manis 550ml', 'BMB02', '899123456004', 'Bumbu Dapur', 18000, 24000, 30, 5, 0, 0, 1792776899)
""")

conn.commit()
conn.close()
print("[DB] Local SQLite updated with authentic Kelontong items.")

# Push to phone
subprocess.run(["adb", "-s", "R5CR81GTJDD", "push", str(db_file), "/data/local/tmp/nusa_kasir.sqlite"], check=True)
subprocess.run(["adb", "-s", "R5CR81GTJDD", "shell", "run-as com.nusa.kelontong cp /data/local/tmp/nusa_kasir.sqlite app_flutter/nusa_kasir.sqlite"], check=True)
subprocess.run(["adb", "-s", "R5CR81GTJDD", "shell", "rm /data/local/tmp/nusa_kasir.sqlite"], check=True)
print("[DB] Pushed to phone app_flutter/nusa_kasir.sqlite successfully!")
