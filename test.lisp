; Factorial with basic recursion
(def! fact 
  (fn* (n)
    (if (= n 1)
      1
      (* n (fact (- n 1)))
    )
  )
)

; Factorial with tail recursion
(def! fact2
  (fn* (n tot)
    (if (= n 1)
      tot
      (fact2 (- n 1) (* tot n))
    )
  )
)

; Fibonacci with basic recursion
(def! fib
  (fn* (limit)
    (if (= limit 0)
      0
      (if (= limit 1)
        1
        (+ (fib (- limit 1)) (fib (- limit 2)))
      )
    )
  )
)

; Fibonacci with tail recursion
(def! fib2-rec
  (fn* (limit count before-last last)
    (if (= count limit)
      before-last
      (fib2-rec limit (+ count 1) last (+ before-last last))
    )
  )
)

; Driver function for the above recursive version
(def! fib2
  (fn* (limit)
    (fib2-rec limit 0 0 1)
  )
)