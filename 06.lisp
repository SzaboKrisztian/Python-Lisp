;; The sum of the squares of the first ten natural numbers is,
;; 1^2+2^2+...+10^2=385

;; The square of the sum of the first ten natural numbers is,
;; (1+2+...+10)^2=552=3025

;; Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025−385=2640

;; Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.

; Recursive function that generates a list of numbers between 1 and limit, inclusive
(def! gen-nums
  (fn* (limit nums)
    (if (= limit 0)
      nums
      (gen-nums (- limit 1) (cons limit nums))
    )
  )
)

; Recursive function that returns the sum of the elements of a list
(def! sum-list-rec
  (fn* (nums total)
    (if (empty? nums)
      total
      (sum-list-rec (rest nums) (+ total (first nums)))
    )
  )
)

; Driver function for the above one
(def! sum-list
  (fn* (nums)
    (sum-list-rec nums 0)
  )
)

; Function that computes the square of the input
(def! square
  (fn* (n) (* n n))
)

; Recursive function that returns the list obtained by applying "func" to each element of "lst"
(def! map-rec
  (fn* (func lst res)
    (let* (num_items (count res))
      (if (= num_items (count lst))
        res
        (map-rec func lst (concat res (list (func (nth lst num_items)))))
      )
    )
  )
)

; Driver function for the above
(def! map
  (fn* (func lst)
    (map-rec func lst '())
  )
)

(let* (numerosos (gen-nums 100 '())
      sum-squares (sum-list (map square numerosos))
      square-sum (square (sum-list numerosos)))
  (prn (- square-sum sum-squares))
)