from flask import Flask
from EventHandler import EventHandler  # Import your event handler class
from DatabaseManager import DatabaseManager # Import your DatabaseManager class
from flask_login import LoginManager
from db_schema import db, dbinit

from flask import Blueprint, request, redirect, render_template, session, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash


from datetime import datetime
from datetime import date
from datetime import time
import time
from base64 import b64encode
from functools import reduce


def run_app():
    database_manager = DatabaseManager(db=db)

    # Initialize Flask app 
    app = create_app()

    # Initialize EventHandler with the same DatabaseManager instance
    event_handler = EventHandler(database_manager)

    # Run the Flask app (make sure this runs in the main thread)
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    run_app()

def create_app():

    app = Flask(__name__)
    db_manager = DatabaseManager(db=db)
    
    # Initialize and configure your DatabaseManager here
    # For example:

    # Register blueprints
    @app.route('/')
    def firstwelcome():
        uname=None
        if current_user.is_authenticated:
            uname=current_user.Username 
            return redirect('/welcome')
        
        stocks = db_manager.get_top_yield_comp(6)
        first_three = stocks[:3]
        next_three = stocks[3:5]
    
        complogolist = []   


        for comp in stocks:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]
        

        news = db_manager.get_news_desc(limit=7)
        
        newsimglist = []   


        for new in news:  
            newsimglist += [{'nid':new.NewsID, 'nimg':b64encode(new.Photo).decode("utf-8")}]
            
        topcompscroll = db_manager.get_topcompscroll()
    
        return render_template('firstentry.html', topcompscroll=topcompscroll, uname=uname, complogolist=complogolist, first_three=first_three, next_three=next_three, news=news, newsimglist=newsimglist)

    @app.route('/logout2')
    def logout2():

        # for a single item
        # either
        # 1. delete the username from the session (Error if the key isn't there)
        try:
            del session['username']
        except KeyError:
            pass

        # 2. pop the username (None is returned if key isn't there)
        session.pop('username',None)

        # otherwise you might want to clear the session data (all of it!)
        session.clear()

        # a go back to the home page
        flash('You have been successfully logged out')
        return redirect('/alllist.html')

    @app.route('/logout')
    def logout():

        logout_user()
        return redirect('/welcome')


    @app.route('/company.html/<int:companyID>')
    def companyzoom(companyID):
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id = db_manager.get_user(uname).id
        
        company = db_manager.get_company(company_id=companyID)
        print(company.CompanyID)
        print(company.Name)
        
        complogo = company.Logo
        logo = b64encode(complogo).decode("utf-8")
        
        industry = company.IndustryName
        stock = company.StockType

        followed = 0
        
        newslist = db_manager.get_comp_news_desc(company_id=companyID, limit=7)
        
        newsimglist = []   


        for news in newslist:
            newsimglist += [{'nid':news.NewsID, 'nimg':b64encode(news.Photo).decode("utf-8")}]
        
        similarlist1 = db_manager.get_top_priced_comp_inds(industry=industry, limit=2)
        similarlist2 = db_manager.get_top_priced_comp_stock(stock_type=stock, limit=3)
        
        # Step 1: Create a set of primary keys from similarlist1
        company_ids_in_list1 = set(companyeg.CompanyID for companyeg in similarlist1)

        # Step 2: Iterate over similarlist2 and combine lists avoiding repetitions
        combined_list = []
        for companyeg in similarlist2:
            if companyeg.CompanyID not in company_ids_in_list1:
                combined_list.append(companyeg)

        # Step 3: Return the combined list
        combined_list = similarlist1 + combined_list
        
        combined_list = [companyeg for companyeg in combined_list if companyeg.CompanyID != companyID]
        
        complogolist = []   

        for comp in combined_list:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]
        
        
        if uname is not None:
            userid = db_manager.get_user(uname).id
            
            if db_manager.is_followed(company_id=companyID, user_id=userid):
                followed = 1
                
        followeds = db_manager.get_followed(user_id=user_id)
        
        follow_list = []

        for followed in followeds:
            foll = db_manager.get_company(company_id=followed.CompanyID).CompanyID
            if foll:
                follow_list.append(foll)
                
        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)
        print(notifications)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        topcompscroll = db_manager.get_topcompscroll()
            
        return render_template('/company.html', topcompscroll=topcompscroll, updatecount=len(updates), updates=updates, follow_list=follow_list, company=company, uname=uname, time=time, date=date, datetime=datetime, followed=followed, newslist=newslist, similarlist1=combined_list, similarlist2=similarlist2, newsimglist=newsimglist, complogolist=complogolist, logo=logo)

    @app.route('/alllist.html')
    def allcompanies():
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id = db_manager.get_user(uname).id
        
        company = db_manager.get_all_companies()
            
        complogolist = []   

        for comp in company:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]

        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)
        print(notifications)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        followeds = db_manager.get_followed(user_id=user_id)
        
        follow_list = []

        for followed in followeds:
            foll = db_manager.get_company(company_id=followed.CompanyID).CompanyID
            if foll:
                follow_list.append(foll)
                
        print(follow_list)
        
        industry_list = db_manager.get_all_industries()
        stock_list = db_manager.get_all_stock_types()
        
        topcompscroll = db_manager.get_topcompscroll()
        
        return render_template('/alllist.html', topcompscroll=topcompscroll, compcount=len(company), industry_list=industry_list, stock_list=stock_list, follow_list=follow_list ,updatecount=len(updates), updates=updates, company=company, uname=uname, time=time, date=date, datetime=datetime, complogolist=complogolist)

    @app.route('/toplist.html')
    def topcompanies():
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id = db_manager.get_user(uname).id
        
        company = db_manager.get_top_perc_change(limit=10)
            
        complogolist = []   


        for comp in company:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]

        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)
        print(notifications)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        followeds = db_manager.get_followed(user_id=user_id)
        
        follow_list = []

        for followed in followeds:
            foll = db_manager.get_company(company_id=followed.CompanyID).CompanyID
            if foll:
                follow_list.append(foll)
                
        print(follow_list)
        
        industry_list = db_manager.get_all_industries()
        stock_list = db_manager.get_all_stock_types()
        
        topcompscroll = db_manager.get_topcompscroll()
        
        return render_template('/toplist.html', topcompscroll=topcompscroll, compcount=len(company), industry_list=industry_list, stock_list=stock_list, follow_list=follow_list ,updatecount=len(updates), updates=updates, company=company, uname=uname, time=time, date=date, datetime=datetime, complogolist=complogolist)


    @app.route('/followed.html')
    def followedcompanies():
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id=db_manager.get_user(uname).id
        else:
            flash("Sorry but you are not logged in yet !!")
            return redirect('/login')

        firstname = db_manager.get_user(uname).FirstName

        follow_link = db_manager.get_followed(user_id=user_id)
        
        follow_comp = []

        for followed in follow_link:
            foll = db_manager.get_company(company_id=followed.CompanyID)
            if foll:
                follow_comp.append(foll)
                
        complogolist = []

        for comp in follow_comp:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]

        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)
        print(notifications)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        followeds = db_manager.get_followed(user_id=user_id)
        
        follow_list = []

        for followed in followeds:
            foll = db_manager.get_company(company_id=followed.CompanyID).CompanyID
            if foll:
                follow_list.append(foll)
                
        print(follow_list)
        
        industry_list = db_manager.get_all_industries()
        stock_list = db_manager.get_all_stock_types()
        
        topcompscroll = db_manager.get_topcompscroll()
        
        return render_template('/followed.html', topcompscroll=topcompscroll, firstname=firstname, compcount=len(follow_comp), industry_list=industry_list, stock_list=stock_list, follow_list=follow_list ,updatecount=len(updates), updates=updates, company=follow_comp, uname=uname, time=time, date=date, datetime=datetime, complogolist=complogolist)

    @app.route('/searchfollowed', methods=['POST'])
    def search_followed_company():
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id = db_manager.get_user(uname).id

        firstname = db_manager.get_user(uname).FirstName
        
        follow_link = db_manager.get_followed(user_id=user_id)
        
        follow_comp = []

        for followed in follow_link:
            foll = db_manager.get_company(company_id=followed.CompanyID)
            if foll:
                follow_comp.append(foll)
                
        searchstring = request.form['search']
        
        if searchstring is None:
            company = follow_comp
            
        else:
            search_paramater = str('%') + str(searchstring) + str('%')
            
            follow_comp2 = []

            for followed in follow_link:
                foll = db_manager.is_name_in_search(company_id=followed.CompanyID, search_paramater=search_paramater)
                if foll:
                    follow_comp2.append(foll)
                    
            company = follow_comp2
        
        industry_list = db_manager.get_all_industries()
        stock_list = db_manager.get_all_stock_types()
        
        complogolist = []   

        for comp in company:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]

        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        followeds = db_manager.get_followed(user_id=user_id)
        
        follow_list = []

        for followed in followeds:
            foll = db_manager.get_company(company_id=followed.CompanyID).CompanyID
            if foll:
                follow_list.append(foll)
                
        topcompscroll = db_manager.get_topcompscroll()
                    
        return render_template('/followed.html', topcompscroll=topcompscroll, firstname=firstname, industry_list=industry_list, stock_list=stock_list, follow_list=follow_list ,updatecount=len(updates), updates=updates, company=company, compcount=len(company), uname=uname, time=time, date=date, datetime=datetime, complogolist=complogolist)

    @app.route('/submitfollowed', methods=['POST'])
    def filter_followed_company():
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id = db_manager.get_user(uname).id

        firstname = db_manager.get_user(uname).FirstName
        
        follow_link = db_manager.get_followed(user_id=user_id)
        
        follow_comp = []

        for followed in follow_link:
            foll = db_manager.get_company(company_id=followed.CompanyID)
            if foll:
                follow_comp.append(foll)
        
        industry_list = db_manager.get_all_industries()
        stock_list = db_manager.get_all_stock_types()
        
        industry_filtered_company_list = []
        stock_filtered_company_list = []
        posichange_company_list = []
        posiop_company_list = []
        
        searchstring = request.form['search3']
        
        if searchstring is "":
            companies = []
            
        else:
            search_paramater = str('%') + str(searchstring) + str('%')
            
            follow_comp2 = []

            for followed in follow_link:
                foll = db_manager.is_name_in_search(company_id=followed.CompanyID, search_paramater=search_paramater)
                if foll:
                    follow_comp2.append(foll)
                    
            companies = follow_comp2
        
        for industry in industry_list:
            if industry.IndustryName in request.form:
                print(industry.IndustryName)
                for followed in follow_link:
                    foll = db_manager.is_comp_in_industry(company_id=followed.CompanyID, industry_name=industry.IndustryName)
                    if foll:
                        industry_filtered_company_list.append(foll)
        
        for stocktp in stock_list:
            if stocktp.StockType in request.form:
                for followed in follow_link:
                    foll = db_manager.is_comp_in_stock(company_id=followed.CompanyID, stock_type=stocktp.StockType)
                    if foll:
                        stock_filtered_company_list.append(foll)
                        
        if 'posichnge' in request.form:
            for followed in follow_link:
                foll = db_manager.is_comp_posichnge(company_id=followed.CompanyID)
                if foll:
                    posichange_company_list.append(foll)

        if 'posiop' in request.form:
            for followed in follow_link:
                foll = db_manager.is_comp_posiop(company_id=followed.CompanyID)
                if foll:
                    posiop_company_list.append(foll)
                    
        print(industry_filtered_company_list)
        print(stock_filtered_company_list)
        
        # Define the list of lists
        lists_of_companies = [industry_filtered_company_list, stock_filtered_company_list, posichange_company_list, posiop_company_list]
        print(lists_of_companies)
        # Filter out empty lists
        non_empty_lists = [company_list for company_list in lists_of_companies if company_list]
        print(non_empty_lists)
        # Extract CompanyIDs from each non-empty list
        non_empty_sets = [set(companyeg.CompanyID for companyeg in company_list) for company_list in non_empty_lists]
        print(non_empty_sets)
        # Find the intersection of sets if there are non-empty lists
        if non_empty_sets:
            intersection_set = reduce(lambda x, y: x.intersection(y), non_empty_sets)
        else:
            intersection_set = set()

        print(intersection_set)
        # Retrieve Company objects corresponding to the CompanyIDs in the intersection set
        combined_list_reps = [companyeg for company_list in non_empty_lists for companyeg in company_list if companyeg.CompanyID in intersection_set]
        
        print(combined_list_reps)
        combined_set = set(combined_list_reps)
        combined_list1 = list(combined_set)
        
        combined_list2 = combined_list1 + companies
        
        combined_list = list(set(combined_list2))

        
        combined_list.sort(key=lambda x: x.CompanyID)
        print(combined_list)
        
        complogolist = []   

        for comp in combined_list:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]

        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        followeds = db_manager.get_followed(user_id=user_id)
        
        follow_list = []

        for followed in followeds:
            foll = db_manager.get_company(company_id=followed.CompanyID).CompanyID
            if foll:
                follow_list.append(foll)
                
        topcompscroll = db_manager.get_topcompscroll()
                    
        return render_template('/followed.html', topcompscroll=topcompscroll, firstname=firstname, compcount=len(combined_list), industry_list=industry_list, stock_list=stock_list, follow_list=follow_list ,updatecount=len(updates), updates=updates, company=combined_list, uname=uname, time=time, date=date, datetime=datetime, complogolist=complogolist)

    @app.route('/submit', methods=['POST'])
    def filter_company():
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id = db_manager.get_user(uname).id


        
        industry_list = db_manager.get_all_industries()
        stock_list = db_manager.get_all_stock_types()
        
        industry_filtered_company_list = []
        stock_filtered_company_list = []
        posichange_company_list = []
        posiop_company_list = []
        
        searchstring = request.form['search3']
        
        if searchstring is "":
            companies = []
            
        else:
            search_paramater = str('%') + str(searchstring) + str('%')
            companies = db_manager.get_all_comp_in_search(search_paramater=search_paramater)

        for industry in industry_list:
            if industry.IndustryName in request.form:
                comp = db_manager.get_all_comp_inds(industry=industry.IndustryName)
                print(comp)
                for cp in comp:
                    if cp:
                        industry_filtered_company_list.append(cp)
        
        for stocktp in stock_list:
            if stocktp.StockType in request.form:
                comp = db_manager.get_all_comp_stock(stock_type=stocktp.StockType)
                for cp in comp:
                    if cp:
                        stock_filtered_company_list.append(cp)
                        
        if 'posichnge' in request.form:
            comp = db_manager.get_all_posichange()
            for cp in comp:
                if cp:
                    posichange_company_list.append(cp)
                    
        if 'posiop' in request.form:
            comp = db_manager.get_all_posiop()
            for cp in comp:
                if cp:
                    posiop_company_list.append(cp)
                    
        print("indus",industry_filtered_company_list)
        print("stock",stock_filtered_company_list)
        
        # Define the list of lists
        lists_of_companies = [industry_filtered_company_list, stock_filtered_company_list, posichange_company_list, posiop_company_list]

        # Filter out empty lists
        non_empty_lists = [company_list for company_list in lists_of_companies if company_list]

        # Extract CompanyIDs from each non-empty list
        non_empty_sets = [set(companyeg.CompanyID for companyeg in company_list) for company_list in non_empty_lists]

        # Find the intersection of sets if there are non-empty lists
        if non_empty_sets:
            intersection_set = reduce(lambda x, y: x.intersection(y), non_empty_sets)
        else:
            intersection_set = set()

        # Retrieve Company objects corresponding to the CompanyIDs in the intersection set
        combined_list_reps = [companyeg for company_list in non_empty_lists for companyeg in company_list if companyeg.CompanyID in intersection_set]
        
        combined_set = set(combined_list_reps)
        combined_list1 = list(combined_set)
        
        combined_list2 = combined_list1 + companies
        
        combined_list = list(set(combined_list2))
        # # Get the sets of CompanyIDs for each list
        # industry_company_ids = set(companyeg.CompanyID for companyeg in industry_filtered_company_list)
        # stock_company_ids = set(companyeg.CompanyID for companyeg in stock_filtered_company_list)
        # posichange_company_ids = set(companyeg.CompanyID for companyeg in posichange_company_list)
        # posiop_company_ids = set(companyeg.CompanyID for companyeg in posiop_company_list)

        # # Find the intersection of all sets
        # common_company_ids = (
        #     industry_company_ids 
        #     & stock_company_ids 
        #     & posichange_company_ids 
        #     & posiop_company_ids
        # )

        # # Create a new list containing only the companies with common CompanyIDs
        # combined_list = [
        #     companyeg for companyeg in industry_filtered_company_list
        #     if companyeg.CompanyID in common_company_ids
        # ]

    # Now, common_companies_list contains only the companies that are present in all four lists

        
        # combined_list_reps = industry_filtered_company_list + stock_filtered_company_list + posichange_company_list + posiop_company_list
        
        # combined_set = set(combined_list_reps)
        
        # combined_list = list(combined_set)
        
        combined_list.sort(key=lambda x: x.CompanyID)
        print(combined_list)

        # company_ids_in_list1 = set(companyeg.CompanyID for companyeg in industry_filtered_company_list)

        # # Step 2: Iterate over similarlist2 and combine lists avoiding repetitions
        # combined_list = []
        # for companyeg in stock_filtered_company_list:
        #     if companyeg.CompanyID not in company_ids_in_list1:
        #         combined_list.append(companyeg)

        # Step 3: Return the combined list
        
        complogolist = []   


        for comp in combined_list:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]

        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        followeds = db_manager.get_followed(user_id=user_id)
        
        follow_list = []

        for followed in followeds:
            foll = db_manager.get_company(company_id=followed.CompanyID).CompanyID
            if foll:
                follow_list.append(foll)
                
        topcompscroll = db_manager.get_topcompscroll()
                    
        return render_template('/alllist.html', topcompscroll=topcompscroll, compcount=len(combined_list), industry_list=industry_list, stock_list=stock_list, follow_list=follow_list ,updatecount=len(updates), updates=updates, company=combined_list, uname=uname, time=time, date=date, datetime=datetime, complogolist=complogolist)

    @app.route('/search', methods=['POST'])
    def search_company():
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id = db_manager.get_user(uname).id

        
        
        
        
        industry_list = db_manager.get_all_industries()
        stock_list = db_manager.get_all_stock_types()
        
        searchstring = request.form['search']
        
        if searchstring is None:
            company = db_manager.get_all_companies()
            
        else:
            search_paramater = str('%') + str(searchstring) + str('%')
            company = db_manager.get_all_comp_in_search(search_paramater=search_paramater)  
        
        complogolist = []   


        for comp in company:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]

        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        followeds = db_manager.get_followed(user_id=user_id)
        
        follow_list = []

        for followed in followeds:
            foll = db_manager.get_company(company_id=followed.CompanyID).CompanyID
            if foll:
                follow_list.append(foll)
                
        topcompscroll = db_manager.get_topcompscroll()
                    
        return render_template('/alllist.html', topcompscroll=topcompscroll, industry_list=industry_list, stock_list=stock_list, follow_list=follow_list ,updatecount=len(updates), updates=updates, company=company, compcount=len(company), uname=uname, time=time, date=date, datetime=datetime, complogolist=complogolist)


    @app.route('/mark_as_read')
    def mark_as_read():
        if current_user.is_authenticated:
            uname=current_user.Username 
        else:
            flash("Sorry but you are not logged in yet !!")
            return redirect('/login')
                
        newsID = request.args.get('parameter')
        print(newsID)
        
        db_manager.read_notification(news_id=newsID, uname=uname)
        
        print("Task is being executed")
        return "Task executed successfully"

    @app.route('/follow_company')
    def follow_company():
        if current_user.is_authenticated:
            uname=current_user.Username 
        else:
            flash("Sorry but you are not logged in yet !!")
            return redirect('/login') 
        
        user_id = db_manager.get_user(uname).id
        company_id = request.args.get('parameter')
        
        db_manager.follow_company(user_id=user_id, company_id=company_id)
        
        return "Task executed successfully"

    @app.route('/unfollow_company')
    def unfollow_company():
        if current_user.is_authenticated:
            uname=current_user.Username 
        else:
            flash("Sorry but you are not logged in yet !!")
            return redirect('/login')
        
        user_id = db_manager.get_user(uname).id       
        company_id = request.args.get('parameter')

        db_manager.unfollow_company(user_id=user_id, company_id=company_id)

        return "Task executed successfully"


    @app.route('/welcome')
    def welcome():
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id = db_manager.get_user(uname).id
        
        stocks = db_manager.get_top_yield_comp(6)
        first_three = stocks[:3]
        next_three = stocks[3:5]
    
        complogolist = []   


        for comp in stocks:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]
        

        news = db_manager.get_news_desc(limit=7)
        
        newsimglist = []   


        for new in news:
            newsimglist += [{'nid':new.NewsID, 'nimg':b64encode(new.Photo).decode("utf-8")}]
            
        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)
        print(notifications)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        topcompscroll = db_manager.get_topcompscroll()
    
        return render_template('welcome.html', topcompscroll=topcompscroll, updatecount=len(updates), updates=updates, uname=uname, complogolist=complogolist, first_three=first_three, next_three=next_three, news=news, newsimglist=newsimglist)

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if current_user.is_authenticated:
            uname=current_user.Username 
            flash("You are still Logged in")
            return redirect('/welcome')
        
        if request.method == "POST":
            username = request.form.get('username')
            password = request.form.get('password')
            
            if (username is "") or (password is ""):
                flash ('Please enter all credentials')
                print("Please enter all credentials")
                return redirect(url_for('login'))
            
            user = db_manager.get_user(username)
            if not user or not check_password_hash(user.Password, password):
                flash ('Email or password incorrect')
                return redirect(url_for('login'))
            login_user(user)
            return redirect(url_for('welcome'))

        topcompscroll = db_manager.get_topcompscroll()
        return render_template('login.html', topcompscroll=topcompscroll)

    @app.route('/register', methods=['POST', 'GET'])
    def register():
        if current_user.is_authenticated:
            uname=current_user.Username
            flash("You are still Logged in")
            return redirect('/welcome')

        if request.method == "POST":
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('conf-password')

            if password != confirm_password:
                flash('Passwords do not match.')
                return redirect(url_for('register'))

            if (first_name is "") or (last_name is "") or (username is "") or (password is ""):
                flash('Please fill out all necessary fields.')
                return redirect(url_for('register'))

            # Check if the user already exists
            user = db_manager.get_user(username)
            if user:
                flash('User already exists. Please log in.')
                return redirect(url_for('login'))

            with open('src/static/images/defaultpropic.jpg', 'rb') as file:
                    image_data = file.read()

            # Create a new user
            db_manager.add_user(first_name=first_name, last_name=last_name,username=username, password=generate_password_hash(password, method='sha256'), image_data=image_data)

            userid = db_manager.get_user(username).id

            # Industry Preferences
            if request.form.get('technology'):
                db_manager.add_industry_pref(user_id=userid, industry_type="Technology")

            if request.form.get('finance'):
                db_manager.add_industry_pref(user_id=userid, industry_type="Finance")

            if request.form.get('healthcare'):
                db_manager.add_industry_pref(user_id=userid, industry_type="Healthcare")

            if request.form.get('retail'):
                db_manager.add_industry_pref(user_id=userid, industry_type="Retail")

            if request.form.get('energy'):
                db_manager.add_industry_pref(user_id=userid, industry_type="Energy")

            # Stock Preferences
            if request.form.get('stable'):
                db_manager.add_stock_pref(user_id=userid, stock_type="Stable")

            if request.form.get('volatile'):
                db_manager.add_stock_pref(user_id=userid, stock_type="Volatile")

            if request.form.get('blue_chip'):
                db_manager.add_stock_pref(user_id=userid, stock_type="Blue Chip")

            if request.form.get('mutual_fund'):
                db_manager.add_stock_pref(user_id=userid, stock_type="Mutual Fund")

            if request.form.get('bonds'):
                db_manager.add_stock_pref(user_id=userid, stock_type="Bonds")

            return redirect(url_for('login'))

        topcompscroll = db_manager.get_topcompscroll()
        return render_template('register.html', topcompscroll=topcompscroll)

    @app.route('/redirect', methods=['POST'])
    def redirect_with_company():
        input_parameter = request.form.get('inputParameter')
        # Construct the URL with the input parameter
        redirect_url = url_for('companyzoom', companyID=input_parameter)
        # Redirect to the constructed URL
        return jsonify({'redirect_url': redirect_url})

    @app.route('/redirecttop', methods=['POST'])
    def redirect_top():
        input_parameter = request.form.get('inputParameter')
        # Construct the URL with the input parameter
        redirect_url = url_for('topcompanies')
        # Redirect to the constructed URL
        return jsonify({'redirect_url': redirect_url})

    @app.route('/account')
    def dashboard():
        
        if current_user.is_authenticated:
            uname=current_user.Username 
        else:
            flash("Sorry but you are not logged in yet !!")
            return redirect('/login')
        
        user = db_manager.get_user(uname)
        user_id = user.id
        
        photo = user.ProfilePic
        propic = b64encode(photo).decode("utf-8")
        
        follow_comp_list = db_manager.get_followed(user_id=user_id, limit=3)
        
        follow_list2 = []
        
        for comp in follow_comp_list:
            follcomp = db_manager.get_company(company_id=comp.CompanyID)
            print(follcomp)
            if follcomp:
                follow_list2.append(follcomp)
                
        complogolist = []   


        for comp in follow_list2:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]
            
        suggest_comp_list = db_manager.get_all_suggested(user_id=user_id, limit=3)
        
        suggest_list2 = []
        
        for comp in suggest_comp_list:
            sugcomp = db_manager.get_company(company_id=comp.CompanyID)
            print(sugcomp)
            if sugcomp:
                suggest_list2.append(sugcomp)
                
        complogolist2 = []   

                
        for comp in suggest_list2:
            complogolist2 += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]

        notifications = db_manager.get_top_notifications(user_id=user_id, limit=4)
        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        newsimglist = []   


        for news in updates:
            newsimglist += [{'nid':news.NewsID, 'nimg':b64encode(news.Photo).decode("utf-8")}]
        
        notifications2 = db_manager.get_user_notification(user_id=user_id, limit=4)
        print(notifications)

        updates2 = []

        for update in notifications2:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates2.append(news_update)
            
        myindustries = db_manager.get_all_user_ind(user_id=user_id)
        mystocktypes = db_manager.get_all_user_stock(user_id=user_id)
        
        followeds = db_manager.get_followed(user_id=user_id)
        
        follow_list = []

        for followed in followeds:
            foll = db_manager.get_company(company_id=followed.CompanyID).CompanyID
            if foll:
                follow_list.append(foll)
                
        topcompscroll = db_manager.get_topcompscroll()
    
        return render_template('account.html', topcompscroll=topcompscroll, updatecount=len(updates2), updates2=updates2, follow_list=follow_list, user=user, propic=propic, myindustries=myindustries, mystocktypes=mystocktypes, updates=updates, newsimglist=newsimglist, follow_list2=follow_list2, suggest_list2=suggest_list2, complogolist=complogolist, complogolist2=complogolist2)

    @app.route('/settings', methods=['POST', 'GET'])
    def settings():
        if current_user.is_authenticated:
            uname=current_user.Username 
        else:
            flash("Sorry but you are not logged in yet !!")
            return redirect('/login')
        
        user = db_manager.get_user(uname)
        photo = current_user.ProfilePic
        propic = b64encode(photo).decode("utf-8")
        
        if request.method == 'POST':

            new_username = request.form.get('username')
            old_password = request.form.get('old-password')
            new_password = request.form.get('password')
            new_password_conf = request.form.get('conf-password')
            
            user = db_manager.get_user(uname)

            if not check_password_hash(user.Password, old_password):
                flash("Current password is not correct")
                print("Current password is not correct")
                return redirect('/settings')
                
            if request.form.get('password') and request.form.get('conf-password'):
                if new_password != new_password_conf:
                    flash("Passwords do not match")
                    print("Passwords do not match")
                    return redirect('/settings')

            if request.form.get('username'):
                if db_manager.get_user(new_username):
                    flash("Username is not available")
                    print("Username is not available")
                    return redirect('/settings')

            if 'profile_pict' in request.files:
                file = request.files['profile_pict']
                data = file.read()
                
                if file: 
                    print("pic check")
                    user.ProfilePic = data

            if request.form.get('old-password'):
                user.Password = generate_password_hash(new_password)
            
            if request.form.get('username'):
                user.Username = new_username
            
            userid = user.id


            db_manager.delete_all_industry_pref(user_id=userid)
            db_manager.delete_all_stock_pref(user_id=userid)
            
            # Industry Preferences
            if request.form.get('technology'):
                db_manager.add_industry_pref(user_id=userid, industry_type="Technology")
            else: ## Field is not chosen but the preference exists in db, delete it
                db_manager.delete_industry_pref(user_id=userid, industry_type="Technology")

            if request.form.get('finance'):
                db_manager.add_industry_pref(user_id=userid, industry_type="Finance")
            else: 
                db_manager.delete_industry_pref(user_id=userid, industry_type="Finance")

            if request.form.get('healthcare'):
                db_manager.add_industry_pref(user_id=userid, industry_type="Healthcare")
            else:
                db_manager.delete_industry_pref(user_id=userid, industry_type="Healthcare")

            if request.form.get('retail'):
                db_manager.add_industry_pref(user_id=userid, industry_type="Retail")
            else: 
                db_manager.delete_industry_pref(user_id=userid, industry_type="Retail")

            if request.form.get('energy'):
                db_manager.add_industry_pref(user_id=userid, industry_type="Energy")
            else: 
                db_manager.delete_industry_pref(user_id=userid, industry_type="Energy")

            # Stock Preferences
            if request.form.get('stable'):
                db_manager.add_stock_pref(user_id=userid, stock_type="Stable")
            else: 
                db_manager.delete_stock_pref(user_id=userid, stock_type="Stable")

            if request.form.get('volatile'):
                db_manager.add_stock_pref(user_id=userid, stock_type="Volatile")
            else: 
                db_manager.delete_stock_pref(user_id=userid, stock_type="Volatile")

            if request.form.get('blue_chip'):
                db_manager.add_stock_pref(user_id=userid, stock_type="Blue Chip")
            else: 
                db_manager.delete_stock_pref(user_id=userid, stock_type="Blue Chip")

            if request.form.get('mutual_fund'):
                db_manager.add_stock_pref(user_id=userid, stock_type="Mutual Fund")
            else: 
                db_manager.delete_stock_pref(user_id=userid, stock_type="Mutual Fund")

            if request.form.get('bonds'):
                db_manager.add_stock_pref(user_id=userid, stock_type="Bonds")
            else: 
                db_manager.delete_stock_pref(user_id=userid, stock_type="Bonds")
            

        topcompscroll = db_manager.get_topcompscroll()

        return render_template('settings.html', topcompscroll=topcompscroll, user=current_user, propic=propic)

    @app.route('/suggest.html')
    def suggestedcompanies():
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id=db_manager.get_user(uname).id
        else:
            flash("Sorry but you are not logged in yet !!")
            return redirect('/login')

        firstname = db_manager.get_user(uname).FirstName
        
        follow_link = db_manager.get_all_ord_suggested(user_id=user_id)
        
        follow_comp = []

        for followed in follow_link:
            foll = db_manager.get_company(company_id=followed.CompanyID)
            if foll:
                follow_comp.append(foll)
                
        complogolist = []


        for comp in follow_comp:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]

        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)
        print(notifications)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        followeds = db_manager.get_followed(user_id=user_id)
        
        follow_list = []

        for followed in followeds:
            foll = db_manager.get_company(company_id=followed.CompanyID).CompanyID
            if foll:
                follow_list.append(foll)
                
        print(follow_list)
        
        industry_list = db_manager.get_all_industries()
        stock_list = db_manager.get_all_stock_types()
        
        topcompscroll = db_manager.get_topcompscroll()
        
        return render_template('/suggest.html', topcompscroll=topcompscroll, firstname=firstname, compcount=len(follow_comp), industry_list=industry_list, stock_list=stock_list, follow_list=follow_list ,updatecount=len(updates), updates=updates, company=follow_comp, uname=uname, time=time, date=date, datetime=datetime, complogolist=complogolist)

    @app.route('/searchsuggest', methods=['POST'])
    def search_suggest_company():
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id = db_manager.get_user(uname).id

        firstname = db_manager.get_user(uname).FirstName
        
        follow_link = db_manager.get_all_ord_suggested(user_id=user_id)
        
        follow_comp = []

        for followed in follow_link:
            foll = db_manager.get_company(company_id=followed.CompanyID)
            if foll:
                follow_comp.append(foll)
                
        searchstring = request.form['search']
        
        if searchstring is None:
            company = follow_comp
            
        else:
            search_paramater = str('%') + str(searchstring) + str('%')
            
            follow_comp2 = []

            for followed in follow_link:
                foll = db_manager.is_name_in_search(company_id=followed.CompanyID, search_paramater=search_paramater)
                if foll:
                    follow_comp2.append(foll)
                    
            company = follow_comp2
        
        industry_list = db_manager.get_all_industries()
        stock_list = db_manager.get_all_stock_types()
        
        complogolist = []   


        for comp in company:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]

        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        followeds = db_manager.get_followed(user_id=user_id)
        
        follow_list = []

        for followed in followeds:
            foll = db_manager.get_company(company_id=followed.CompanyID).CompanyID
            if foll:
                follow_list.append(foll)
                
        topcompscroll = db_manager.get_topcompscroll()
                    
        return render_template('/suggest.html', topcompscroll=topcompscroll, firstname=firstname, industry_list=industry_list, stock_list=stock_list, follow_list=follow_list ,updatecount=len(updates), updates=updates, company=company, compcount=len(company), uname=uname, time=time, date=date, datetime=datetime, complogolist=complogolist)

    @app.route('/submitsuggest', methods=['POST'])
    def filter_suggest_company():
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id = db_manager.get_user(uname).id

        firstname = db_manager.get_user(uname).FirstName

        follow_link = db_manager.get_all_ord_suggested(user_id=user_id)
        
        follow_comp = []

        for followed in follow_link:
            foll = db_manager.get_company(company_id=followed.CompanyID)
            if foll:
                follow_comp.append(foll)
        
        industry_list = db_manager.get_all_industries()
        stock_list = db_manager.get_all_stock_types()
        
        industry_filtered_company_list = []
        stock_filtered_company_list = []
        posichange_company_list = []
        posiop_company_list = []
        
        searchstring = request.form['search3']
        
        if searchstring is "":
            companies = []
            
        else:
            search_paramater = str('%') + str(searchstring) + str('%')
            
            follow_comp2 = []

            for followed in follow_link:
                foll = db_manager.is_name_in_search(company_id=followed.CompanyID, search_paramater=search_paramater)
                if foll:
                    follow_comp2.append(foll)
                    
            companies = follow_comp2
        
        for industry in industry_list:
            if industry.IndustryName in request.form:
                print(industry.IndustryName)
                for followed in follow_link:
                    foll = db_manager.is_comp_in_industry(company_id=followed.CompanyID, industry_name=industry.IndustryName)
                    if foll:
                        industry_filtered_company_list.append(foll)
        
        for stocktp in stock_list:
            if stocktp.StockType in request.form:
                for followed in follow_link:
                    foll = db_manager.is_comp_in_stock(company_id=followed.CompanyID, stock_type=stocktp.StockType)
                    if foll:
                        stock_filtered_company_list.append(foll)
                        
        if 'posichnge' in request.form:
            for followed in follow_link:
                foll = db_manager.is_comp_posichnge(company_id=followed.CompanyID)
                if foll:
                    posichange_company_list.append(foll)

        if 'posiop' in request.form:
            for followed in follow_link:
                foll = db_manager.is_comp_posiop(company_id=followed.CompanyID)
                if foll:
                    posiop_company_list.append(foll)
                    
        print(industry_filtered_company_list)
        print(stock_filtered_company_list)
        
        # Define the list of lists
        lists_of_companies = [industry_filtered_company_list, stock_filtered_company_list, posichange_company_list, posiop_company_list]
        print(lists_of_companies)
        # Filter out empty lists
        non_empty_lists = [company_list for company_list in lists_of_companies if company_list]
        print(non_empty_lists)
        # Extract CompanyIDs from each non-empty list
        non_empty_sets = [set(companyeg.CompanyID for companyeg in company_list) for company_list in non_empty_lists]
        print(non_empty_sets)
        # Find the intersection of sets if there are non-empty lists
        if non_empty_sets:
            intersection_set = reduce(lambda x, y: x.intersection(y), non_empty_sets)
        else:
            intersection_set = set()

        print(intersection_set)
        # Retrieve Company objects corresponding to the CompanyIDs in the intersection set
        combined_list_reps = [companyeg for company_list in non_empty_lists for companyeg in company_list if companyeg.CompanyID in intersection_set]
        
        print(combined_list_reps)
        combined_set = set(combined_list_reps)
        combined_list1 = list(combined_set)
        
        combined_list2 = combined_list1 + companies
        
        combined_list = list(set(combined_list2))

        
        combined_list.sort(key=lambda x: x.CompanyID)
        print(combined_list)
        
        complogolist = []   


        for comp in combined_list:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]

        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        followeds = db_manager.get_followed(user_id=user_id)
        
        follow_list = []

        for followed in followeds:
            foll = db_manager.get_company(company_id=followed.CompanyID).CompanyID
            if foll:
                follow_list.append(foll)
        
        topcompscroll = db_manager.get_topcompscroll()
                    
        return render_template('/suggest.html', topcompscroll=topcompscroll, firstname=firstname, compcount=len(combined_list), industry_list=industry_list, stock_list=stock_list, follow_list=follow_list ,updatecount=len(updates), updates=updates, company=combined_list, uname=uname, time=time, date=date, datetime=datetime, complogolist=complogolist)

    @app.route('/genupdates.html')
    def generalupdates():
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
        
        newslist = db_manager.get_all_latest_news()
        
        companies = db_manager.get_all_companies()
        
        complogolist = []

        for comp in companies:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]
        
        newsimglist = []   

        for news in newslist:
            newsimglist += [{'nid':news.NewsID, 'nimg':b64encode(news.Photo).decode("utf-8")}]
        
        topcompscroll = db_manager.get_topcompscroll()
            
        return render_template('/genupdates.html', topcompscroll=topcompscroll, complogolist=complogolist, companies=companies, compcount=len(newslist), uname=uname, time=time, date=date, datetime=datetime, newslist=newslist, newsimglist=newsimglist)
        
    @app.route('/genupdates.html/<int:companyID>')

    def generalcompanyupdates(companyID):
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
            user_id=db_manager.get_user(uname).id
        
        
        
        
        
        newslist = db_manager.get_company_news(comapany_id=companyID)
        
        companies = db_manager.get_all_companies()
        
        compname = db_manager.get_company(company_id=companyID).Name
        
        complogolist = []


        for comp in companies:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]
        
        newsimglist = []   


        for news in newslist:
            newsimglist += [{'nid':news.NewsID, 'nimg':b64encode(news.Photo).decode("utf-8")}]
        
        topcompscroll = db_manager.get_topcompscroll()
            
        return render_template('/genupdates.html', topcompscroll=topcompscroll, compname=compname, complogolist=complogolist, companies=companies, compcount=len(newslist), uname=uname, time=time, date=date, datetime=datetime, newslist=newslist, newsimglist=newsimglist)    

    @app.route('/genupdfollow.html')
    def generalfollowupdates():
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
        else:
            flash("Sorry but you are not logged in yet !!")
            return redirect('/login')
        
        user_id = db_manager.get_user(uname).id
        
        companies = db_manager.get_all_companies()
        
        newslist = db_manager.get_all_latest_news()
        
        follow_link = db_manager.get_followed(user_id=user_id)
        
        follow_comp = []

        for followed in follow_link:
            foll = db_manager.get_company(company_id=followed.CompanyID)
            if foll:
                follow_comp.append(foll)
        
        # Extract CompanyIDs from the filtered list for faster lookup
        filtered_company_ids = {companyeg.CompanyID for companyeg in follow_comp}

        # List to store companies absent in the filtered list
        absent_companies = []

        # Iterate through all companies and check if they are absent in the filtered list
        for companyeg in companies:
            if companyeg.CompanyID not in filtered_company_ids:
                absent_companies.append(companyeg)
        
        companies = db_manager.get_all_companies()
        
        complogolist = []


        for comp in companies:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]
        
        newsimglist = []   


        for news in newslist:
            newsimglist += [{'nid':news.NewsID, 'nimg':b64encode(news.Photo).decode("utf-8")}]
            
        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)
        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
        
        topcompscroll = db_manager.get_topcompscroll()    
            
        return render_template('/genupdfollow.html', topcompscroll=topcompscroll, updates=updates, updatecount=len(updates), complogolist=complogolist, follcompanies=follow_comp, restcompanies=absent_companies, compcount=len(newslist), uname=uname, time=time, date=date, datetime=datetime, newslist=newslist, newsimglist=newsimglist)

    @app.route('/genupdfollow.html/<int:companyID>')
    def generalfollowcompanyupdates(companyID):
        user_id = 0
        uname = None
        if current_user.is_authenticated:
            uname=current_user.Username 
        else:
            flash("Sorry but you are not logged in yet !!")
            return redirect('/login')
        
        user_id = db_manager.get_user(uname).id
        
        
        companies = db_manager.get_all_companies()
        
        compname = db_manager.get_company(company_id=companyID).Name
        
        newslist = db_manager.get_company_news(comapany_id=companyID)
        
        follow_link = db_manager.get_followed(user_id=user_id)
        
        follow_comp = []

        for followed in follow_link:
            foll = db_manager.get_company(company_id=followed.CompanyID)
            if foll:
                follow_comp.append(foll)
        
        # Extract CompanyIDs from the filtered list for faster lookup
        filtered_company_ids = {companyeg.CompanyID for companyeg in follow_comp}

        # List to store companies absent in the filtered list
        absent_companies = []

        # Iterate through all companies and check if they are absent in the filtered list
        for companyeg in companies:
            if companyeg.CompanyID not in filtered_company_ids:
                absent_companies.append(companyeg)
        
        companies = db_manager.get_all_companies()
        
        complogolist = []


        for comp in companies:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]
        
        newsimglist = []   


        for news in newslist:
            newsimglist += [{'nid':news.NewsID, 'nimg':b64encode(news.Photo).decode("utf-8")}]
            
        notifications = db_manager.get_user_notification(user_id=user_id, limit=4)
        print(notifications)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
                
        topcompscroll = db_manager.get_topcompscroll()
            
        return render_template('/genupdfollow.html', topcompscroll=topcompscroll, updatecount=len(updates), updates=updates, compname=compname, complogolist=complogolist, follcompanies=follow_comp, restcompanies=absent_companies, compcount=len(newslist), uname=uname, time=time, date=date, datetime=datetime, newslist=newslist, newsimglist=newsimglist)
        
    @app.route('/handle_item_click', methods=['POST'])
    def handle_item_click():
        item = request.json['item']
        # Process the item as needed
        print("Item clicked:", item)
        # Return some response if needed
        return redirect(url_for('generalcompanyupdates', companyID=item))
        #return jsonify({'message': 'Item received'})
        
    @app.route('/notifications.html')
    def notificationspage():
        if current_user.is_authenticated:
            uname=current_user.Username 
        else:
            flash("Sorry but you are not logged in yet !!")
            return redirect('/login')    
        user_id = db_manager.get_user(uname).id
    
        notifications = db_manager.get_all_ord_notifications(user_id=user_id)
        print(notifications)

        updates = []

        for update in notifications:
            news_update = db_manager.get_news(news_id=update.NewsID)
            if news_update:
                updates.append(news_update)
        
        newslist = updates
        
        companies = db_manager.get_all_companies()
        
        complogolist = []


        for comp in companies:
            complogolist += [{'cid':comp.CompanyID, 'cimg':b64encode(comp.Logo).decode("utf-8")}]
        
        newsimglist = []   


        for news in newslist:
            newsimglist += [{'nid':news.NewsID, 'nimg':b64encode(news.Photo).decode("utf-8")}]
        
        topcompscroll = db_manager.get_topcompscroll()
            
        return render_template('/notifications.html', topcompscroll=topcompscroll, userid=user_id, notifications=notifications, name=current_user.FirstName, complogolist=complogolist, companies=companies, compcount=len(newslist), uname=uname, time=time, date=date, datetime=datetime, newslist=newslist, newsimglist=newsimglist)
        
    @app.route('/markallread')
    def markallread():    
        if current_user.is_authenticated:
            uname=current_user.Username 
        else:
            flash("Sorry but you are not logged in yet !!")
            return redirect('/login')    
        
        db_manager.mark_all_read(uname=uname)
        
        return redirect('/notifications.html')

    @app.route('/info.html')
    def info():
        uname=None
        if current_user.is_authenticated:
            uname=current_user.Username
        topcompscroll = db_manager.get_topcompscroll()
        return render_template('info.html', topcompscroll=topcompscroll, uname=uname)
        
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return db_manager.get_user_by_id(user_id)    
    
    # Additional configuration can go here
    app.secret_key = 'any Su93r$3cret string you want'


    # select the database filename
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///todo.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SUPPRESS_SEND'] = True

    # set up a 'model' for the data you want to store
    

    # init the database so it can connect with our app
    db.init_app(app)

    # drop everything, create all the tables, then put some data into the tables
    with app.app_context():   
        db.drop_all()
        db.create_all()
        dbinit()
        db_manager.initialize_all_companies()
        db_manager.update_all_stocks()
       #  db_manager.update_all_news()

    return app
    
