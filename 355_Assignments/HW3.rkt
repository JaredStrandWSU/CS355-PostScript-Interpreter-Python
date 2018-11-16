#lang racket
(require racket/stream)

;Alg Logic: base case is empty list to be returned createst pair that appends to cdr of list otherwise list is our return val
[define (FlattenFunction L)
  (cond	((empty? L) 
         '())
        ((pair? L)
         (append(FlattenFunction (car L)) (FlattenFunction (cdr L))))
        (else 
         (list L))
        )]
;Alg Logic: base case is empty, if n is 0(first elem) replace, else traverse list until value is num elem we're looking for
[define (ReplaceNthFunction n v L)
  (cond	((empty? L)
         '())
        ((zero? n)
         (cons v (ReplaceNthFunction (- n 1) v (cdr L))))
        (else
         (cons (car L) (ReplaceNthFunction (- n 1) v (cdr L))))
        )]

[define (MergeUnique2Function L1 L2);
  (cond	((and (empty? L1) (empty? L2))
         '())
        ((empty? L1)
         (cons (car L2) (MergeUnique2Function '() (cdr L2))))
        ((empty? L2)
         (cons (car L1) (MergeUnique2Function (cdr L1) '())))
        ((< (car L1) (car L2))
         (cons (car L1) (MergeUnique2Function (cdr L1) L2)))
        ((> (car L1) (car L2))
         (cons (car L2) (MergeUnique2Function L1 (cdr L2))))
        (else
         (cons (car L1) (MergeUnique2Function (cdr L1) (cdr L2))))
        )]

[define (MergeUniqueNFunction Ln)
  (foldr MergeUnique2Function '() Ln)]

;map car and cadr
[define (UnzipFunction List1)
  (cons (map car List1) (cons (map cadr List1) '()))
  ]

;Alg Logic: calls helper to add and sum vals 
[define (NthHelper sum temp rL L)
  (cond	((< (+ temp (car L)) sum)
         (NthHelper sum (+ temp (car L)) (cons (car L) rL) (cdr L)))
        (else
         (reverse rL))
        )]

;helper adder
[define (NumbersToSumFunction sum L)
  (NthHelper sum 0 '() L)
  ]

;stream of squares. anonymous fun, 
(define StreamofSquares
  (letrec (
           [f (lambda (x y) (cons x (lambda () (f (* y y) (+ y 1)))))])
    (lambda () (f 1 2))))

;nnum until stream 
(define (NumTil stream n)
  (if (<= n (car (stream)))
      '()
      (cons (car (stream))  (NumTil (cdr (stream)) n))) )

(define (StreamSumHelper stream curSum maxSum)
  (if (>= (+ curSum (car(stream))) maxSum)
      '()
      (cons (car (stream))  (StreamSumHelper (cdr (stream)) (+ curSum (car(stream))) maxSum))))
(define (StreamSum sum S)
  (StreamSumHelper StreamofSquares 0 sum))
;TESTS
(define (Bool2str val) (if val "true" "false"))

(define (TestFlatten)
  (let* ([T1 (equal? (FlattenFunction '(1 (2 (3 4(5 6)7(8(9(10)11))))))'(1 2 3 4 5 6 7 8 9 10 11))]
         [T2 (equal? (FlattenFunction '((1)(2 (2)) (3(3(3))) (4(4(4(4)))))) '(1 2 2 3 3 3 4 4 4 4))]
         [T3 (equal? (FlattenFunction '( () )) '())])
    (display(string-append "\n-------\n Flatten \n
                              T1: " (Bool2str T1)
                           ", T2: " (Bool2str T2)
                           ", T3: " (Bool2str T3)))))

(define (TestReplace)
  (let* ([T1 (equal? (ReplaceNthFunction 3 40 '(1 2 3 4 (5) "6"))'(1 2 3 40 (5) "6"))]
         [T2 (equal? (ReplaceNthFunction 4 5 '(1 2 3 4 (5) "6")) '( 1 2 3 4 5 "6"))]
         [T3 (equal? (ReplaceNthFunction 0 9 '("6" 10 11 12)) '(9 10 11 12))])
    (display(string-append "\n-------\n Replace \n
                              T1: " (Bool2str T1)
                           ", T2: " (Bool2str T2)
                           ", T3: " (Bool2str T3)))))

(define (TestMergeUnique)
  (let* ([T1 (equal? (MergeUnique2Function '(4 6 7) '(3 5 7)) '(3 4 5 6 7))]
         [T2 (equal? (MergeUnique2Function '(1 5 7) '(2 5 7)) '(1 2 5 7))]
         [T3 (equal? (MergeUnique2Function '() '(3 5 7)) '(3 5 7))])
    (display(string-append "\n-------\n mergeUnique2 \n
                              T1: " (Bool2str T1)
                           ", T2: " (Bool2str T2)
                           ", T3: " (Bool2str T3)))))

(define (TestMergeUniqueN)
  (let* ([T1 (equal? (MergeUniqueNFunction '()) '())]
         [T2 (equal? (MergeUniqueNFunction '((2 4 6) (1 4 5 6))) '(1 2 4 5 6))]
         [T3 (equal? (MergeUniqueNFunction '((2 4 6 10) (1 3 6) (8 9))) '(1 2 3 4 6 8 9 10))])
    (display(string-append "\n-------\n MergeUniqueN \n
                              T1: " (Bool2str T1)
                           ", T2: " (Bool2str T2)
                           ", T3: " (Bool2str T3)))))

(define (TestUnzip)
  (let* ([T1 (equal? (UnzipFunction '((1 2) (3 4) (5 6))) '((1 3 5) (2 4 6)))]
         [T2 (equal? (UnzipFunction '((1 “a”) (5 “b”) (8 “c”))) '((1 5 8) (“a” “b” “c”)))])
    (display(string-append "\n-------\n unzip \n
                              T1: " (Bool2str T1)
                           ", T2: " (Bool2str T2)))))

(define (TestNumbersToSum)
  (let* ([T1 (equal? (NumbersToSumFunction 100 '(10 20 30 40)) '(10 20 30))]
         [T2 (equal? (NumbersToSumFunction 30 '(5 4 6 10 4 2 1 5)) '(5 4 6 10 4))]
         [T3 (equal? (NumbersToSumFunction 5 '(5 4 6)) '())])
    (display(string-append "\n-------\n numbersToSum \n
                              T1: " (Bool2str T1)
                           ", T2: " (Bool2str T2)
                           ", T3: " (Bool2str T3)))))

(define (TestStreamSum)
  (let* ([T1 (equal? (last (StreamSum 10000 StreamofSquares)) 900)]
         [T2 (equal? (last (StreamSum 99999999999 StreamofSquares)) 44796249)]
         [T3 (equal? (last (StreamSum 999999 StreamofSquares)) 1413)])
    (display(string-append "\n-------\n streamSum \n
                              T1: " (Bool2str T1)
                           ", T2: " (Bool2str T2)
                           ", T3: " (Bool2str T3)))))

;Call the test function
(TestFlatten)
(TestReplace)
(TestMergeUnique)
(TestMergeUniqueN)
(TestUnzip)
(TestNumbersToSum)
(TestStreamSum)