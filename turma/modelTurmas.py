from config import db

class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(100))
    professor_id = db.Column(db.Integer, db.ForeignKey("professor.id"), nullable=False)
    ativo = db.Column(db.Boolean)
    #professor = db.relationship("Professor", back_populates="turmas")

    def __init__(self, descricao):
        self.descricao = descricao

    def to_dict(self):
        professor_data = None
        if self.professor:
            professor_data = {
                'id': self.professor.id,
                'descricao': self.professor.descricao,
                
            }
        return {'id': self.id,
               'descricao': self.descricao,
               'professor': professor_data,
               'ativo': self.ativo}


class TurmaNaoEncontrada(Exception):
    pass


def turma_por_id(idTurma):
    turma = Turma.query.get(idTurma)

    if not turma:
        raise TurmaNaoEncontrada("Turma não encontrada")
    return turma.to_dict()

def getTurma():
    turmas = Turma.query.all()
    return [turma.to_dict() for turma in turmas]

def apaga_tudo():
    try:
        db.session.query(Turma).delete()
        db.session.commit()
        return "message: Banco de dados resetado"
    except Exception as e:
        db.session.rollback()
        return f"Erro ao resetar o banco de dados: {e}"

def createTurma(descricao, professor):
    if not descricao or not professor:
        return {'erro': 'Parâmetro obrigatório ausente'}

    if not isinstance(descricao, str):
        return {'erro': 'O descricao deve ser uma string'}

    if not isinstance(professor, str):
        return {'erro': 'O professor deve ser uma string'}

    nova_turma = Turma(descricao=descricao, professor=professor)
    db.session.add(nova_turma)
    db.session.commit()
    return nova_turma.to_dict(), 201


def deleteTurma(idTurma):
    turma = Turma.query.get(idTurma)
    if not turma:
        raise TurmaNaoEncontrada
    db.session.delete(turma)
    db.session.commit()
    return 'mensagem: Turma deletada com sucesso', turma


def atualizarTurma(idTurma, descricao=None, professor=None):
    try:
        turma_encontrada = Turma.query.get(idTurma)
        if turma_encontrada is None:
            raise TurmaNaoEncontrada("Turma não encontrada")

        if descricao is None and professor is None:
            return 'erro: Pelo menos um dos campos "descricao" ou "professor" deve ser fornecido', None

        if descricao and not isinstance(descricao, str):
            return 'erro: O descricao deve ser uma string', None
        if professor and not isinstance(professor, str):
            return 'erro: O professor deve ser uma string', None

        if descricao:
            turma_encontrada.descricao = descricao
        if professor:
            turma_encontrada.professor = professor

        db.session.commit()

        return "mensagem: Turma atualizada com sucesso", turma_encontrada.to_dict()

    except Exception as e:
        db.session.rollback()
        return f"erro: {str(e)}", None


def atualizarParcialTurma(idTurma, dados):
    try:
        turma_encontrada = Turma.query.get(idTurma)
        if turma_encontrada is None:
            raise TurmaNaoEncontrada("Turma não encontrada")

        for chave, valor in dados.items():
            if hasattr(turma_encontrada, chave):
                setattr(turma_encontrada, chave, valor)

        db.session.commit()
        return "mensagem: Turma atualizada com sucesso", turma_encontrada.to_dict()

    except Exception as e:
        db.session.rollback()
        return f"erro: {str(e)}", None

# print(turma_por_id(28))
# print(getTurma())
# print(createTurma(2,'ads','caio'))
# print(deleteTurma(1))
# print(atualizarTurma(28, nome='bd', professor=None))
# print(atualizarParcialTurma(2,{'professor':'luana'}))
