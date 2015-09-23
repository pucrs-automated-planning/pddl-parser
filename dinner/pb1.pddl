(define (problem pb1)
  (:domain dinner)
  (:init
    (garbage)
    (clean)
    (quiet)
  )
  (:goal (and
    (dinner)
    (present)
    (not (garbage))
  ))
)