import urllib2 as url
import lxml.etree as etree
import os
import gzip
import datetime

def scoreboard(year, month, day, home=None, away=None):
    '''
    Return the data for a certain day matching certain criteria as a dictionary

    Should not be used other than as called by `__init__.py`
    '''
    monthstr = str(month).zfill(2)
    daystr = str(day).zfill(2)
    filename = "gameday-data/year_%i/month_%s/day_%s/scoreboard.xml.gz" % (year, monthstr, daystr)
    file = os.path.join(os.path.dirname(__file__), filename)
    if os.path.isfile(file):
        data = file
    else:
        data = url.urlopen("http://gd2.mlb.com/components/game/mlb/year_%i/month_%s/day_%s/scoreboard.xml" % (year, monthstr, daystr))
    parsed = etree.parse(data)
    root = parsed.getroot()
    games = {}
    for game in root:
        if game.tag == "go_game":
            teams = game.findall('team')
            home_name = teams[0].attrib['name']
            away_name = teams[1].attrib['name']
            if (home_name == home and home!=None) or (away_name == away and away!=None) or (away==None and home==None):
                game_type = "go_game"
                game_data = game.find('game')
                game_id = game_data.attrib['id']
                game_league = game_data.attrib['league']
                game_status = game_data.attrib['status']
                game_start_time = game_data.attrib['start_time']
                home_team_data = teams[0].find('gameteam')
                home_team = {'name': home_name, 'runs': int(home_team_data.attrib['R']), 'hits':int(home_team_data.attrib['H']), 'errors':int(home_team_data.attrib['E'])}
                away_team_data = teams[1].find('gameteam')
                away_team = {'name': away_name, 'runs': int(away_team_data.attrib['R']), 'hits':int(away_team_data.attrib['H']), 'errors':int(away_team_data.attrib['E'])}
                w_pitcher_data = game.find('w_pitcher')
                w_pitcher_name = w_pitcher_data.find('pitcher').attrib['name']
                w_pitcher = {'name':w_pitcher_name, 'wins':int(w_pitcher_data.attrib['wins']), 'losses':int(w_pitcher_data.attrib['losses'])}
                l_pitcher_data = game.find('l_pitcher')
                l_pitcher_name = l_pitcher_data.find('pitcher').attrib['name']
                l_pitcher = {'name':l_pitcher_name, 'wins':int(l_pitcher_data.attrib['wins']), 'losses':int(l_pitcher_data.attrib['losses'])}
                sv_pitcher_data = game.find('sv_pitcher')
                sv_pitcher_name = sv_pitcher_data.find('pitcher').attrib['name']
                sv_pitcher = {'name':sv_pitcher_name, 'saves':int(sv_pitcher_data.attrib['saves'])}
                output = {'game_id':game_id, 'game_type':game_type, 'game_league':game_league, 'game_status':game_status, 'game_start_time':game_start_time, 'home_team':home_team, 'away_team':away_team, 'w_pitcher':w_pitcher, 'l_pitcher':l_pitcher, 'sv_pitcher':sv_pitcher}
                games[game_id]=output
        elif game.tag == "sg_game":
            teams = game.findall('team')
            home_name = teams[0].attrib['name']
            away_name = teams[1].attrib['name']
            if (home_name == home and home!=None) or (away_name == away and away!=None) or (away==None and home==None):
                game_type = "sg_game"
                game_data = game.find('game')
                game_id = game_data.attrib['id']
                game_league = game_data.attrib['league']
                game_status = game_data.attrib['status']
                game_start_time = game_data.attrib['start_time']
                delay_reason = game_data.find('delay_reason').text
                teams = game.findall('team')
                home_team_data = teams[0].find('gameteam')
                home_team = {'name': teams[0].attrib['name'], 'runs': int(home_team_data.attrib['R']), 'hits':int(home_team_data.attrib['H']), 'errors':int(home_team_data.attrib['E'])}
                away_team_data = teams[1].find('gameteam')
                away_team = {'name': teams[1].attrib['name'], 'runs': int(away_team_data.attrib['R']), 'hits':int(away_team_data.attrib['H']), 'errors':int(away_team_data.attrib['E'])}
                output = {'game_id':game_id, 'game_type':game_type, 'game_league':game_league, 'game_status':game_status, 'game_start_time':game_start_time, 'home_team':home_team, 'away_team':away_team, 'delay_reason':delay_reason, 'w_pitcher':{}, 'l_pitcher':{}, 'sv_pitcher':{}}
                games[game_id]=output
    return games

