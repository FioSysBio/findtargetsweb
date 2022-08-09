from models import Modelos_Execucao, Users

SQL_DELETA_MODELO = 'delete from Modelos_Executados where id = %s'

SQL_DELETA_MODELO_USUARIO = 'delete from Modelos_Executados where email_user = %s'

SQL_DELETA_CONTA = 'delete from Usuarios where id = %s'

SQL_MODELO_POR_ID = 'SELECT id, organismo, fba_result, arquivo_sbml, forma_analise, descricao, data_execucao, ' \
                    'email_user from Modelos_Executados where id = %s'

SQL_USUARIO_POR_ID = 'SELECT id, nome, email, senha, status, nivel, instituicao, token, validado from Usuarios where id = %s'

SQL_BUSCA_ID_USER_POR_EMAIL = 'SELECT id from Usuarios where email = %s'

SQL_USUARIO_POR_EMAIL = 'SELECT id, nome, email, senha, status, nivel, instituicao, token, validado from Usuarios where email = %s'

SQL_ATUALIZA_MODELO = 'UPDATE Modelos_Executados SET organismo=%s, fba_result=%s, arquivo_sbml=%s, forma_analise=%s,' \
                      'descricao=%s where id = %s'

SQL_ATUALIZA_USUARIO = 'UPDATE Usuarios SET nome=%s, email=%s, senha=%s, status=%s,' \
                       'nivel=%s, instituicao=%s, token=%s, validado=%s where id = %s'

SQL_ATUALIZA_PROFILE = 'UPDATE Usuarios SET nome=%s, email=%s, senha=%s, instituicao=%s where id = %s'

SQL_ALTERA_TOKEN = 'UPDATE Usuarios SET token=0, validado=1 where token = %s'

SQL_BUSCA_MODELOS = 'SELECT id, organismo, fba_result, arquivo_sbml, forma_analise, descricao, data_execucao, email_user ' \
                    'from Modelos_Executados'

SQL_BUSCA_MODELOS_EMAIL_USER = 'SELECT id, organismo, fba_result, arquivo_sbml, forma_analise, descricao, data_execucao, email_user ' \
                               'from Modelos_Executados WHERE email_user = %s'

SQL_BUSCA_CONTAS = 'SELECT id, nome, email, senha, status, nivel, instituicao, token, validado from Usuarios'

SQL_BUSCA_TOKEN = 'SELECT id, nome, email, senha, status, nivel, instituicao, token, validado from Usuarios where token = %s'

SQL_CRIA_MODELO = 'INSERT into Modelos_Executados (organismo, fba_result, arquivo_sbml, forma_analise, descricao, email_user) ' \
                  'values (%s, %s, %s, %s, %s, %s)'

SQL_BUSCA_EMAIL_ID_USER = 'SELECT email from Usuarios where id = %s'

SQL_CRIA_USUARIO = 'INSERT into Usuarios (nome, email, senha, status, nivel, instituicao, token, validado) ' \
                   'values (%s, %s, %s, %s, %s, %s, %s, %s)'


class ModeloDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, Modelo):
        cursor = self.__db.connection.cursor()

        if (Modelo.id):
            cursor.execute(SQL_ATUALIZA_MODELO,
                           (Modelo.organismo, Modelo.fba_result, Modelo.arquivo_sbml, Modelo.forma_analise,
                            Modelo.descricao, Modelo.email_user, Modelo.id))
        else:
            cursor.execute(SQL_CRIA_MODELO, (
            Modelo.organismo, Modelo.fba_result, Modelo.arquivo_sbml, Modelo.forma_analise, Modelo.descricao,
            Modelo.email_user))
            Modelo.id = cursor.lastrowid
        self.__db.connection.commit()
        return Modelo

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_MODELOS)
        modelos = traduz_modelos(cursor.fetchall())
        return modelos

    def listar_por_email(self, email):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_MODELOS_EMAIL_USER, (email,))
        modelos = traduz_modelos(cursor.fetchall())
        return modelos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_MODELO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Modelos_Execucao(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_MODELO, (id,))
        self.__db.connection.commit()

    def deletar_modelo_user(self, email_user):
        self.__db.connection.cursor().execute(SQL_DELETA_MODELO_USUARIO, (email_user,))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def salvar_user(self, Usuario):
        cursor = self.__db.connection.cursor()
        if (Usuario.id):
            cursor.execute(SQL_ATUALIZA_USUARIO, (Usuario.nome, Usuario.email, Usuario.senha, Usuario.status,
                                                  Usuario.nivel, Usuario.instituicao, Usuario.token, Usuario.validado,
                                                  Usuario.id))
        else:
            cursor.execute(SQL_CRIA_USUARIO, (Usuario.nome, Usuario.email, Usuario.senha, Usuario.status,
                                              Usuario.nivel, Usuario.instituicao, Usuario.token, Usuario.validado))
            Usuario.id = cursor.lastrowid
        self.__db.connection.commit()
        return Usuario

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_CONTA, (id,))
        self.__db.connection.commit()

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Users(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], id=tupla[0])

    def buscar_por_email(self, email):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_EMAIL, (email,))
        dados = cursor.fetchone()
        usuario = traduz_usuario_simple(dados) if dados else None
        return usuario

    def buscar_por_email_por_id_user(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_EMAIL_ID_USER, (id,))
        dados = cursor.fetchone()
        return dados

    def buscar_Token(self, token):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_TOKEN, (token,))
        dados = cursor.fetchone()
        usuario = traduz_usuario_simple(dados) if dados else None
        return usuario

    def atualiza_Token(self, token):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_ALTERA_TOKEN, (token,))
        self.__db.connection.commit()

    def listar_contas(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_CONTAS)
        contas = traduz_usuario(cursor.fetchall())
        return contas


def traduz_modelos(modelos):
    def cria_modelo_com_tupla(tupla):
        return Modelos_Execucao(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], id=tupla[0])

    return list(map(cria_modelo_com_tupla, modelos))


def traduz_usuario_simple(tupla):
    return Users(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], id=tupla[0])


def traduz_usuario(users):
    def cria_conta_com_tupla(tupla):
        return Users(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], id=tupla[0])

    return list(map(cria_conta_com_tupla, users))
