from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Team, Game, League
from .forms import Game_forms
from .scripts import create_games, create_teams, get_updated_games, aproveitamento, create_league, update_teams, update_games
import requests, time
from django.http import JsonResponse
import json
import json
	
# Create your views here.

def	home(request):
	leagues_list = League.objects.all()
	context = {"leagues_list": leagues_list}
	return render(request, 'index.html', context)

def	get_data(request):
	id_liga = int(request.POST.get('league_id'))
	print (id_liga)
	league = League.objects.get(league_id=id_liga)
	teamslist = Team.objects.filter(league_id=id_liga)
	gameslist = Game.objects.filter(league_id=id_liga)
	teams_list = teamslist.order_by('-points', '-wins', '-sg')
	data = {
		'league_data': {
			'league_id': league.league_id,
			'name': league.league_name,
			'logo': league.logo,
			'country': league.country,
			'url': league.url,
			'zone_1': league.zone_1,
			'zone_1_txt': league.zone_1_txt,
			'zone_2': league.zone_2,
			'zone_2_txt': league.zone_2_txt,
			'zone_3': league.zone_3,
			'zone_3_txt': league.zone_3_txt,
			'zone_4': league.zone_4_txt,
			'zone_4_txt': league.zone_4_txt,
			'zone_5': league.zone_5,
			'zone_5_txt': league.zone_5_txt,
			'zone_reb': league.zone_reb,
			'zone_reb_txt': league.zone_reb_txt,
		},
		'teams': [],
		'games': []
	}
	for team in teams_list:
		data['teams'].append({
			'id_name': team.id_name,
			'name': team.name,
			'points': team.points,
			'wins': team.wins,
			'draws': team.draws,
			'loss': team.loss,
			'goals_pro': team.goals_pro,
			'goals_con': team.goals_con,
			'aproveitamento': team.aproveitamento,
			'sg': team.sg,
			'logo': team.logo,
			'stadium': team.stadium,
			'games_played': team.games_played,
	})
	for game in gameslist:
		data['games'].append({
			'league_id' : game.league_id,
			'game_id': game.id,
			'home_team': game.home_team.name,
			'away_team': game.away_team.name,
			'home_goals': game.home_goals,
			'away_goals': game.away_goals,
			'simulated': game.simulated,
			'real_played': game.real_played,
			'round': game.round,
			'timestamp': game.timestamp,
			'local_time': game.local_time,
	})
	return (JsonResponse(data, safe=False))

def reset_result(game, home_team, away_team):
	home_team.games_played -= 1
	away_team.games_played -= 1
	home_team.goals_pro -= game.home_goals
	home_team.goals_con -= game.away_goals
	away_team.goals_pro -= game.away_goals
	away_team.goals_con -= game.home_goals
	home_team.sg -= game.home_goals - game.away_goals
	away_team.sg -= game.away_goals - game.home_goals
	if game.home_goals > game.away_goals:
		home_team.wins -= 1
		away_team.loss -= 1
		home_team.points -= 3
	elif game.home_goals == game.away_goals:
		home_team.draws -= 1
		away_team.draws -= 1
		home_team.points -= 1
		away_team.points -= 1
	else:
		away_team.wins -= 1
		home_team.loss -= 1
		away_team.points -= 3
	game.home_goals = None
	game.away_goals = None
	game.played = False
	home_team.aproveitamento = aproveitamento(home_team)
	away_team.aproveitamento = aproveitamento(away_team)
	game.save()
	home_team.save()
	away_team.save()

def current_timestamp():
    return int(time.time())

def	get_current_round(id):
	cur_time = current_timestamp()
	game_list = Game.objects.filter(league_id = id)
	cur_game_time = 0
	cur_round = 1
	for game in game_list:
		if int(game.timestamp) > cur_time and (int(game.timestamp) < int(cur_game_time) or cur_game_time == 0):
			cur_game_time = game.timestamp
			cur_round = game.round
	return(cur_round)

