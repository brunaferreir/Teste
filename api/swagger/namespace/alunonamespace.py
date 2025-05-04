from flask_restx import Namespace, Resource, fields
from aluno.modelAluno import AlunoNaoEncontrado, aluno_por_id, get_alunos, create_aluno, apaga_tudo, atualizarAluno, atualizarParcialAluno, deleteAluno

alunos_ns = Namespace("aluno", description="Dados relacionados aos alunos")

aluno_model = alunos_ns.model("Aluno", {
    "nome": fields.String(required=True, description="Nome do aluno"),
    "data_nascimento": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)"),
    "nota_primeiro_semestre": fields.Float(required=True, description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(required=True, description="Nota do segundo semestre"),
    "turma_id": fields.Integer(required=True, description="ID da turma"),
})

aluno_output_model = alunos_ns.model("AlunoOutput", {
    "id": fields.Integer(description="ID do aluno"),
    "turma_id": fields.Integer(required=True, description="ID da turma"),
    "nome": fields.String(required=True, description="Nome do aluno"),
    "idade": fields.Integer(required=True, description="Idade do aluno"),
    "data_nascimento": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)"),
    "nota_primeiro_semestre": fields.Float(required=True, description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(required=True, description="Nota do segundo semestre"),
    "media_final": fields.Float(required=True, description="Média final do aluno")

    
})


@alunos_ns.route("/")
class AlunosResource(Resource):
    @alunos_ns.marshal_list_with(aluno_output_model)
    def get(self):
        """Lista todos os alunos"""
        return get_alunos()

    @alunos_ns.expect(aluno_model)
    @alunos_ns.marshal_with(aluno_output_model, code=201, description='Aluno criado com sucesso')
    @alunos_ns.response(400, 'Erro de validação')
    def post(self):
        """Cria um novo aluno"""
        data = alunos_ns.payload
        response, status_code = create_aluno(data)
        return response, status_code

@alunos_ns.route("/<int:id_aluno>")
@alunos_ns.response(404, 'Aluno não encontrado')
class AlunoIdResource(Resource):
    @alunos_ns.marshal_with(aluno_output_model)
    def get(self, id_aluno):
        """Obtém um aluno pelo ID"""
        try:
            return aluno_por_id(id_aluno)
        except AlunoNaoEncontrado as e:
            alunos_ns.abort(404, str(e))

    @alunos_ns.expect(aluno_model)
    @alunos_ns.marshal_with(aluno_output_model, description='Aluno atualizado com sucesso')
    @alunos_ns.response(400, 'Erro de validação')
    @alunos_ns.response(404, 'Aluno não encontrado')
    @alunos_ns.response(500, 'Erro interno do servidor')
    def put(self, id_aluno):
        """Atualiza um aluno pelo ID"""
        data = alunos_ns.payload
        response, status_code = atualizarParcialAluno(id_aluno, data)
        return response, status_code

    @alunos_ns.response(200, 'Aluno excluído com sucesso')
    def delete(self, id_aluno):
        """Exclui um aluno pelo ID"""
        deleteAluno(id_aluno)
        return {"message": "Aluno excluído com sucesso"}, 200