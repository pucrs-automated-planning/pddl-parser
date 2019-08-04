(define (domain blocksworld)
  (:requirements :strips :negative-preconditions)
  (:predicates (clear ?x) (onTable ?x) (holding ?x) (on ?x ?y))

  (:action pickup
    :parameters (?ob)
    :precondition (and (clear ?ob) (onTable ?ob))
    :effect (and (holding ?ob) (not (clear ?ob)) (not (onTable ?ob)))
  )

  (:action putdown
    :parameters (?ob)
    :precondition (holding ?ob)
    :effect (and (clear ?ob) (onTable ?ob) (not (holding ?ob)))
  )

  (:action stack
    :parameters (?ob ?underob)
    :precondition (and (clear ?underob) (holding ?ob) (not (equal ?ob ?underob)))
    :effect (and (clear ?ob) (on ?ob ?underob) (not (clear ?underob)) (not (holding ?ob)))
  )

  (:action unstack
    :parameters (?ob ?underob)
    :precondition (and (on ?ob ?underob) (clear ?ob) (not (equal ?ob ?underob)))
    :effect (and (holding ?ob) (clear ?underob) (not (on ?ob ?underob)) (not (clear ?ob)))
  )
)