import psycopg2

conn = psycopg2.connect(host='192.168.1.252', database='casio', user='postgres', password='Mgv17Watch')
cur = conn.cursor()
cur.execute("INSERT INTO reloj (referencia, tipo_reparacion, pila, modulo, categoria, img_url) VALUES ( 'A158WEA-1EF', 'Replacment', 'CR2017', '498', 'Collection', 'No tiene') ON CONFLICT (referencia) DO UPDATE SET tipo_reparacion = EXCLUDED.tipo_reparacion, pila = EXCLUDED.pila, modulo = EXCLUDED.modulo, categoria = EXCLUDED.categoria, img_url = EXCLUDED.img_url RETURNING id")
id_reloj = cur.fetchone()[0]
conn.commit()
print(dir(cur))
# id_reloj = cur.lastrowid

print(id_reloj)