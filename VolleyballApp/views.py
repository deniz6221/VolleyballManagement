from django.shortcuts import render, redirect
from .forms import forms
from django.http import HttpResponse
from VolleyballApp.forms.forms import LoginForm, AddPlayerForm, AddCoachJuryForm, StadiumForm, DeleteMatchForum
import VolleyballApp.database.auth as auth
from VolleyballApp.database import insertions, selections
from datetime import datetime
import json
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            result = auth.loginAuth(username, password)
            if result == -1:
                return render(request,"login.html", {'invalid_login': True, 'form': forms.LoginForm})
            request.session["username"] = username
            request.session["password"] = password
            if result == 0:
                return redirect("/manager")
            elif result == 1:
                return redirect("/player")
            elif result == 2:
                return redirect("/coach")
            elif result == 3:
                return redirect("/jury")
            return render(request,"login.html", {'invalid_login': True, 'form': forms.LoginForm})


    return render(request,"login.html", {'invalid_login': False, 'form': forms.LoginForm})

def app_page(request):
    if(not auth.check_session_key(request)):
        return redirect('/login')
    type = auth.loginAuth(request.session["username"], request.session["password"]) 
    if(type == 0):
        return redirect('/manager')
    elif (type == 1):
        return redirect('/player')
    elif (type == 2):
        return redirect('/coach')
    elif (type == 2):
        return redirect('/jury')
    return redirect('/login')


