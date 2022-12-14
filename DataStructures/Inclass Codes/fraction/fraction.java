class Fraction
{
    private int num;
    private int den;

    public Fraction()
    {
        num = 0;
        den = 1;
    }

    public Fraction(int num, int den)
    {
        this.num = num;
        this.den = den;
    }

    // Accessors and Mutators
    public int getNum()
    {
        return this.num;
    }
    public void setNum(int num)
    {
        this.num = num;
    }

    public int getDen()
    {
        return this.den;
    }
    public void setDen(int den)
    {
        this.den = den;
    }

    public String toString()
    {
        return this.num + "/" + this.den;
    }
}