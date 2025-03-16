#CRUD

# Professores;
# get - todos os professores
# get id  - um professor

# post - criar novo professor

# delete - todos os professores
# delete id -um professor

# put - atualizar professor
# path - 

#-----------------------------------------------------------

# Alunos;
# get - todoos os alunos
# get id  - um aluno

# post - criar novo aluno

# delete - todos os alunos
# delete id -um aluno

# put - atualizar aluno
# path - 

#-----------------------------------------------------------

# Turmas
# get - todas as turmas
# get id  - uma turma

# post - criar nova turma

# delete - todos as turmas
# delete id - uma turma

# put - atualizar turma
# path - 

from flask import Flask, jsonify, request

class AlunoNaoEncontrado(Exception):
    pass

dici = {
    "alunos":[
        {"id":1,"nome":"Joao"}
       ,{"id":2,"nome":"Maria"}
       ,{"id":3,"nome":"Pedro"} 
],
    "professores":[
        {"id":1,"nome":"carlos", "idade":30, "materia":"matematica", "observacao":"bom professor"}
        ,{"id":2,"nome":"lucas", "idade":34, "materia":"POO", "observacao":"bom professor"} 
        ],
    "turmas":[
        {"id":1,"descricao":"turma1", "professor_id":1,"ativo":True}
              ]
}

def aluno_por_id(id_aluno):
    for aluno in dici['alunos']:
        if aluno['id'] == id_aluno:
            return aluno
    raise AlunoNaoEncontrado

app = Flask(__name__)

#ALUNOS

#GET

@app.route('/alunos', methods=['GET'])
def get_alunos():
    dados = dici['alunos']
    return jsonify(dados)

#GET ID

@app.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return jsonify(aluno), 200  
    except AlunoNaoEncontrado:
        return jsonify({'erro': 'aluno nao encontrado'}), 404


#POST

# @app.route('/alunos', methods=['POST'])
# def create_aluno(): 
#       dados = request.json
#       dici['alunos'].append(dados)
#       return jsonify(dados), 201 

# @app.route('/alunos', methods=['POST'])
# def create_aluno():
#     dados = request.json
#     id_aluno = dados.get('id')
#     nome_aluno = dados.get('nome')
    
#     if not nome_aluno:
#         return jsonify({'erro': 'aluno sem nome'}), 400

#      # Verifica se o ID já existe
#     for aluno in dici['alunos']:
#         if aluno['id'] == id_aluno:
#             return jsonify({'erro': 'id ja utilizada'}), 400  

#     # Adiciona o novo aluno
#     dici['alunos'].append(dados)
#     return jsonify(dados), 201



# @app.route('/alunos', methods=['POST'])
# def create_aluno(): 
#       dados = request.json
#       dici['alunos'].append(dados)
#       return jsonify(dados), 201 

# @app.route('/alunos', methods=['POST'])
# def create_aluno():
#     dados = request.json
#     id_aluno = dados.get('id')
#     nome_aluno = dados.get('nome')
    
#     if not nome_aluno:
#         return jsonify({'erro': 'aluno sem nome'}), 400

#      # Verifica se o ID já existe
#     for aluno in dici['alunos']:
#         if aluno['id'] == id_aluno:
#             return jsonify({'erro': 'id ja utilizada'}), 400  

#     # Adiciona o novo aluno
#     dici['alunos'].append(dados)
#     return jsonify(dados), 201




@app.route('/alunos', methods=['POST'])
def create_aluno():
    dados = request.json
    if not dados:
        return jsonify({'erro': 'Dados inválidos'}), 400

    id_aluno = dados.get('id')
    nome_aluno = dados.get('nome')

    # Validação da presença do nome DEVE vir primeiro
    if not nome_aluno:
        return jsonify({'erro': 'aluno sem nome'}), 400

    # Validação de tipos
    if not isinstance(id_aluno, int):
        return jsonify({'erro': 'O id deve ser um número inteiro'}), 400
    if not isinstance(nome_aluno, str):
        return jsonify({'erro': 'O nome deve ser uma string'}), 400

    # Verifica se o ID já existe
    for aluno in dici['alunos']:
        if aluno['id'] == id_aluno:
            return jsonify({'erro': 'id ja utilizada'}), 400

    # Adiciona o novo aluno
    dici['alunos'].append(dados)
    return jsonify(dados), 201







#RESET

@app.route('/reseta', methods=['POST'])
def reseta():
    dici["alunos"] = []
    return jsonify({"message": "Banco de dados resetado"}), 200

