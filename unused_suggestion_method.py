# Unused suggestion generator
def addSugesstions():
    if current_user.is_authenticated:
        uname=current_user.Username 
    else:
        flash("Sorry but you are not logged in yet !!")
        return redirect('/login')    
    user_id = Users.query.filter_by(Username = uname).first().id
    
    already_Sugg = Suggested.query.filter_by(UserID = user_id).delete()
    db.session.commit() 

    industry_preferences = IndustryPreferences.query.filter_by(User_ID = user_id).all()
    stock_preferences = StockPreferences.query.filter_by(User_ID = user_id).all()
    
    for preference in industry_preferences:
        companies = Companies.query.filter_by(IndustryName = preference.IndustryName).all()
        for comp in companies:
            sugg = Suggested(comp.CompanyID, user_id, 1)
            db.session.add(sugg)
           
    db.session.commit() 
    
    for preference in stock_preferences:
        companies = Companies.query.filter_by(StockType = preference.StockType).all()
        for comp in companies:
            if Suggested.query.filter_by(UserID = user_id, CompanyID = comp.CompanyID).first():
                Suggested.query.filter_by(UserID = user_id, CompanyID = comp.CompanyID).first().SuggestMetric = 2
            else:
                sugg = Suggested(comp.CompanyID, user_id, 1)
                db.session.add(sugg)
                
    db.session.commit()
    
    return 1