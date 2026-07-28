import random



print("This is guessing game ,guess any number between 1 to 9 lets see how many attempts its took to guess the right number ")

ans_number=random.randint(1,9)
attempts=0

   

while True:

  guessed_number=input("guess the number ")


  if(guessed_number.lower()=='exit'):
     break

  guessed_number=int(guessed_number)

  if(guessed_number>ans_number):
     attempts+=1
     print("your number is bigger than ans")
  elif(guessed_number<ans_number):
     attempts+=1
     print("your number is smaller than ans")

  else:
     attempts+=1
     print(f"bingo you guessed the right number and it took {attempts} attempts")
     break

