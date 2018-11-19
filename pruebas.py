import fdb


con = fdb.connect(dsn='192.168.1.252:W:\STECCS_MGV_TEST.FDB',
                  user='sysdba',
                  password='masterkey',
                  charset='UTF8')


cursor = con.cursor()
familia = input('De que familia CASIO quieres sacar los datos? ')
result = cursor.execute("SELECT CODIGO_ARTICULO FROM ARTICULOS WHERE FAMILIA = '{}'".format(familia))
# result = cursor.execute("SELECT CODIGO_ARTICULO FROM ARTICULOS WHERE CODIGO_ARTICULO = 'A168WECM-5EF'")
items = [row[0] for row in result]
con.close()

print(items)

items= ['GW-B5600-2ER', 'GW-B5600BC-1BER', 'GW-B5600BC-1ER', 'GMW-B5000GD-1ER', 'GMW-B5000GD-9ER', 'GW-B5600HR-1ER', 'GBD-800-1ER', 'GBD-800-2ER', 'GBD-800-1BER', 'GBD-800-4ER', 'GBD-800-7ER', 'GBD-800-8ER', 'GR-B100-1A2ER', 'GR-B100-1A3ER', 'GR-B100-1A4ER', 'GR-B100GB-1AER', 'GST-W130BC-1A3ER', 'GST-W330AC-2AER', 'MTG-B1000-1AER', 'MTG-B1000B-1A4ER', 'MTG-B1000B-1AER']

for item in items:
    print("{}".format(item))
