st = [96, 97, 98, 67, 68, 36, 37, 38]
co = 8
map_arr = []
mark_size = 0.223
mark_sep = 0.3

for i in range(co):
    a = []
    a = st.copy()

    for j in range(len(a)):
        a[j]+=3*i
    map_arr.append(a)

# print(map_arr)
f = open("map_gen_1.txt", "w+")
for i in range(len(map_arr)-1, -1,  -1): 
    for j in range(len(map_arr[i])-1,-1, -1): 
        x = round(j*0.3, 2)
        y = round((len(map_arr)-i-1)*0.3, 2)
        f.write(str(str(map_arr[i][j])+ "\t" + str(mark_size) + "\t" + str(x)  + "\t" + str(y)  + "\t0\t0\t0\t0\n"))
        map_arr[i][j] = (map_arr[i][j], mark_size, x, y, 0, 0, 0, 0)
        
f.close()
print(map_arr)





        