def	premier_league(request, round=1):
	exec_game(request)
	if (request.method == "GET"):
		round = get_current_round(39)
	else:
		game_id = int(request.POST.get('game_id'))
		game_class = Game.objects.get(id = game_id)
		round = game_class.round
	league = League.objects.all()
	games_list = Game.objects.filter(league_id = 39, round = round)
	teams_list = Team.objects.filter(league_id = 39)
	teams_list = teams_list.order_by('-points', '-sg', '-goals_pro')
	context = {'league': league[2], 'teams_list': teams_list, 'games_list': games_list, 'current_round' : round}
	return render(request, 'home.html', context)

def	la_liga(request, round=1):
	exec_game(request)
	if (request.method == "GET"):
		round = get_current_round(140)
	else:
		game_id = int(request.POST.get('game_id'))
		game_class = Game.objects.get(id = game_id)
		round = game_class.round
	league = League.objects.all()
	games_list = Game.objects.filter(league_id = 140, round = round)
	teams_list = Team.objects.filter(league_id = 140)
	teams_list = teams_list.order_by('-points', '-sg', '-goals_pro')
	context = {'league': league[3], 'teams_list': teams_list, 'games_list': games_list, 'current_round' : round}
	return render(request, 'home.html', context)

def	serie_a(request, round=1):
	exec_game(request)
	if (request.method == "GET"):
		round = get_current_round(135)
	else:
		game_id = int(request.POST.get('game_id'))
		game_class = Game.objects.get(id = game_id)
		round = game_class.round
	league = League.objects.all()
	games_list = Game.objects.filter(league_id = 135, round = round)
	teams_list = Team.objects.filter(league_id = 135)
	teams_list = teams_list.order_by('-points', '-sg', '-goals_pro')
	context = {'league': league[5], 'teams_list': teams_list, 'games_list': games_list, 'current_round' : round}
	return render(request, 'home.html', context)

def	bundesliga(request, round=1):
	exec_game(request)
	if (request.method == "GET"):
		round = get_current_round(78)
	else:
		game_id = int(request.POST.get('game_id'))
		game_class = Game.objects.get(id = game_id)
		round = game_class.round
	league = League.objects.all()
	games_list = Game.objects.filter(league_id = 78, round = round)
	teams_list = Team.objects.filter(league_id = 78)
	teams_list = teams_list.order_by('-points', '-sg', '-goals_pro')
	context = {'league': league[4], 'teams_list': teams_list, 'games_list': games_list, 'current_round' : round}
	return render(request, 'home.html', context)


def brasil_serie_a(request, round=1):
	exec_game(request)
	if (request.method == "GET"):
		round = get_current_round(71)
	else:
		game_id = int(request.POST.get('game_id'))
		game_class = Game.objects.get(id = game_id)
		round = game_class.round
	league = League.objects.filter(league_id = 71)
	games_list = Game.objects.filter(league_id = 71, round = round)
	teams_list = Team.objects.filter(league_id = 71)
	teams_list = teams_list.order_by('-points', '-wins', '-sg')
	context = {'league': league[0], 'teams_list': teams_list, 'games_list': games_list, 'current_round' : round}
	return render(request, 'home.html', context)

def brasil_serie_b(request, round=1):
	if (request.method == "GET"):
		round = get_current_round(72)
		league = League.objects.all()
		games_list = Game.objects.filter(league_id = 72, round = round)
		teams_list = Team.objects.filter(league_id = 72)
		teams_list = teams_list.order_by('-points', '-wins', '-sg')
		context = {'league': league[1], 'teams_list': teams_list, 'games_list': games_list, 'current_round' : round}
		return render(request, 'home.html', context)
	else:
		exec_game(request)
		teams_list = Team.objects.filter(league_id = 72)
		teams_list = teams_list.order_by('-points', '-wins', '-sg')
		data = []
		for team in teams_list:
			data.append({
				'id_name':team.name,
				'games': team.games_played,
				'logo': team.logo,
				'points': team.points,
				'wins': team.wins,
				'draws': team.draws,
				'loss': team.loss,
				'goals_pro': team.goals_pro,
				'goals_con': team.goals_con,
				'sg': team.sg,
				'aproveitamento': team.aproveitamento,
			})
		return JsonResponse(data, safe=False)