#PUT ID

# def aluno_por_id(id_aluno):
#     for aluno in dici['alunos']:
#         if aluno['id'] == id_aluno:
#             return aluno
#     raise AlunoNaoEncontrado


# @app.route('/alunos/<int:id_aluno>', methods=['PUT'])
# def update_aluno(id_aluno):
#      dados = request.json
#      nome_aluno = dados.get('nome')
    
#      if not nome_aluno:
#         return jsonify({'erro': 'aluno sem nome'}), 400

#      try:
#         aluno = aluno_por_id(id_aluno)
#         aluno.update(dados)  
#         return jsonify(aluno), 200   
#      except AlunoNaoEncontrado:
#          return jsonify({'erro': 'aluno nao encontrado'}), 404
     



@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def update_aluno(id_aluno):
    dados = request.json
    if not dados:
        return jsonify({'erro': 'Dados inválidos'}), 400

    nome_aluno = dados.get('nome')
    id_novo = dados.get('id')

    if not nome_aluno:
        return jsonify({'erro': 'aluno sem nome'}), 400

    # Validação de tipos
    if id_novo is not None and not isinstance(id_novo, int):
        return jsonify({'erro': 'O id deve ser um número inteiro'}), 400
    if not isinstance(nome_aluno, str):
        return jsonify({'erro': 'O nome deve ser uma string'}), 400

    try:
        aluno = aluno_por_id(id_aluno)
        # Atualiza apenas se as chaves existirem nos dados recebidos
        if 'nome' in dados:
            aluno['nome'] = nome_aluno
        if 'id' in dados:
            aluno['id'] = id_novo
        return jsonify(aluno), 200
    except AlunoNaoEncontrado:
        return jsonify({'erro': 'aluno nao encontrado'}), 404






#PATCH ID

@app.route('/alunos/<int:id_aluno>', methods=['PATCH'])
def patch_aluno(id_aluno):
    dados = request.json
    try:
        aluno = aluno_por_id(id_aluno)
        for chave, valor in dados.items():
            aluno[chave] = valor
        return jsonify(aluno), 200
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404



#DELETE ID

@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        dici['alunos'].remove(aluno)
        return 'aluno deletado', 204
    except AlunoNaoEncontrado:
         return jsonify({'erro': 'aluno nao encontrado'}), 404

#DELETE TUDO   

@app.route('/alunos', methods=['DELETE'])
def delete_alunos():
    dici['alunos'] = []
    return 'alunos deletados', 204






#-----------------------------------------------------------------------------------------------

#PROFESSORES

class ProfessorNaoEncontrado(Exception):
    pass


def professor_por_id(professor_id):
    for professor in dici['professores']:
        if professor['id'] == professor_id:
            return professor
    raise ProfessorNaoEncontrado


#GET

@app.route('/professores', methods=['GET'])
def get_professores():
    dados = dici['professores']
    return jsonify(dados)

# #GET ID

@app.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        
        professor = professor_por_id(id_professor)
        return jsonify(professor), 200  
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404


# #POST

@app.route('/professores', methods=['POST'])
def create_professores(): 
      dados = request.json
      dici['professores'].append(dados)
      return jsonify(dados), 201   

 

# # #RESET

# @app.route('/reseta', methods=['POST'])
# def reseta():
#     dici["professores"] = []
#     return jsonify({"message": "Banco de dados resetado"}), 200

# #PUT ID

@app.route('/professores/<int:id_professor>', methods=['PUT'])
def update_professor(id_professor):
     dados = request.json
     try:
        professor = professor_por_id(id_professor)
        professor.update(dados)  
        return jsonify(professor), 200   
     except ProfessorNaoEncontrado:
         return jsonify({'message': 'Professor não encontrado'}), 404
     

# #PATCH ID

@app.route('/professores/<int:id_professor>', methods=['PATCH'])
def patch_professor(id_professor):
    dados = request.json
    try:
        professor = professor_por_id(id_professor)
        for chave, valor in dados.items():
            professor[chave] = valor
        return jsonify(professor), 200
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404



# #DELETE ID

@app.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_profesor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        dici['professores'].remove(professor)
        return 'professor deletado', 204
    except ProfessorNaoEncontrado:
         return jsonify({'message': 'Professor não encontrado'}), 404


# #DELETE TUDO   

@app.route('/professores', methods=['DELETE'])
def delete_professores():
    dici['professores'] = []
    return 'professores deletados', 204




if __name__ == '__main__':
    app.run(debug=True)







