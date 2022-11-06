// declares an array of 10 integer values and passes to function that sums

class Array
{
	public static void main(String [] args)
	{
	// declaring array
	int[] intArray = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
	int value = 0;
	value = sumArray(intArray);
	
	System.out.println("The sum is " + value);
	
	}
	
	public static int sumArray(int[] array)
	{
		int val = 0;
		for(int i=0; i<array.length; i++)
		{
			val += array[i];
		}
		
		return val;
	}
}