class GameScoreboard(object):
    '''
    Object to hold scoreboard information about a certain game
    '''
    def __init__(self, data):
        '''
        Creates a `GameScoreboard` object

        data is expected to come from the `scoreboard()` function
        '''
        self.game_id = data['game_id']
        self.game_type = data.get('game_type', '')
        self.game_status = data.get('game_status', '')
        self.game_league = data.get('game_league', '')
        self.game_start_time = data.get('game_start_time', '')
        self.home_team = data.get('home_team', {}).get('name', '')
        self.home_team_runs = data.get('home_team', {}).get('runs', 0)
        self.home_team_hits = data.get('home_team', {}).get('hits', 0)
        self.home_team_errors = data.get('home_team', {}).get('errors', 0)
        self.away_team = data.get('away_team', '').get('name', '')
        self.away_team_runs = data.get('away_team', {}).get('runs', 0)
        self.away_team_hits = data.get('away_team', {}).get('hits', 0)
        self.away_team_errors = data.get('away_team', {}).get('errors', 0)
        self.w_pitcher = data.get('w_pitcher', {}).get('name', '')
        self.w_pitcher_wins = data.get('w_pitcher', {}).get('wins', 0)
        self.w_pitcher_losses = data.get('w_pitcher', {}).get('losses', 0)
        self.l_pitcher = data.get('l_pitcher', {}).get('name', '')
        self.l_pitcher_wins = data.get('l_pitcher', {}).get('wins', 0)
        self.l_pitcher_losses = data.get('l_pitcher', {}).get('losses', 0)
        self.sv_pitcher = data.get('sv_pitcher', {}).get('name', '')
        self.sv_pitcher_saves = data.get('sv_pitcher', {}).get('saves', 0)
        self.w_team = ''
        self.l_team = ''
        if self.home_team_runs > self.away_team_runs:
            self.w_team = self.home_team
            self.l_team = self.away_team
        elif self.away_team_runs > self.home_team_runs:
            self.w_team = self.away_team
            self.l_team = self.home_team
        year, month, day, rest = self.game_id.split('_', 3)
        hour, other = self.game_start_time.split(':', 2)
        minute = other[:2]
        am_pm = other[2:]
        if am_pm == "PM":
            hour = int(hour)+11
        self.date = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
    
    def nice_score(self):
        '''
        Return a nicely formatted score of the game
        '''
        return '%s (%d) at %s (%d)' % (self.away_team, self.away_team_runs, self.home_team, self.home_team_runs)
    
    def __str__(self):
        return self.nice_score()

def box_score(game_id):
    '''
    Return the box score of a game with matching id
    
    Should not be used other than as called by `__init__.py`
    '''
    year, month, day, rest = game_id.split('_', 3)
    filename = "gameday-data/year_%s/month_%s/day_%s/gid_%s/boxscore.xml" % (year, month, day, game_id)
    file = os.path.join(os.path.dirname(__file__), filename)
    if os.path.isfile(file):
        data = file
    else:
        data = url.urlopen("http://gd2.mlb.com/components/game/mlb/year_%s/month_%s/day_%s/gid_%s/boxscore.xml" % (year, month, day, game_id))
    parsed = etree.parse(data)
    root = parsed.getroot()
    linescore = root.find('linescore')
    result = {}
    result['game_id']=game_id
    for x in linescore:
        inning = x.attrib['inning']
        home = x.attrib['home']
        away = x.attrib['away']
        result[int(inning)] = {'home':home, 'away':away}
    return result

