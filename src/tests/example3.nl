int x = 5;
byte y = 3;
func myFunc(int numb, byte otherval) int {
    return numb + 1;
}
func main() int {
    int z = myFunc(x,y);
    z = ((z + 2) % 3) + 4;
    int new_num = 100;
    return 0;
}