def	restart_teams(teams_list):
	for team in teams_list:
		team.points = 0
		team.goals_pro = 0
		team.goals_con = 0
		team.wins = 0
		team.loss = 0
		team.draws = 0
		team.sg = 0
		team.games_played = 0
		team.save()
	
def	restart_games(game_list):
	for game in game_list:
		game.home_goals = None
		game.away_goals = None
		game.played = False
		game.save()

def	restart():
	restart_teams(Team.objects.all())
	restart_games(Game.objects.all())

def reset_simulation(request):
	l_id = int(request.POST.get('league_id'))
	game_list = Game.objects.filter(league_id = l_id)
	if (request.method == 'POST'):
		for game in game_list:
			if (game.simulated == True and game.real_played == False):
				reset_result(game, game.home_team, game.away_team)
	round = get_current_round(l_id)
	games_list = Game.objects.filter(league_id = l_id, round = round)
	teams_list = Team.objects.filter(league_id = l_id)
	teams_list = teams_list.order_by('-points', '-wins', '-sg')
	league = League.objects.get(league_id = l_id)
	context = {'teams_list': teams_list, 'games_list': games_list, 'current_round' : round, 'league': league}
	return render(request, 'home.html', context)


def next_round(request):
	round = int(request.POST.get('current_round'))
	league_id = int(request.POST.get('league_id'))
	games_list = Game.objects.filter(league_id = league_id, round = round + 1)
	teams_list = Team.objects.filter(league_id = league_id)
	teams_list = teams_list.order_by('-points', '-wins', '-sg')
	league = League.objects.get(league_id = league_id)
	context = {'teams_list': teams_list, 'games_list': games_list, 'current_round' : round + 1, 'league': league}
	return render(request, 'home.html', context)

def prev_round(request):
	round = int(request.POST.get('current_round'))
	league_id = int(request.POST.get('league_id'))
	games_list = Game.objects.filter(league_id = league_id, round = round - 1)
	teams_list = Team.objects.filter(league_id = league_id)
	teams_list = teams_list.order_by('-points', '-wins', '-sg')
	league = League.objects.get(league_id = league_id)
	context = {'teams_list': teams_list, 'games_list': games_list, 'current_round' : round - 1, 'league': league}
	return render(request, 'home.html', context)

def api_football(request):
	""" if (request.method == 'POST'):
		url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
		querystring = {"league":"71", "season":"2024"}
		headers = {
			"X-RapidAPI-Key": "a915c948a2mshd5daae6b916daabp1b5891jsn54b9950682d1",
			"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
		}
		response = requests.get(url, headers=headers, params=querystring)
		data = response.json()
		restart(request)
		get_updated_games(data) """
	update_games()
	return(home(request))

def exec_game(request):
	if request.method == 'POST':
		home_team_name = request.POST.get('home_team')
		home_goals = int(request.POST.get('home_goals'))
		away_team_name = request.POST.get('away_team')
		away_goals = int(request.POST.get('away_goals'))
		game_id = int(request.POST.get('game_id'))
		home_team = Team.objects.get(name=home_team_name)
		away_team = Team.objects.get(name=away_team_name)
		game_class = Game.objects.get(id = game_id)
		if game_class.simulated == True:
			reset_result(game_class, home_team, away_team)
		round = game_class.round
		home_team.games_played += 1
		away_team.games_played += 1
		home_team.goals_pro += home_goals
		game_class.home_goals = home_goals
		home_team.goals_con += away_goals
		game_class.away_goals = away_goals
		away_team.goals_pro += away_goals
		away_team.goals_con += home_goals
		home_team.sg += home_goals - away_goals
		away_team.sg += away_goals - home_goals
		if home_goals > away_goals:
			home_team.wins += 1
			away_team.loss += 1
			home_team.points += 3
		elif home_goals == away_goals:
			home_team.draws += 1
			away_team.draws += 1
			home_team.points += 1
			away_team.points += 1
		else:
			away_team.wins += 1
			home_team.loss += 1
			away_team.points += 3
		home_team.aproveitamento = aproveitamento(home_team)
		away_team.aproveitamento = aproveitamento(away_team)
		game_class.simulated = True
		home_team.save()
		away_team.save()
		game_class.save()