class GameBoxScore(object):
    '''
    Object to hold the box score of a certain game
    '''
    def __init__(self, data):
        '''
        Creates a `GameBoxScore` object

        data is expected to come from the `box_score()` function
        '''
        self.game_id = data['game_id']
        data.pop('game_id', None)
        self.innings = []
        for x in sorted(data):
            result = {'inning':int(x), 'home':data[x]['home'], 'away':data[x]['away']}
            self.innings.append(result)
    
    def __iter__(self):
        '''
        Allows object to be iterated over
        '''
        for x in self.innings:
            yield x
    
    def print_scoreboard(self):
        '''
        Print object as a scoreboard
        '''
        output = ''
        innings = []
        away = []
        home = []
        for x in self:
            innings.append(x['inning'])
            away.append(x['away'])
            home.append(x['home'])
        output += "Inning\t"
        for x in innings:
            output += str(x)+" "
        output += '\n'
        for x in innings:
            output += "---"
        output += "\nAway\t"
        for y, x in enumerate(away, start=1):
            if y>=10:
                output += str(x)+"  "
            else:
                output += str(x)+" "
        output += "\nHome\t"
        for y, x in enumerate(home, start=1):
            if y>=10:
                output += str(x)+"  "
            else:
                output += str(x)+" "
        return output

def get_stats(game_id):
    '''
    Return individual stats of a game with matching id
    
    Should not be used other than as called by `__init__.py`
    '''
    year, month, day, rest = game_id.split('_', 3)
    filename = "gameday-data/year_%s/month_%s/day_%s/gid_%s/boxscore.xml" % (year, month, day, game_id)
    file = os.path.join(os.path.dirname(__file__), filename)
    if os.path.isfile(file):
        data = file
    else:
        data = url.urlopen("http://gd2.mlb.com/components/game/mlb/year_%s/month_%s/day_%s/gid_%s/boxscore.xml" % (year, month, day, game_id))
    parsed = etree.parse(data)
    root = parsed.getroot()
    pitching = root.findall('pitching')
    batting = root.findall('batting')
    home_pitching = []
    away_pitching = []
    home_batting = []
    away_batting = []
    for y in pitching:
        home=False
        if y.attrib['team_flag'] == "home":
            home = True
        for x in y.findall('pitcher'):
            stats = {}
            for i in x.attrib:
                stats[i]=x.attrib[i]
            if home:
                home_pitching.append(stats)
            elif not home:
                away_pitching.append(stats)
    for y in batting:
        home=False
        if y.attrib['team_flag'] == "home":
            home = True
        for x in y.findall('batter'):
            stats = {}
            for i in x.attrib:
                stats[i]=x.attrib[i]
            if home:
                home_batting.append(stats)
            elif not home:
                away_batting.append(stats)
    output = {'home_pitching':home_pitching, 'away_pitching':away_pitching, 'home_batting':home_batting, 'away_batting':away_batting}
    return output

class GameStats():
    '''
    Holds stat object for all players in a game
    '''
    pass

class PitcherStats(object):
    '''
    Holds stats information for a pitcher
    '''
    def __init__(self, data):
        '''
        Creates a pitcher object that matches the corresponding stats in `data`
        
        `data` should be a dictionary for a single pitcher that comes from `get_stats()`
        '''
        for x in data:
            try:
                setattr(self, x, int(data[x]))
            except ValueError:
                setattr(self, x, data[x])
    
    def nice_output(self):
        '''
        Prints basic player stats in a nice way
        '''
        return "%s - %i Earned Runs, %i Strikouts, %i Hits" % (self.name, self.er, self.so, self.h)
    
    def __str__(self):
        return self.nice_output()