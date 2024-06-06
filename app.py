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
    #management = Management.query.all()
    dep_data = Depense.query.all()
    
    return render_template("index.html", rev_data=rev_data, dep_data=dep_data)
    


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

    table2 = Revenu.query.get_or_404(id)
    try:
        db.session.delete(table2)
        db.session.commit()
        return redirect("/")

    except Exception:
        return "Une erreur s'est produit"
    

@app.route("/calcul")
def operation():
    total_revenu = Revenu.query.all()
    total_depense = Depense.query.all()

    budget_s = 0
    spent_s = 0

    for revenue in total_revenu:
        budget_s+=revenue.amount_s
        

    for depenses in total_depense:
        spent_s+=depenses.amount
    

    solde_s = budget_s - spent_s
    
    try:
        management_s = Management(budget=budget_s, spent=spent_s, solde=solde_s)
        db.session.add(management_s)
        db.session.commit()
    except Exception as e:
        return f"Vous avez une erreur de type: {e}"
    management = Management.query.all()
    return render_template("index.html", management=management)#budget_s=budget_s, spent_s=spent_s, sum_solde=sum_solde)




if __name__ == "__main__":
    app.run(debug=True)