def db_manager_home(request):
    if(not auth.check_session_key(request)):
        return redirect('/login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 0):
        return redirect('/login')
    return render(request, "dbManager.html", {'username': request.session['username']})

def db_manager_add_player(request):
    if(not auth.check_session_key(request)):
        return redirect('/login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 0):
        return redirect('/login')
    if request.method == "POST":
        form = AddPlayerForm(request.POST)
        if form.is_valid():
            try:
                values =(
                form.cleaned_data["username"],
                form.cleaned_data["password"],
                form.cleaned_data["name"],
                form.cleaned_data["surname"],
                form.cleaned_data["date_of_birth"],
                form.cleaned_data["height"],
                form.cleaned_data["weight"])
                position = form.cleaned_data["positions"]
                teams = form.cleaned_data["teams"]
                
                if len(teams) == 0:
                    return render(request, "dbManagerAddUsers.html", {'form': AddPlayerForm, 'status': 0, "teamSelect": True})
                if len(position) == 0:
                    return render(request, "dbManagerAddUsers.html", {'form': AddPlayerForm, 'status': 0, "posSelect": True})
                if not insertions.insertPlayer(values, position, teams):
                    return render(request, "dbManagerAddUsers.html", {'form': AddPlayerForm, 'status': -1})
                return render(request, "dbManagerAddUsers.html", {'form': AddPlayerForm, 'status': 1})
            except:
                return render(request, "dbManagerAddUsers.html", {'form': AddPlayerForm, 'status': -1})
        else:
            return render(request, "dbManagerAddUsers.html", {'form': AddPlayerForm, 'status': -1})

    return render(request, "dbManagerAddUsers.html", {'form': AddPlayerForm, 'status': 0})

def db_manager_add_coach(request):
    if(not auth.check_session_key(request)):
        return redirect('../../login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 0):
        return redirect('../../login')
    if request.method == "POST":
        form = AddCoachJuryForm(request.POST)
        if form.is_valid():
            try:
                values =(
                form.cleaned_data["username"],
                form.cleaned_data["password"],
                form.cleaned_data["name"],
                form.cleaned_data["surname"],
                form.cleaned_data["nationality"])
                if(not insertions.insertCoach(values)):
                    return render(request, "dbManagerAddUsers.html", {'form': AddCoachJuryForm, 'status': -1})
                return render(request, "dbManagerAddUsers.html", {'form': AddCoachJuryForm, 'status': 1})
            except:
                return render(request, "dbManagerAddUsers.html", {'form': AddCoachJuryForm, 'status': -1})

    return render(request, "dbManagerAddUsers.html", {'form': AddCoachJuryForm, 'status': 0})

def db_manager_add_jury(request):
    if(not auth.check_session_key(request)):
        return redirect('../../login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 0):
        return redirect('../../login')
    if request.method == "POST":
        form = AddCoachJuryForm(request.POST)
        if form.is_valid():
            try:
                values =(
                form.cleaned_data["username"],
                form.cleaned_data["password"],
                form.cleaned_data["name"],
                form.cleaned_data["surname"],
                form.cleaned_data["nationality"])
                if(not insertions.insertJury(values)):
                    return render(request, "dbManagerAddUsers.html", {'form': AddCoachJuryForm, 'status': -1})
                return render(request, "dbManagerAddUsers.html", {'form': AddCoachJuryForm, 'status': 1})
            except:
                return render(request, "dbManagerAddUsers.html", {'form': AddCoachJuryForm, 'status': -1})

    return render(request, "dbManagerAddUsers.html", {'form': AddCoachJuryForm, 'status': 0})


def db_manager_stadium(request):
    if(not auth.check_session_key(request)):
        return redirect('../../login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 0):
        return redirect('../../login')
    if request.method == "POST":
        form = StadiumForm(request.POST)
        if form.is_valid():
            try:
                id = form.cleaned_data["Stadium"]
                newName = form.cleaned_data["New_Stadium_Name"]
                insertions.updateStadium(id, newName)
                return render(request, "dbManagerChangeStad.html", {'form': StadiumForm, 'status': 1})
            except Exception as e:
                print(e)
                return render(request, "dbManagerChangeStad.html", {'form': StadiumForm, 'status': -1})
    return render(request, "dbManagerChangeStad.html", {'form': StadiumForm, 'status': 0})

def coach_home(request):
    if(not auth.check_session_key(request)):
        return redirect('/login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 2):
        return redirect('/login')
    return render(request, "coach.html", {"username": request.session["username"]})

def coach_delete_match(request):
    if(not auth.check_session_key(request)):
        return redirect('/login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 2):
        return redirect('/login')
    if request.method == "POST":
        form = DeleteMatchForum(request.POST)
        if form.is_valid():
            try:
                id = form.cleaned_data["Session_ID"]
                insertions.deleteMatch(id)
                return render(request, "coachDeleteMatch.html", {"form": DeleteMatchForum, "status": 1})
            except Exception as e:
                print(e)
                return render(request, "coachDeleteMatch.html", {"form": DeleteMatchForum, "status": -1})
    return render(request, "coachDeleteMatch.html", {"form": DeleteMatchForum, "status": 0})

def coach_add_match(request):
    if(not auth.check_session_key(request)):
        return redirect('/login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 2):
        return redirect('/login')
    team_id = selections.get_coach_team_id(request.session["username"])
    next_match = int(selections.get_max_match_id()) +1
    if team_id == []:
        return render(request, "coachAddMatch.html", {"status": False})
    if request.method == "POST":
        values = (int(selections.get_max_match_id()) +1, 
                 team_id[0], request.POST.get("stadium"), 
                 request.POST.get("timeSlot"), 
                 request.POST.get("matchDate"),
                 request.POST.get("jury"))
        try:
            insertions.addMatch(values)
            return render(request, "coachAddMatch.html", {"status": True, "insert": 1})
        except Exception as e:
            print(e)
            return render(request, "coachAddMatch.html", {"status": True, "insert": -1})
    if "date" in request.GET:
        date = datetime.strptime(request.GET["date"], '%Y-%m-%d').strftime('%d.%m.%Y')
        available = selections.get_available_time_slots(date)
        return render(request, "coachAddMatchSession.html", {"data": available, "jsondata": json.dumps(available), "juries": selections.get_juries(), "date": date, "team_name": team_id[1],"session_id": next_match})

    return render(request, "coachAddMatch.html", {"status": True, "insert": 0})

def coach_add_squad(request):
    if(not auth.check_session_key(request)):
        return redirect('/login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 2):
        return redirect('/login')
    try:
        team_id = selections.get_coach_team_id(request.session["username"])
        if (team_id == []):
            return redirect("/coach")
        squad_matches = selections.get_squad_matches(team_id[0])
        if request.method == "POST":
            players = [key for key in request.POST.keys() if request.POST.get(key) == 'on']
            if len(players) != 6:
                return redirect("/coach/createSquad")
            positions = []
            for i in players:
                positions.append({"username": i, "position": request.POST.get("pos_" + i)})
            match_id = int(request.POST.get("matchId"))
            rej = True
            for i in squad_matches:
                if int(i["id"]) == match_id:
                    rej = False
            if rej:
                return redirect("/coach/createSquad?success=-1")
            if(insertions.add_session_squad(match_id, positions)):
                return redirect("/coach/createSquad?success=1")
            return redirect("/coach/createSquad?success=-1")
        if "id" in request.GET:
            reject = -1
            req_id = request.GET["id"]
            for i in range(len(squad_matches)):
                elmt = squad_matches[i]
                if int(elmt["id"]) == int(req_id):
                    reject = i
                    break
            if reject == -1:
                return redirect("/coach/createSquad")
            players = selections.get_available_players(team_id[0], squad_matches[reject]["date"], squad_matches[reject]["time"])
            return render(request, "coachPlayersMatch.html", {"players": players, "matchId": req_id, "matchDate": squad_matches[reject]["date"]})
        if "success" in  request.GET:
            try:
                val = int(request.GET["success"])
                return render(request, "coachAddSquad.html", {"matches": squad_matches, "status": val})
            except:
                return redirect("/coach/createSquad")
        return render(request, "coachAddSquad.html", {"matches": squad_matches, "status": 0})
    except Exception as e:
        print(e)
        return redirect("/coach/createSquad?success=-1")

def coach_stadium(request):
    if(not auth.check_session_key(request)):
        return redirect('/login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 2):
        return redirect('/login')
    return render(request, "coachStadium.html", {"stadiums": selections.get_stadiums()})

def jury_home(request):
    if(not auth.check_session_key(request)):
        return redirect('/login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 3):
        return redirect('/login')
    username = request.session["username"]
    lst = selections.get_average_count_rating(username)
    return render(request, "jury.html", {"username": username, "average": lst[1], "count": lst[0]})

def jury_rate(request):
    if(not auth.check_session_key(request)):
        return redirect('/login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 3):
        return redirect('/login')
    username = request.session["username"]
    matches = selections.get_rateable_matches(username)
    if request.method == "POST":
        match_id = request.POST.get("id")
        rating = request.POST.get("rating")
        can_rate = False
        for i in matches:
            if str(i["id"]) == str(match_id):
                can_rate = True
                break
        if not can_rate:
            return redirect('/jury')
        insertions.rateMatch(match_id, rating)
        return redirect("/jury/rate?status=true")
    if 'id' in request.GET:
        match_id = request.GET['id']
        can_rate = False
        for i in matches:
            if str(i["id"]) == str(match_id):
                can_rate = True
                break
        if not can_rate:
            return redirect('/jury')
        vals = selections.get_match_info(match_id)
        return render(request, "juryRateMatch.html", {"id": vals[0], "team": vals[2], "date": vals[1], "stad": vals[3]})
    if 'status' in request.GET:
        return render(request, "juryRate.html", {"matches": matches, "status": True})
    return render(request, "juryRate.html", {"matches": matches, "status": False})

def player_home(request):
    if(not auth.check_session_key(request)):
        return redirect('/login')
    if(auth.loginAuth(request.session["username"], request.session["password"]) != 1):
        return redirect('/login')
    username = request.session["username"]
    return render(request, "player.html", {"username": username, "players": selections.get_played_players(username), "height": selections.get_average_height(username)})

def log_out(request):
    try:
        del request.session["username"]
        del request.session["password"]
    except:
        pass
    return redirect('/login')