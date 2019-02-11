number_points = 11
total_number_points = 44

# theta test        ------>       test for interger division of number to find what theta to assign to each point
print(4 /11)
print(10 / 11)
print(11 / 11)
print(16 / 11)
print(18 / 11)
print(24 / 11)
print(30 / 11)
print(36 / 11)
print(39 / 11)

# phi test
print(0 % 11)
print(11 % 11)
print(22 % 11)
print(33 % 11)
print('space')
print(12 % 11)
print(13 % 11)
print(14 % 11)

list = [0] * total_number_points
for i in range(1,total_number_points + 1,1):
    if ((i-1) / number_points) % 2 == 0:
        list[i-1] = (i - 1) % number_points
    else:
        list[i-1] = 10 - ((i - 1) % 11
print(list)
