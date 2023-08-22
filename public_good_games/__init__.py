from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'public_good_games'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 1
    ENDOWMENT = cu(20)
    MULTIPLIER = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label='How many tokens do you think are in your group account?'
    )
    code_number = models.IntegerField(label="Code Number")
    ncsu = models.StringField(label="NCSU Student ID number")
    gender = models.StringField(widget=widgets.RadioSelect, choices=['Male', 'Female'], label="Gender")
    major = models.StringField(label="Major")
    semester = models.IntegerField(label="Semester currently in")
    invest = models.IntegerField(
        widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    )
    profit_tokens = models.CurrencyField()


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    total_invest = [p.invest for p in players]
    group.total_contribution = sum(total_invest)
    for p in players:
        group.individual_share = (
            (C.ENDOWMENT - p.contribution) + ((group.total_contribution * C.MULTIPLIER) / C.PLAYERS_PER_GROUP)
        )
        p.profit_tokens = group.individual_share / 4
        p.payoff = p.profit_tokens


# PAGES
class InstructionsSheet(Page):
    pass


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['code_number', 'ncsu', 'gender', 'major', 'semester']


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution', 'invest']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


class FinalResults(Page):
    pass


# page_sequence = [InstructionsSheet, Questionnaire, Contribute, ResultsWaitPage, Results, FinalResults]
page_sequence = [InstructionsSheet, Contribute, ResultsWaitPage, Results, FinalResults]