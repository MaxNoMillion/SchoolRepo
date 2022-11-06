import java.io.*;
import java.util.Hashtable;
import javax.lang.model.util.ElementScanner14;

/* ***************************************************
 * <Andrew Steen>
 * <11-15-21>
 * <Infix2Postfix.java>
 *
 * <Converts Infix notation to Postfix notation and then solves the expression>
 *************************************************** */

public class Infix2Postfix
{
    public static void main(String[] args)
    {
        String postfixNotation = "";
        int i = 1;

        while (readNumLine(i) != null)
        {
        System.out.println(readNumLine(i));
        postfixNotation = infix2Postfix(readNumLine(i));
        System.out.println(postfixNotation);
        System.out.println(evaluatePostfix(postfixNotation));
        System.out.println();
        i++;
        }
    }

    private static String readNumLine(int lineNum)
    {
        String str = "";
        BufferedReader input;
        try
        {
            input = new BufferedReader(new FileReader("input"));
            for (int i = 0; i < lineNum; i++)
            {
                str = input.readLine();
            }
        }
        catch (IOException ioe)
        {
            ioe.printStackTrace();
        }   
        return str;
    }

    private static String infix2Postfix(String input)
    {
        // Priority
        char[] keys = {'(', '^', '*', '/', '+', '-', '\0'};
        int[] priors = {4, 3, 2, 2, 1, 1, 0};
        Hashtable infixPriority = createPriorityHash(keys, priors);
        char[] keys2 = {'^', '*', '/', '+', '-', '\0', '('};
        int[] priors2 = {2, 2, 2, 1, 1, 0};
        Hashtable stackPriority = createPriorityHash(keys2, priors2);

        Queue<Character> infixQ = new Queue<Character>();
        Queue<Character> postfixQ = new Queue<Character>();
        Stack<Character> operS = new Stack<Character>();
        char[] charInput = string2CharArr(input);
        char op = '\0';
        char token = '\0';

        for (int i = 0; i < charInput.length; i++)
            infixQ.Enqueue(charInput[i]);
        
        while (!infixQ.IsEmpty())      
        {                           
            token = infixQ.Dequeue();  
            if (Character.isDigit(token))
                postfixQ.Enqueue(token);
            else if (token == ')')
            {
                op = operS.Pop();
                while (op != '(')
                {
                    postfixQ.Enqueue(op);
                    op = operS.Pop();
                }
            }
            else
            {
                if (operS.IsEmpty())
                    op = '\0';
                else
                    op = operS.Peek();
                while ((Integer)stackPriority.getOrDefault(op, 0) >= (Integer)infixPriority.getOrDefault(token, 0))
                {
                    op = operS.Pop();
                    postfixQ.Enqueue(op);
                    if (operS.IsEmpty())
                        op = '\0';
                    else
                        op = operS.Peek();
                }
                operS.Push(token);
            }
        }

        while (!operS.IsEmpty())
        {
            op = operS.Pop();
            postfixQ.Enqueue(op);
        }
        
        String str = new String();;
        while(!postfixQ.IsEmpty())
            str += postfixQ.Dequeue();
        return str;
    }

    private static char[] string2CharArr(String input)
    {
        char[] charArr = input.toCharArray();
        return charArr;
    }

    private static Hashtable createPriorityHash(char[] charArr, int[] priority)
    {
        Hashtable hash = new Hashtable();
        for (int i = 0; i < charArr.length; i++)
        {
            try
            {
                hash.put(charArr[i], (Integer)priority[i]);
            }
            catch (Exception e)
            {
                hash.put(charArr[i], 0);
            }
        }
        return hash;
        
    }

    private static String evaluatePostfix(String input)
    {
        char[] charInput = string2CharArr(input);

        Stack<Double> postfixS = new Stack<Double>();

        for (int i = 0; i < charInput.length; i++)
        {
            if (Character.isDigit(charInput[i]))
                postfixS.Push(Double.valueOf(Character.getNumericValue(charInput[i])));
            else
            {
                double a = postfixS.Pop();
                double b = postfixS.Pop();
                postfixS.Push(eval(a, b, charInput[i]));
            }
        }
        return postfixS.Pop() + "";
    }

    private static double eval(double a, double b, char op)
    {
        if (op == '^')
            return Math.pow(b,a);
        else if (op == '*')
            return a * b;
        else if (op == '/')
            return b / a;
        else if (op == '+')
            return a + b;
        else if (op == '-')
            return b - a;
        else 
            return 0;
    }
}