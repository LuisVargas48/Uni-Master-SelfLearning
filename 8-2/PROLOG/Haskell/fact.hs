fact :: Int -> Int
fact 0 = 1
fact n = n * fact (n-1)

main = do 
  putStrLn "The factorial of 20 is: " 
  print (fact 20)

