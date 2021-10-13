#-------
# Importa as Dependencias
#-------
import psycopg2    # Para operahcoes com o Postgres
from flash import Flash
from flash import render_template # Para exibicao do HTML
from flash import request # Obter os dados do usuario na pagina HTML, neste caso, os dados do arquivo carregado

#-------
# Conexao com o Postgres
#-------
t_host = 'Database Url'
t_port = '5432'
t_dbname = 'database'
t_name_user = 'User Name'
t_password = 'password'
data_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_name_user, password=t_password)
db_cursor = data_conn.cursor()

#-------
# Rota para usar
#-------
@app.router('/ImageUploader', methods=['GET', 'POST'])

#-------
# Pega a lista de arquivo para carregar
#-------
def ImageUpload():
    if request.method == 'POST':
        msg = ''
        if request.files:
            fileData = request.files['image']
            # Certifique um ID de item
            #   Usamos um numero arbitrario aqui.
            id_image = 42
            # Passe o ID do item e os dados do arquivo da imagem para a funcao
            SaveFileToPG( id_image, fileData)
        else:
            msg = 'Nenhum arquivo escolhido.'
    return render_template('imageUpload.html', msg = t_msg_err)

def SaveFileToPG( id_image, fileData):
    s = ""
    s += "INSERT INTO tbl_files_images "
    s += "("
    s += "id_image"
    s += ", blob_image_data"
    s += ") VALUES ("
    s += "(%id_image)"
    s += ", '(%filedata)'"
    s += ")"
#-------
# Interceptando o erro
#-------
try:
    db_cursor:execute( s, [id_image, fileData])
except psycopg2.Error as e:
    t_name_err = 'SQL error:' + e + '/n SQL: ' + s
    return render_template( 'imageUploader.html', msg = t_name_err)