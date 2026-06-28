import Constants as cons
class GameState:
    # Main game flow
    start_game: bool = False
    pause_game: bool = False
    game_over: bool = False
    game_run: bool = True

    #music
    level1_music_start:bool=False
  

    # Intro / transition
    start_intro: bool = False
    opening_intro: bool = False

    # Shop / dialog
    is_shopmenu: bool = False
    is_purchased: bool = False
    not_purchased: bool = False
    is_dialog_active: bool = False
    wants_close_dialog: bool = False
    dialog_message: str = ""

    # Level
    current_level: str = "1"
    level_complete_shop: bool = False
    pending_level_load: bool = False

    # Level flags
    is_level1: bool = True
    is_level2: bool = False
    is_level3: bool = False

    # Goal dialogs
    show_goal_dialog_l1: bool = False
    show_goal_dialog_l2: bool = False
    show_goal_dialog_l3: bool = False

    # Waves
    current_wave: int = 0
    wave_active: bool = False
    wave_cleared: bool = False
    enemy_left: int = 0

    # Boss
    is_boss_spawned: bool = False
    phase2_triggered: bool = False

    # Player / alliance related state
    has_alliance: bool = False
    potion_spawned: bool = False
    was_freezed: bool = False

    # Character selection
    player_name: str = ""
    selected_gender: str = "Female"
    choosing: bool = True

    #timer
    opening_intro_timer: int = cons.INTRO_TIMER
    game_over_timer: int = cons.GAME_OVER_TIMER
    victory_timer: int = cons.VICTORY_TIMER
    show_dialog_timer: int = 3000

    item_spawn_cooldown: int = 0
    fire_spawn_timer: int = 0
    turnado_spawn_timer: int = 0
    finish_anime: int = cons.DEATH_PLAY

    #goal
    had_enough_socre=False


    def set_level(self, level: str) -> None:
        self.current_level = level
        self.is_level1 = level == "1"
        self.is_level2 = level == "2"
        self.is_level3 = level == "3"

    def reset_wave_state(self) -> None:
        self.current_wave = 0
        self.wave_active = False
        self.wave_cleared = False
        self.enemy_left = 0

    def reset_boss_state(self) -> None:
        self.is_boss_spawned = False
        self.phase2_triggered = False
    
    def set_level(self, level):
        self.current_level = level
        self.is_level1 = level == '1'
        self.is_level2 = level == '2'
        self.is_level3 = level == '3'