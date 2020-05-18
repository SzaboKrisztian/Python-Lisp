; If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

; Find the sum of all the multiples of 3 or 5 below 1000.

; Functions that returns the value if it is a multiple of 3 or 5, otherwise 0
(def! is-mult
  (fn*
    (n)
    (if (= (% n 3) 0)
      n 
      (if (= (% n 5) 0)
        n
        0
      )
    )
  )
)

; Recursive function that adds together all the multiples of 3 and 5 up to the limit
(def! euler1
  (fn*
    (limit total)
    (if (= limit 0)
      total
      (euler1 (- limit 1) (+ total (is-mult limit)))
    )
  )
)

(prn (euler1 999 0))