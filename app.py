from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budgetmanager.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)    #connexion de l'appli avec la base de données


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
        budget+=revenue.amount

    for depense in dep_data:
        spent+=depense.amount

    solde = budget - spent 
    try:
        gestion = Management(budget=budget, spent=spent, solde=solde)
        db.session.add(gestion)
        db.session.commit()
    except Exception:
        return "Erreur lors de l'ajout à la base de données"

    return render_template("index.html", rev_data=rev_data, dep_data=dep_data, budget=budget, spent=spent, solde=solde)
    


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
                
                return redirect("/page2")
            
            except Exception :
                return "Une erreur s'est produit"

    return render_template("revenu.html")  



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
              
                return redirect("/page3")

            except Exception :
                return "Une erreur s'est produit"

    return render_template("depense.html")  

   

@app.route("/delete/<int:id>/")
def delete(id):
    table1 = Revenu.query.get_or_404(id)   
    table2 = Depense.query.get_or_404(id)  
      
    try:
        db.session.delete(table1)
        db.session.delete(table2)

        db.session.commit()

        return redirect("/")

    except Exception:
        return "Une erreur s'est produit"
    

@app.route("/update<int:id>/", methods=["GET", "POST"])
def update(id):
    reve = Revenu.query.get_or_404(id)
    if request.method == "POST":
        reve.title=request.form["title"]
        reve.amount=request.form["amount"]

        try:
            db.session.commit()
            return redirect("/")
        
        except Exception:
            print("erreur")

    return render_template("update.html", reve=reve)
    

if __name__ == "__main__":
    app.run(debug=True)



