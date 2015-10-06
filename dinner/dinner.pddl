; This is a comment line
(define (domain dinner) ; There is no block comment like
  (:requirements :strips)
  (:predicates
    (clean)
    (dinner)
    (quiet)
    (present)
    (garbage)
  )
  (:action cook
    :parameters ()
    :precondition (and
      (clean)
    )
    :effect (and
      (dinner)
    )
  )
  (:action wrap
    :parameters ()
    :precondition (and
      (quiet)
    )
    :effect (and
      (present)
    )
  )
  (:action carry
    :parameters ()
    :precondition (and
      (garbage)
    )
    :effect (and
      (not (garbage))
      (not (clean))
    )
  )
  (:action dolly
    :parameters ()
    :precondition (and
      (garbage)
    )
    :effect (and
      (not (garbage))
      (not (quiet))
    )
  )
)