import psycopg2

modelo = 'A168WECM-5EF'
conn = psycopg2.connect(host='localhost', database='casio', user='postgres', password='masterkey')
cur = conn.cursor()
cur.execute('SELECT id FROM reloj WHERE referencia = %s', (modelo,))
id_reloj = cur.fetchone()[0]
print(id_reloj)
conn.close()