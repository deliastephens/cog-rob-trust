(define (domain human-domain-1)

  (:requirements :strips :typing)

  (:predicates
    (at ?obj - locatable ?loc - location)
    (adj ?l1 - location ?l2 - location)
    (clear ?loc - location))
  
  (:types
    location locatable - object
    robot - locatable)

  (:action robot-move
    :parameters (?r - robot ?l1 - location ?l2 - location)
    :precondition (and (at ?r ?l1)
                        (adj ?l1 ?l2)
                        (clear ?l2))
    :effect (and (not (at ?r ?l1))
                  (at ?r ?l2))))