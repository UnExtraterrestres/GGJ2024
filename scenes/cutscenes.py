import batFramework as bf
from .cutsceneBlocks import *


class Test(bf.Cutscene):
    def __init__(self):
        super().__init__()

        self.add_blocks(
            bf.FunctionBlock(lambda : print("START")),
            bf.FunctionBlock(lambda : bf.CutsceneManager().disable_player_control()),
            Say("HELLO GUYS ! what's up ?",1),
            SayKey("test",1),
            bf.FunctionBlock(lambda : bf.CutsceneManager().enable_player_control()),
            bf.FunctionBlock(lambda : print("END")),
            bf.FunctionBlock(lambda : bf.CutsceneManager().manager.set_scene("main"))
        )


class ObjectifDonne(bf.Cutscene):

    def __init__(self):
        super().__init__()

        self.add_blocks(
            SayKey("objectif_pj_bonjour", 1),
            SayKey("objectif_fr_demande1", 1),
            SayKey("objectif_fr_demande2", 1),
            SayKey("objectif_fr_demande3", 1),
            SayKey("objectif_pj_refus", 1),
            SayKey("objectif_fr_menace1", 1),
            SayKey("objectif_pj_accepte1", 1),
            SayKey("objectif_fr_menace2", 1),
            SayKey("objectif_pj_accepte2", 1),
            bf.FunctionBlock(lambda: bf.CutsceneManager().manager.set_scene("main"))
        )


class RencontreLutinParser(bf.Cutscene):

    def __init__(self):
        super().__init__()

        self.add_blocks(
            SayKey("lutin_bonjour", 1),
            SayKey("pj_salutation", 1),
            SayKey("lutin_proposition", 1),
            SayKey("pj_accueil_lutin", 1),
            SayKey("lutin_intro_parser", 1),

            bf.FunctionBlock(lambda: bf.CutsceneManager().manager.set_scene("main"))
        )


class Twist(bf.Cutscene):

    def __init__(self):
        super().__init__()

        self.add_blocks(
            # Le joueur atteint un endroit clé avec le lutin parcer
            SayKey("pj_question_lutin_parcer", 1),

            # Le lutin parcer révèle la vérité
            SayKey("lutin_parcer_explication", 1),
            SayKey("lutin_parcer_explication2", 1),
            SayKey("pj_realisation", 1),

            # Le lutin parcer encourage le joueur à continuer malgré tout
            SayKey("lutin_parcer_encouragement", 1),
            SayKey("pj_accepte_revelation", 1),
            SayKey("pj_vraie_solution", 1),

            bf.FunctionBlock(lambda: bf.CutsceneManager().manager.set_scene("main"))
        )
