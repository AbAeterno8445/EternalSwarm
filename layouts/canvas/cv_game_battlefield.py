import math
import level_building as buildings
import level_unit as units


# Process game battle (buildings and units)
# Returns a dictionary with relevant battle data, to be used by canvas_game
def process_battle(cv_game):
    remove_buildings = []
    remove_units = []
    mapx, mapy = cv_game.levelmap.get_position()
    for h in range(cv_game.levelmap.height):
        # Process units
        for u in cv_game.unit_list[h]:
            u.tick()

            u_x, u_y = u.get_position()
            u_w = u.get_width()
            # Process walking units
            if u.state == units.state_walk:
                # Check for opposing units to battle
                u_range = 20 + u.get_width() / 2  # TODO change to unit range variable
                for u_other in cv_game.unit_list[h] + cv_game.building_list[h]:
                    if u is u_other or u_other.player_owned == u.player_owned or u_other.hp <= 0:
                        continue
                    u_otherx, u_othery = u_other.get_position()
                    u_otherw = u_other.get_width()
                    if abs((u_x + u_w / 2) - (u_otherx + u_otherw / 2)) < u_range:
                        if (u.player_owned and u_x < u_otherx) or (not u.player_owned and u_x > u_otherx):
                            u.set_battle_target(u_other)

                # Check if unit is out of bounds and fade/delete it if so, damage player as well
                if not u.state == units.state_fade:
                    u_mapx = math.floor(abs(mapx - u_x) / 48)
                    if (u_x and u_x < mapx - 8) or u_mapx >= cv_game.levelmap.width:
                        u.switch_state(units.state_fade)
                        if not u.player_owned:
                            cv_game.add_health(-u.dmg_player)
            # Process battling units
            elif u.state == units.state_battle:
                if u.is_attack_ready() and u.battle_target:
                    u.battle_target.hurt(u.get_damage_total())
                    if u.battle_target.hp <= 0:
                        u.battle_target = None
                        u.switch_state(units.state_walk)
                    else:
                        u.reset_attack()
                elif (u.battle_target and u.battle_target.hp <= 0) or not u.battle_target:
                    u.switch_state(units.state_walk)
            # Delete units
            elif u.state == units.state_delete:
                remove_units.append(u)
        # Process buildings
        for b in cv_game.building_list[h]:
            b.tick()
            if b.type == buildings.buildtype_spawner:
                if b.is_unit_ready():
                    cv_game.create_unit_at(b.x, b.y, b.player_owned, b.spawn_unit)
                    b.reset_spawn()
            if b.hp <= 0:  # Building destroyed
                remove_buildings.append(b)
                # If building is owned by enemy, progress level
                if not b.player_owned:
                    cv_game.levelmap.enemy_buildings -= 1

    battle_data = {
        "remove_units": remove_units,
        "remove_buildings": remove_buildings
    }
    return battle_data