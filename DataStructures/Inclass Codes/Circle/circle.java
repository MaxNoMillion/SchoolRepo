class Circle
{
    private int radius;
    
    public Circle() //constructor
    {
        radius = 0;
    }

    public Circle(int radius)
    {
        this.radius = radius;
    }

    //An accessor for radius
    public int getRadius()
    {
        return this.radius;
    }
    // A mutator for radius
    public void setRadius(int radius)
    {
        this.radius = radius;
    }

    public boolean Equals(Circle other)
    {
        return (this.radius == other.radius);
    }
}
