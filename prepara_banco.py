import MySQLdb

print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='', database='findtarget', host='localhost', port=3306)


# Descomente se quiser desfazer o banco...
conn.cursor().execute("DROP DATABASE IF EXISTS `findtarget`;")
conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `findtarget` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `findtarget`;
    CREATE TABLE `Modelos_Executados` (
      `id` int NOT NULL AUTO_INCREMENT,
      `organismo` varchar(150) COLLATE utf8_bin NOT NULL,
      `fba_result` double precision NOT NULL,
      `arquivo_sbml` varchar(200) NOT NULL,
      `forma_analise` varchar(50) COLLATE utf8_bin NOT NULL,
      `descricao` text COLLATE utf8_bin NOT NULL,
      `data_execucao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `id_user` int NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    
    CREATE TABLE `Usuarios` (
      `id` int NOT NULL AUTO_INCREMENT,
      `nome` varchar(100) COLLATE utf8_bin NOT NULL,
      `email` varchar(200) COLLATE utf8_bin NOT NULL, 
      `senha` varchar(16) COLLATE utf8_bin NOT NULL,
      `status` int NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

#print('Crio banco e tabelas...')

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      "INSERT INTO findtarget.Usuarios (nome, email, senha, status) VALUES (%s, %s, %s, %s)",
      [
            ('Rafael', 'rafaelvicent7@gmail.com', '1234', 1),
            ('Fabricio', 'fabs@gmail.com', 'fiotec', 1),
            ('Fernando', 'ferds@hotmail.com', '1010', 0),
            ('Marcio', 'argollo@gmail.com', '12345', 0)
      ])

#print('Populou usuarios')

cursor.execute('select * from findtarget.Usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo modelos
cursor.executemany(
      "INSERT INTO findtarget.Modelos_Executados (organismo, fba_result, arquivo_sbml, forma_analise, descricao, id_user) VALUES (%s, %s, %s, %s, %s, %s)",
      [
            ('Pseudomas Aeruginosas', '1.036524', 'arquivo_sbml3_ccbh4851', 'only FVA', 'teste inicial', 1),
            ('Pseudomas Aeruginosas', '1.036524', 'arquivo_sbml3_ccbh4851', 'only FVA', 'teste inicial', 2),
      ])

cursor.execute('select * from findtarget.Modelos_Executados')
print(' -------------  Modelos Executados:  -------------')
for model in cursor.fetchall():
    print(model[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()