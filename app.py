from flask import Flask, request, render_template, redirect,  url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budgetmanager.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)    


class Management(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Integer(), nullable=False)
    spent = db.Column(db.Integer(), nullable=False)
    solde = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f"{self.budget} {self.spent} {self.solde}"


class Revenu(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    amount = db.Column(db.Integer(), nullable=False)
    
    def __repr__(self):
        return f"{self.title} {self.amount}"


class Depense(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    amount = db.Column(db.Integer(), nullable=False)
    
    def __repr__(self):
        return f"{self.title} {self.amount}"
    


@app.route("/") 
def index():
    rev_data = Revenu.query.all() 
    dep_data = Depense.query.all()

    budget = 0
    spent = 0
    for revenue in rev_data:
        budget+=revenue.amount  #Incrementation_pour_obtenir_la_somme_total_des_revenus

    for depense in dep_data:    
        spent+=depense.amount   #Incrementation_pour_obtenir_la_somme_total_des_depenses

    solde = budget - spent   #OPERATION_DIFFERENCE _ENTRE8_TOTAL_REVENU_ET_TOTAL_DEPENSE
    
    try:
        gestion = Management(budget=budget, spent=spent, solde=solde)
        db.session.add(gestion)
        db.session.commit()
    except Exception:
        return "Erreur: données on ajouter à la base de données"

    return render_template("index.html", rev_data=rev_data, dep_data=dep_data, budget=budget, spent=spent, solde=solde)
    

#REVENU
@app.route("/page2", methods=["GET", "POST"])
def table_revenu():
    if request.method == "POST" :           
        title = request.form["title"]       
        amount = request.form["amount"]     
        type_data = request.form["type_data"]

        if type_data == "revenu":
            try:
                table1 = Revenu(title=title, amount=amount) 
                db.session.add(table1)    
                db.session.commit() 
                
                return redirect(url_for('table_revenu'))
            
            except Exception :
                return "Une erreur s'est produit"

    return render_template("revenu.html")  


#DEPENSE
@app.route("/page3", methods=["GET", "POST"])
def table_depense():
    if request.method == "POST" :           
        title = request.form["title"]       
        amount = request.form["amount"]
        type_data = request.form["type_data"]
        
        if type_data == "depense":
            try:
                table2 = Depense(title=title, amount=amount) 
                db.session.add(table2)      
                db.session.commit()   
              
                return redirect(url_for('table_depense'))

            except Exception :
                return "Une erreur s'est produit"

    return render_template("depense.html")  

   
#DELETE_REVENU
@app.route("/delete_revenu/<int:id>/")
def delete_revenu(id):
    table1 = Revenu.query.get_or_404(id)
    
    try:
        db.session.delete(table1)
        db.session.commit()
        return redirect(url_for('index'))  
    except Exception:
        return "---Erreur---"


#DELETE_DEOPENSE
@app.route("/delete_depense/<int:id>/")
def delete_depense(id):
    table2 = Depense.query.get_or_404(id)
    
    try:
        db.session.delete(table2)
        db.session.commit()
        return redirect(url_for("index"))
    except Exception:
        return "---Erreur---"

if __name__ == "__main__":
    app.run(debug=True)