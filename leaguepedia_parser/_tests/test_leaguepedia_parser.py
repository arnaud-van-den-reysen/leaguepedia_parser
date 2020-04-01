from unittest import TestCase
from leaguepedia_parser.leaguepedia_parser import LeaguepediaParser


class TestLeaguepediaParser(TestCase):
    def test___init__(self):
        lp = LeaguepediaParser()

        self.assertIsNotNone(lp.client)
        self.assertIsNotNone(lp.query)

    def test_get_tournament_regions(self):
        lp = LeaguepediaParser()

        regions = lp.get_tournament_regions()

        self.assertTrue('Korea' in regions)
        self.assertTrue('China' in regions)

    def test_get_tournament_level(self):
        lp = LeaguepediaParser()

        tournament_level = lp.get_tournament_level()

        self.assertTrue('Primary' in tournament_level)
        self.assertTrue('Secondary' in tournament_level)



    def test_get_tournaments(self):
        lp = LeaguepediaParser()

        for region in ['China', 'Europe', 'Korea']:
            tournaments = lp.get_tournaments(region, year=2020)
            self.assertGreater(tournaments.__len__(), 0)

    def test_get_games(self):
        lp = LeaguepediaParser()

        for tournament_name in ['LEC 2020 Spring', 'LCK 2020 Spring', 'LPL 2020 Spring']:
            games = lp.get_games(tournament_name)
            self.assertGreater(games.__len__(), 0)

    def test_get_picks_bans(self):
        lp = LeaguepediaParser()

        for tournament_name in ['LEC 2020 Spring', 'LCK 2020 Spring', 'LPL 2020 Spring']:
            games = lp.get_games(tournament_name, limit=1)
            pb = lp.get_picks_bans(games[0])
            self.assertIsNotNone(pb)

    def test_buggy_game(self):
        lp = LeaguepediaParser()

        for tournament_name in ['LEC 2020 Spring', 'LCK 2020 Spring', 'LPL 2020 Spring']:
            games = lp.get_games(tournament_name, limit=1)
            game = games[0]
            game['leaguepedia_game_id'] = 'BUG'
            pb = lp.get_picks_bans(game)
            self.assertIsNotNone(pb)

    def test_super_buggy_game(self):
        lp = LeaguepediaParser()

        for tournament_name in ['LEC 2020 Spring', 'LCK 2020 Spring', 'LPL 2020 Spring']:
            games = lp.get_games(tournament_name, limit=1)
            game = games[0]
            game['leaguepedia_game_id'] = 'BUG'
            game['team1_picks'] = 'BUG'
            with self.assertRaises(Exception):
                lp.get_picks_bans(game)

    def test_get_long_team_name(self):
        lp = LeaguepediaParser()

        self.assertEqual(lp.get_long_team_name('tsm'), 'Team SoloMid')
        self.assertEqual(lp.get_long_team_name('IG'), 'Invictus Gaming')
        self.assertIsNone(lp.get_long_team_name('mister mv'))

    def test_get_team_logo(self):
        lp = LeaguepediaParser()

        self.assertIsNotNone(lp.get_team_logo('T1'))
        self.assertIsNotNone(lp.get_team_logo('G2 Esports'))
