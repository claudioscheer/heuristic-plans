(define (domain rpg)

    (:requirements :strips :typing :negative-preconditions)

    (:types
        room
        hero
    )

    (:predicates
        (hero_at ?hero - hero ?x - room)
        (goal_at ?hero - hero ?x - room)
        (monster_angry ?x - room)
        (trap_armed ?x - room)
        (sword_at ?x - room)
        (visited_room ?x - room)
        (valid_move ?from - room ?to - room)
        (empty_handed ?x - hero)
    )

    (:action move
        :parameters (?hero - hero ?from - room ?to - room)
        :precondition (and
            (not (goal_at ?hero ?from)) ; Ensures that the hero has not yet reached the goal.
            (hero_at ?hero ?from) ; Hero must be at ?from room.
            (valid_move ?from ?to) ; It must to be a valid move on the board.
            (not (visited_room ?from)) ; The room can not have been visited.
            (not (visited_room ?to)) ; The room can not have been visited.
            (not (trap_armed ?from)) ; Hero can not move with an armed trap.
            (not (monster_angry ?from)) ; Hero can not move with the monster angry.
            (not (and
                (monster_angry ?to)
                (empty_handed ?hero)
                ; Condition to ensure that the hero does not go to ?to, which has a monster, empty-handed.
            ))
        )
        
        :effect (and
            (hero_at ?hero ?to) ; Hero changes position.
            (visited_room ?from) ; ?from has now been visited.
        )
    )

    (:action get_sword
        :parameters (?hero - hero ?location - room)
        :precondition (and
            (hero_at ?hero ?location) ; Hero must be at ?location room.
            (not (visited_room ?location)) ; The room can not have been visited.
            (sword_at ?location) ; Sword must be at ?location room.
            (empty_handed ?hero) ; Hero does not have a sword.
        )
        
        :effect (and
            (not (empty_handed ?hero)) ; Hero is no longer empty-handed.
        )
    )

    (:action drop_sword
        :parameters (?hero - hero ?location - room)
        :precondition (and
            (hero_at ?hero ?location) ; Hero must be at ?location room.
            (not (empty_handed ?hero)) ; Hero must hold a sword.
            (trap_armed ?location) ; Trap is armed at ?location.
        )
        
        :effect (and
            (empty_handed ?hero) ; Hero no longer holds a sword.
        )
    )

    (:action hug_monster
        :parameters (?hero - hero ?location - room)
        :precondition (and
            (hero_at ?hero ?location) ; Hero must be at ?location room.
            (monster_angry ?location) ; Monster must be angry at ?location room.
            (not (empty_handed ?hero)) ; Hero have the sword.
        )
        
        :effect (and
            (not (monster_angry ?location)) ; Hug the monster.
            ; I could move the hero forward here, but I think it is more consistent to let the move action do that.
        )
    )

    (:action disarm_trap
        :parameters (?hero - hero ?location - room)
        :precondition (and
            (hero_at ?hero ?location) ; Hero must be at ?location room.
            (trap_armed ?location) ; Trap is armed at ?location.
            (empty_handed ?hero) ; Hero can not have a sword.
        )
        
        :effect (and
            (not (trap_armed ?location)) ; Disarm the trap at ?location.
        )
    )
)