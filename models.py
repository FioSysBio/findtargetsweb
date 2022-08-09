class Modelos_Execucao: #add um id para o modelo identificar na tabela de resultados
    def __init__(self, organismo, fba_result, arquivo_sbml, forma_analise, descricao, data_exec, email_user, id=None):
        self.id = id
        self.organismo = organismo
        self.fba_result = fba_result
        self.arquivo_sbml = arquivo_sbml
        self.forma_analise = forma_analise
        self.descricao = descricao
        self.data_exec = data_exec
        self.email_user = email_user
#
class Users: #add id para relacionar a um modelo executado
    def __init__(self, nome, email, senha, status, nivel, instituicao, token, validado, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.status = status
        self.nivel = nivel
        self.instituicao = instituicao
        self.token = token
        self.validado = validado