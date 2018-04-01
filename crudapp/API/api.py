from flask import Flask, jsonify, request
import pymysql


app = Flask(__name__)
app.debug = True
config = {
  'user': 'crud_at_admin',
  'password': 'cruds_r_4_$tudds',
  'host': 'crud-rds.cilehwcmvw1z.us-west-2.rds.amazonaws.com',
  'database': 'products',
  'raise_on_warnings': True,
}


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/shoes/<int:shoe_id>')
def getShoeById(shoe_id):
    conn = pymysql.connect(host='crud-rds.cilehwcmvw1z.us-west-2.rds.amazonaws.com', port=3306, user='crud_at_admin', passwd='cruds_r_4_$tudds', db='products')
    cur = conn.cursor()
    cur.execute("SELECT * from ShoeCatalog where shoeid=\'{0}\'".format(shoe_id))
    return jsonify({'shoes': dictToJSON(cur.fetchall(), cur)})


@app.route('/products')
def pullCatalog():
    conn = pymysql.connect(host='crud-rds.cilehwcmvw1z.us-west-2.rds.amazonaws.com', port=3306, user='crud_at_admin', passwd='cruds_r_4_$tudds', db='products')
    cur = conn.cursor()
    cur.execute("SELECT * from ShoeCatalog")
    return jsonify({'shoes': dictToJSON(cur.fetchall(), cur)})


@app.route('/products/style/')
def pullCatologProductsWithAttributes():
    if(not bool(request.args)):
        return str([])
    conn = pymysql.connect(host='crud-rds.cilehwcmvw1z.us-west-2.rds.amazonaws.com', port=3306, user='crud_at_admin', passwd='cruds_r_4_$tudds', db='products')
    cur = conn.cursor()
    query = "SELECT * from ShoeCatalog where %s"
    preparedStatement = query % (' and '.join([('{0}=\'{1}\'').format(arg, request.args[arg]) for arg in request.args]))
    cur.execute(preparedStatement)
    return jsonify({'shoes': dictToJSON(cur.fetchall(), cur)})



def dictToJSON(data, cur):
    json = []

    for row in data:
        shoe_entry = {}
        for column, value in zip(cur.description,row):
            shoe_entry[column[0]] = value
        json.append(shoe_entry)

    return json
    

    






if __name__ == '__main__':
    app.run()