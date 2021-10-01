import mariadb
import dbcreds
from flask import Flask, request, Response
import json

cursor = None
conn = None

app= Flask(__name__)

@app.route('/animals', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def animal_handler():
    try:
        conn = mariadb.connect(
                        user=dbcreds.user,
                        password=dbcreds.password,
                        host=dbcreds.host,
                        port=dbcreds.port,
                        database=dbcreds.database
                        )
        cursor = conn.cursor()

        if request.method == 'GET':
            cursor.execute("SELECT animal_name FROM animals")
            resp = cursor.fetchall()
            if len(resp > 0):
                return Response(json.dumps(resp), mimetype="application/json", status=200)
            else:
                return Response("Data not found", mimetype="text/html", status=404) 

        elif request.method == 'POST':
            data = request.json
            req_animal = data.get("animal_name")
            if len(data) == 1:
                if len(req_animal) > 60:
                    return Response("Must have less than 60 characters", mimetype="text/html", status=400)
                elif len(req_animal) == 0:
                    return Response("Empty request", mimetype="text/html", status=400)
                else:
                    cursor.execute("SELECT animal_name FROM animals")
                    animal_list = cursor.fetchall()
                    if req_animal in str(animal_list):
                        return Response("This animal already exists in the database", mimetype="text/html", status=403)
                    else:
                        cursor.execute("INSERT INTO animals(animal_name) VALUES(?)", [req_animal])
                        conn.commit()
                        return Response("Success!", mimetype="text/html", status=200)
            elif data == None:
                return Response("Must include some data to post", mimetype="text/html", status=400)
            elif len(data) > 1:
                return Response("Only one entry at a time", mimetype="text/html", status=400)
            else:
                return Response("Something went wrong", mimetype="text/html", status=500)

        elif request.method == 'PATCH':
            data = request.json
            req_id = data.get("id")
            req_animal = data.get("animal_name")
            if len(data) == 2:
                if len(req_animal) > 60:
                    return Response("Must have less than 60 characters", mimetype="text/html", status=400)
                elif len(req_animal) == 0:
                    return Response("Empty request", mimetype="text/html", status=400)
                elif len(req_id) == 0:
                    return Response("Empty request", mimetype="text/html", status=400)
                else:
                    cursor.execute("SELECT * FROM animals")
                    animal_list = cursor.fetchall()
                    if req_animal in str(animal_list):
                        return Response("This animal already exists in the database", mimetype="text/html", status=403)
                    elif req_id not in str(animal_list):
                        return Response('There is not animal matching that id', mimetype="text/html", status=404)
                    else:
                        cursor.execute("UPDATE animals SET animal_name=? WHERE id=?", [req_animal, req_id])
                        conn.commit()
                        return Response("Success!", mimetype="text/html", status=200)
            else:
                return Response("Incorrect data sent over. Requires two parameters", mimetype="text/html", status=400)
        elif request.method == 'DELETE':
            data = request.json
            req_animal = data.get("animal_name")
            if len(data) == 1:
                if len(req_animal) > 60:
                    return Response("Must have less than 60 characters", mimetype="text/html", status=400)
                elif len(req_animal) == 0:
                    return Response("Empty request", mimetype="text/html", status=400)
                else:
                    cursor.execute("SELECT * FROM animals")
                    animal_list = cursor.fetchall()
                    if req_animal not in str(animal_list):
                        return Response("This animal does not exist in the database, we cannot delete something that doesnt exist", mimetype="text/html", status=404)
                    else:
                        cursor.execute("DELETE FROM animals WHERE animal_name=?", [req_animal])
                        conn.commit()
                        return Response("Success!", mimetype="text/html", status=200)
            elif data == None:
                return Response("Must include some data to post", mimetype="text/html", status=400)
            elif len(data) > 1:
                return Response("Only one entry at a time", mimetype="text/html", status=400)
            else:
                return Response("Something went wrong", mimetype="text/html", status=500)

        else:
            print("Something went wrong, bad request method")
    
    except mariadb.DataError:
        print("Something is wrong with your data")
        return Response("Something is wrong with the data", status=404)
    except mariadb.OperationalError:
        print("Something is wrong with your connection")
        return Response("Something is wrong with the connection", status=500)
    except:
        print("Something went wrong")
        return Response("Something went wrong", status=500)
    finally:
        if (cursor != None):
            cursor.close()
        if (conn != None):
            conn.rollback()
            conn.close()