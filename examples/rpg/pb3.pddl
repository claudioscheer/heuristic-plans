(define (problem pb3)
    (:domain rpg)

    (:objects
        room_1 room_2 room_3
        room_4 room_5 room_6 room_7 - room
        hero_1 - hero
    )

    (:init
        (hero_at hero_1 room_1)
        (empty_handed hero_1)
        (monster_angry room_3)
        (monster_angry room_5)
        (sword_at room_4)
        (trap_armed room_6)
        (valid_move room_1 room_2)
        (valid_move room_1 room_4)
        (valid_move room_2 room_1)
        (valid_move room_2 room_3)
        (valid_move room_2 room_5)
        (valid_move room_3 room_2)
        (valid_move room_3 room_6)
        (valid_move room_4 room_1)
        (valid_move room_4 room_5)
        (valid_move room_5 room_4)
        (valid_move room_5 room_2)
        (valid_move room_5 room_6)
        (valid_move room_6 room_5)
        (valid_move room_6 room_3)
        (valid_move room_6 room_7)
        (valid_move room_7 room_6)
    )

    (:goal (and
        (hero_at hero_1 room_7)
    ))
)