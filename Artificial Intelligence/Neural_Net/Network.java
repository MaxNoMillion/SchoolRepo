//////////////////////////////////////////////////////////////////////////
// Name: Andrew Steen                                                   //
// SWID: 102-68-080                                                     //
// Date: Oct 28 2022                                                    //
// Assignment #: 2                                                      //
// Program Discription: 3-Layer neural network that uses sochastic      //
//    gradient descent to guess the digit of handwritten numbers.       //
//////////////////////////////////////////////////////////////////////////

// Imports
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

/**    Helper Classes     **/

// Class for creating weight arrays
class Weight {
  private double weights[][];
  public Weight(int row_size, int col_size, boolean isRandom){
    this.weights = new double[row_size][col_size];

    // Used to generate initial random weight values
    if (isRandom) {
      Random random = new Random();
      for (int i = 0; i < weights.length; i++){
        for (int j = 0; j < weights[i].length; j++){
          this.weights[i][j] = random.nextDouble()*2 - 1;     // Generates value between 0 and 1 so I
        }                                                     // multiplied each value by 2 and subtract
      }                                                       // by 1 to get a range of -1 to 1
    }
  }
  // Weight setters and getters
  public double[][] getWeights(){
    return this.weights;
  }
  public void setWeights(double[][] weight){
    this.weights = weight;
  }
}

// Class for creating bias arrays
class Bias {
  private double biases[];
  public Bias(int size, boolean isRandom){
    this.biases = new double[size];

    // Used to generate initial random bias values
    if (isRandom) {
      Random random = new Random();
      for (int i = 0; i < biases.length; i++){
        this.biases[i] = random.nextDouble()*2 - 1;         // Same as weights
      }
    }
  }
  // Bias setters and getters
  public double[] getBiases(){
    return this.biases;
  }
  public void setBiases(double[] bias){
    this.biases = bias;
  }
}

// Class for creating WeightGradient arrays
class WeightGradient {
  private double weight_gradients[][];
  public WeightGradient(int row_size, int col_size){
    this.weight_gradients = new double[row_size][col_size];
  }
  // WeightGradient setters and getters
  public double[][] getWeightGradients(){
    return this.weight_gradients;
  }
  public void setWeightGradients(double[][] weight_gradient){
    this.weight_gradients = weight_gradient;
  }
}

// Class for creating BiasGradient arrays
class BiasGradient {
  private double bias_gradients[];
  public BiasGradient(int size){
    this.bias_gradients = new double[size];
  }
  // BiasGradient setters and getters
  public double[] getBiasGradients(){
    return this.bias_gradients;
  }
  public void setBiasGradients(double[] bias_gradient){
    this.bias_gradients = bias_gradient;
  }
}


/////**    Main Class    **/////
public class Network {
  // PARAMETERS of Network //
  private static final double learning_rate = 0.5;
  private static final int hidden_layer_size = 200;
  private static final int input_size = 784;
  private static final int output_size = 10;
  private static final int training_data_size = 60000;
  private static final int testing_data_size = 10000;
  private static final int mini_batch_size = 10;
  private static final int epochs = 30;

  // Creating class variables for weights and biases for first and second layer
  // For ease of munipulating
  public static Weight weights1 = new Weight(hidden_layer_size, input_size, true);
  public static Bias biases1 = new Bias(hidden_layer_size, true);
  public static Weight weights2 = new Weight(output_size, hidden_layer_size, true);
  public static Bias biases2 = new Bias(output_size, true);

  /////// MAIN ///////
  public static void main(String[] args){
    // Network information for user (or shows on boot up)
    System.out.println("\n\nCurrent Network Parameters:");
    System.out.printf("  Deminsion of Network: %d by %d by %d", input_size, hidden_layer_size, output_size);
    System.out.printf("\n  Training Data Size: %d", training_data_size);
    System.out.printf("\n  Mini-Batch Info: %d mini-batches of size %d", training_data_size / mini_batch_size, mini_batch_size);
    System.out.printf("\n  Number of Epochs: %d", epochs);
    System.out.printf("\n  Learning Rate: %f", (float) learning_rate);
    System.out.printf("\n\nNow you may choose an option below.");

    boolean run = true;                 // Boolean parameter for exiting program.  
    boolean isNetworkLoaded = false;    // Boolean parameter for hiddening selections.

    // Main loop of program //
    while (run == true){                                                            // Switch run to false to exit program.
      System.out.println("\n\n\nDo you wish to:");                                      // Printing options
      System.out.println("  [1] Train the network");
      System.out.println("  [2] Load a pre-trained network");
      if (isNetworkLoaded == true){                                                 // Logic to only display first 2 options
        System.out.println("  [3] Display network accuracy on Training data");      // until either 1 or 2 is selected.
        System.out.println("  [4] Display network accuracy on Testing data");
        System.out.println("  [5] Save the network state to file");
      }
      System.out.println("  [0] Exit");
      
      Scanner scanner = new Scanner(System.in);
      String input = scanner.nextLine();

      // Selector for all posible options
      if (Integer.parseInt(input) == 1){
        System.out.print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"); // Just to make the user interface **dynamic**
        System.out.println("Training network...\n\n");
        trainNetwork();
        isNetworkLoaded = true;                                               // Makes other options selectable
      }
      else if (Integer.parseInt(input) == 2){
        System.out.println("\n\nLoading network weights and biases...\n\n");
        isNetworkLoaded = loadPreTrainedNetwork();                                              // Makes other options selectable
      }
      else if ((Integer.parseInt(input) == 3) && (isNetworkLoaded == true))   // Displays training data accuracy
        displayTrainingAccuracy();
      else if ((Integer.parseInt(input) == 4) && (isNetworkLoaded == true))   // Displays testing data accuracy
        displayTestingAccuracy();
      else if ((Integer.parseInt(input) == 5) && (isNetworkLoaded == true))   // Saves weights and biases of current network state
        saveNetworkState();
      else if (Integer.parseInt(input) == 0)                                  // Exits program
        run = false;
      else
        System.out.println("Please input only options listed.");            // If user types invalid input
    }
  }
  
  // For training neural network
  public static void trainNetwork(){
    // Resets weights and biases to be random.
    weights1 = new Weight(hidden_layer_size, input_size, true);
    biases1 = new Bias(hidden_layer_size, true);
    weights2 = new Weight(output_size, hidden_layer_size, true);
    biases2 = new Bias(output_size, true);
    BiasGradient bias_grad1 = new BiasGradient(hidden_layer_size);                    // Weight and Bias gradient objects
    BiasGradient bias_grad2 = new BiasGradient(output_size);
    WeightGradient weight_grad1 = new WeightGradient(hidden_layer_size, input_size);
    WeightGradient weight_grad2 = new WeightGradient(output_size, hidden_layer_size);
    double[] activation1 = new double[hidden_layer_size];                             // Arrays to store activation values
    double[] activation2 = new double[output_size];
    
    /// Intiating Reading of Data ///
    double[][] training_data = new double[training_data_size][input_size + 1];    // creating array to hold training data
                                                                                    // The +1 is for the first index of the data being the digit name
    // Reading data into array for ease of access.
    training_data = readData("mnist_train.csv", training_data);         // Fetches training data as 2D array

    // Normalizing Pixel Values
    for (int i = 0; i < training_data.length; i++)                               // Divides every data point by 255 save the first data point of each line
      for (int j = 1; j <input_size; j++)                                           // This is done to convert pixel value from 0-255 to 0.0-1.0
        training_data[i][j] = (double) training_data[i][j] / 255;

    // Creating ONE HOT VECTORS
    double[][] expected_out = new double[training_data_size][output_size];      // Creating 2D array to store all one-hot-vectors
    for (int i = 0; i < training_data.length; i++)                              
      expected_out[i][(int) training_data[i][0]] = 1;                           // Uses first digit of each line in training_data
                                                                                  // as the index of each one-hot-array


    ////// Start of Epoch Loop //////
    for (int epoch_num = 0; epoch_num < epochs; epoch_num++){
      // Variable initialization and reset
      int[] training_digit_counter = new int[output_size];
      int[] guessed_digit_counter = new int[output_size];

      // Shuffle training data //
      // with array of indexes of training data (allowing for fast shuffling of data)
      Integer[] training_data_index = new Integer[training_data_size];                        // Initializing array
      training_data_index = shuffleData(training_data_index);                                 // Shuffled Index array

      // Making mini-batches
      int[][] mini_batches = new int[training_data_size / mini_batch_size][mini_batch_size];  // 2D array that's 6000 x 10
      mini_batches = makeMiniBatches(mini_batches, training_data_index);


      // RUNS THROUGH 6000 MINIBATCHES //
      for (int batch_ind = 0; batch_ind < (training_data_index.length / mini_batch_size); batch_ind++){
        // Initialization and Reset of Summed Gradients for Later Calculations
        double[][] summ_weight_grad1 = new double[hidden_layer_size][input_size];
        double[][] summ_weight_grad2 = new double[output_size][hidden_layer_size];
        double[] summ_bias_grad1 = new double[hidden_layer_size];
        double[] summ_bias_grad2 = new double[output_size];


        // For each data sample in Mini-BATCH
        for (int i = 0; i < mini_batch_size; i++){
          // Forward Pass //
          // Layer 1
          double[] tempA = new double[hidden_layer_size];
          for (int j = 0; j < hidden_layer_size; j++)                                 // Dotting Weight1 matrix with input_data matrix
            for (int k = 0; k < input_size; k++)
              tempA[j] += weights1.getWeights()[j][k] * training_data[mini_batches[batch_ind][i]][k + 1];
          
          for (int j = 0; j < hidden_layer_size; j++)
            activation1[j] = sigmoid(tempA[j] + biases1.getBiases()[j]);              // Using sigmoid fn to get 0 to 1 smooth value
  
          // Layer 2
          double[] tempB = new double[output_size];                                   // Dotting Weight2 matrix with activation1 matrix
          for (int j = 0; j < output_size; j++)
            for (int k = 0; k < hidden_layer_size; k++)
              tempB[j] += weights2.getWeights()[j][k] * activation1[k];
           
          for (int j = 0; j < output_size; j++)
            activation2[j] = sigmoid(tempB[j] + biases2.getBiases()[j]);              // Using sigmoid fn to get 0 to 1 smooth value

          // Counts how many particuler digit appear in the data
          training_digit_counter[(int) training_data[mini_batches[batch_ind][i]][0]] += 1;
          // Counts how many particuler digits the network guesses correctly
          if ((int) training_data[mini_batches[batch_ind][i]][0] == getMaxValueIndex(activation2))
            guessed_digit_counter[getMaxValueIndex(activation2)] += 1;



          //// BackPROPOGATION ////
          // Bias Gradients for Layer 2
          double[] temp1 = new double[output_size];
          for (int j = 0; j < output_size; j++)                             // Final layer bias gradient equation
            temp1[j] = (activation2[j] - expected_out[mini_batches[batch_ind][i]][j]) * activation2[j] * (1 - activation2[j]);
          bias_grad2.setBiasGradients(temp1);

          // Weight Gradients for Layer 2
          double[][] temp2 = new double[output_size][hidden_layer_size];
          for (int j = 0; j < output_size; j++)                            // Final layer weight gradient equation
            for (int k = 0; k < hidden_layer_size; k++)
              temp2[j][k] = activation1[k] * bias_grad2.getBiasGradients()[j];
          weight_grad2.setWeightGradients(temp2);

          // Bias Gradient for Layer 1
          double[] temp3 = new double[hidden_layer_size];
          for (int j = 0; j < hidden_layer_size; j++)                       // Layer 1 bias gradient equation (Summation part)
            for (int k = 0; k < output_size; k++)
              temp3[j] += weights2.getWeights()[k][j] * bias_grad2.getBiasGradients()[k];
          for (int j = 0; j < hidden_layer_size; j++)                       // Layer 1 bias gradient equation (Activation part)
            temp3[j] *= activation1[j] * (1 - activation1[j]);
          bias_grad1.setBiasGradients(temp3);

          // Weight Gradient for Layer 1
          double[][] temp4 = new double[hidden_layer_size][input_size];
          for (int j = 0; j < hidden_layer_size; j++)                       // First layer weight gradient equation
            for (int k = 0; k < input_size; k++)
              temp4[j][k] = training_data[i][k + 1] * bias_grad1.getBiasGradients()[j];
          weight_grad1.setWeightGradients(temp4);


          ///// Summing gradients
          for (int j = 0; j < output_size; j++)                                       // Sums bias and weight gradients as
            summ_bias_grad2[j] += bias_grad2.getBiasGradients()[j];                     // program progresses through an
                                                                                        // individual mini-batch.
          for (int j = 0; j < output_size; j++)                                         // This is to help with calculating
            for (int k = 0; k < hidden_layer_size; k++)                                 // the new weights and biases.
              summ_weight_grad2[j][k] += weight_grad2.getWeightGradients()[j][k];
            
          for (int j = 0; j < hidden_layer_size; j++)
            summ_bias_grad1[j] += bias_grad1.getBiasGradients()[j];
          
          for (int j = 0; j < hidden_layer_size; j++)
            for (int k = 0; k < input_size; k++)
              summ_weight_grad1[j][k] += weight_grad1.getWeightGradients()[j][k];
        }

        //// End Mini-BATCH ////
        // Calc new weights and biases
        // Updated 2nd Layer Biases
        double[] temp11 = new double[output_size];
        for (int j = 0; j < output_size; j++)           // Updating equation (Must cast mini_batch_size to integer)
          temp11[j] = biases2.getBiases()[j] - ((learning_rate / (double) mini_batch_size) * summ_bias_grad2[j]);
        biases2.setBiases(temp11);

        // Updated 2nd Layer Weights
        double[][] temp12 = new double[output_size][hidden_layer_size];
        for (int j = 0; j < output_size; j++)           // Updating equation (Must cast mini_batch_size to integer)
          for (int k = 0; k < hidden_layer_size; k++)
            temp12[j][k] = weights2.getWeights()[j][k] - ((learning_rate / (double) mini_batch_size) * summ_weight_grad2[j][k]);
        weights2.setWeights(temp12);

        // Updated 1st Layer Biases
        double[] temp13 = new double[hidden_layer_size];
        for (int j = 0; j < hidden_layer_size; j++)           // Updating equation (Must cast mini_batch_size to integer)
          temp13[j] = biases1.getBiases()[j] - ((learning_rate / (double) mini_batch_size) * summ_bias_grad1[j]);
        biases1.setBiases(temp13);

        // Updated 2nd Layer Weights
        double[][] temp14 = new double[hidden_layer_size][input_size];
        for (int j = 0; j < hidden_layer_size; j++)           // Updating equation (Must cast mini_batch_size to integer)
          for (int k = 0; k < input_size; k++)
            temp14[j][k] = weights1.getWeights()[j][k] - ((learning_rate / (double) mini_batch_size) * summ_weight_grad1[j][k]);
        weights1.setWeights(temp14);
      }
      // Printing network accuracy every epoch
      System.out.println("Epoch: " + (epoch_num + 1));
      print_data(training_digit_counter, guessed_digit_counter);
    }
  }

  // For loading weights and biases from a preloaded file
  public static boolean loadPreTrainedNetwork(){
    // Asks with file to load
    System.out.print("What network state would you like to load? ");
    double[][] loaded_data = new double[hidden_layer_size + output_size + 2][input_size];
    Scanner scanner = new Scanner(System.in);

    loaded_data = readData(scanner.nextLine(), loaded_data);            // Loads in weights and bias data
    // If no file exsist the this if statement will be false
    if ((int) loaded_data[0][0] != -1){
      // Reading and formatting weights1
      double[][] w1 = new double[hidden_layer_size][input_size];        // Weights1, Weight2, Biases1, and Biases2 are all contained
      for (int i = 0; i < hidden_layer_size; i++)                         // in the same file where Weights1[0] is the first line and
        for (int j = 0; j < input_size; j++)                              // Weights1[1] is the second line. Weights2 comes directly after
          w1[i][j] = loaded_data[i][j];                                   // Weights1 on the next line, followed by Biases1 and Biases2
      weights1.setWeights(w1);     // Setting weights1                    // in the same manner. All in all, the loaded_date 2D array
                                                                          // is (input_size) x (hidden_layer_size + input_size + 2).
      // Reading and formatting weights2
      double[][] w2 = new double[output_size][hidden_layer_size];
      for (int i = 0; i < output_size; i++)
        for (int j = 0; j < hidden_layer_size; j++)
          w2[i][j] = loaded_data[i + hidden_layer_size][j];
      weights2.setWeights(w2);     // Setting weights2

      // Reading and formatting biases1
      double[] b1 = new double[hidden_layer_size];
      for (int i = 0; i < hidden_layer_size; i++)
        b1[i] = loaded_data[hidden_layer_size + output_size][i];
      biases1.setBiases(b1);      // Setting biases1

      // Reading and formatting biases2
      double[] b2 = new double[output_size];
      for (int i = 0; i < output_size; i++)
        b2[i] = loaded_data[hidden_layer_size + output_size + 1][i];
      biases2.setBiases(b2);      // Setting biases2

      return true;
    }
    return false;
  }

  // For running through the training data to find the accuracy of the network's guesses
  public static void displayTrainingAccuracy(){
    // For user interface dynamics
    System.out.print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
    System.out.println("Running through training data...\n\n\n");

    // Variable initialization and reset
    int[] training_digit_counter = new int[output_size];
    int[] guessed_digit_counter = new int[output_size];
    double[] activation1 = new double[hidden_layer_size];
    double[] activation2 = new double[output_size];
    /// Intiating Reading of Data ///
    double[][] training_data = new double[training_data_size][input_size + 1];    // creating array to hold training data
                                                                                // The +1 is for the first index of the data being the digit name
    // Reading data into array for ease of access.
    training_data = readData("mnist_train.csv", training_data);

    // Normalizing Pixel Values
    for (int i = 0; i < training_data.length; i++)                               // Divides every data point by 255 save the first data point of each line
      for (int j = 1; j <input_size; j++)                                          // This is done to convert pixel value from 0-255 to 0.0-1.0
        training_data[i][j] = (double) training_data[i][j] / 255;
    
    for (int i = 0; i < training_data.length; i++){
      // Forward Pass //
      // Layer 1
      double[] tempA = new double[hidden_layer_size];
      for (int j = 0; j < hidden_layer_size; j++)                               // Dotting Weight1 matrix with input_data matrix
        for (int k = 0; k < input_size; k++)
          tempA[j] += weights1.getWeights()[j][k] * training_data[i][k + 1];
      
      for (int j = 0; j < hidden_layer_size; j++)                               // Running through sigmoid fn
        activation1[j] = sigmoid(tempA[j] + biases1.getBiases()[j]);

      // Layer 2
      double[] tempB = new double[output_size];
      for (int j = 0; j < output_size; j++)                                     // Dotting Weight2 matrix with activation1 matrix
        for (int k = 0; k < hidden_layer_size; k++)
          tempB[j] += weights2.getWeights()[j][k] * activation1[k];
        
      for (int j = 0; j < output_size; j++)                                     // Running through sigmoid
        activation2[j] = sigmoid(tempB[j] + biases2.getBiases()[j]);

      // Counts how many particle digit appear in the data
      training_digit_counter[(int) training_data[i][0]] += 1;
      // Counts how many particle digits the network guesses correctly
      if ((int) training_data[i][0] == getMaxValueIndex(activation2))
        guessed_digit_counter[getMaxValueIndex(activation2)] += 1;
    }
    print_data(training_digit_counter, guessed_digit_counter);                  // Prints accuracy data
  }

  // For running through testing data to find the accuracy of the network's guesses
  public static void displayTestingAccuracy(){
    System.out.print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
    System.out.println("Running through testing data...\n\n\n");

    // Variable initialization and reset
    int[] testing_digit_counter = new int[output_size];
    int[] guesstest_digit_counter = new int[output_size];
    double[] activation1 = new double[hidden_layer_size];
    double[] activation2 = new double[output_size];
    /// Intiating Reading of Data ///
    double[][] testing_data = new double[testing_data_size][input_size + 1];    // creating array to hold training data
                                                                                // The +1 is for the first index of the data being the digit name
    // Reading data into array for ease of access.
    testing_data = readData("mnist_test.csv", testing_data);

    // Normalizing Pixel Values
    for (int i = 0; i < testing_data.length; i++)                               // Divides every data point by 255 save the first data point of each line
      for (int j = 1; j <input_size; j++)                                         // This is done to convert pixel value from 0-255 to 0.0-1.0
      testing_data[i][j] = (double) testing_data[i][j] / 255;
    
    for (int i = 0; i < testing_data.length; i++){
      // Forward Pass //
      // Layer 1
      double[] tempA = new double[hidden_layer_size];                         
      for (int j = 0; j < hidden_layer_size; j++)                               // Dotting Weight1 matrix with input_data matrix
        for (int k = 0; k < input_size; k++)
          tempA[j] += weights1.getWeights()[j][k] * testing_data[i][k + 1];
      
      for (int j = 0; j < hidden_layer_size; j++)                               // Running through sigmoid fn
        activation1[j] = sigmoid(tempA[j] + biases1.getBiases()[j]);

      // Layer 2
      double[] tempB = new double[output_size];
      for (int j = 0; j < output_size; j++)                                     // Dotting Weight2 matrix with activation1 matrix
        for (int k = 0; k < hidden_layer_size; k++)
          tempB[j] += weights2.getWeights()[j][k] * activation1[k];
        
      for (int j = 0; j < output_size; j++)                                     // Running through sigmoid fn
        activation2[j] = sigmoid(tempB[j] + biases2.getBiases()[j]);

      // Counts how many particle digit appear in the data
      testing_digit_counter[(int) testing_data[i][0]] += 1;

      // Counts how many particle digits the network guesses correctly
      if ((int) testing_data[i][0] == getMaxValueIndex(activation2))
        guesstest_digit_counter[getMaxValueIndex(activation2)] += 1;
    }
    print_data(testing_digit_counter, guesstest_digit_counter);                   // Prints accuracy data
  }

  // For saving weights and biases of current network state
  public static void saveNetworkState(){
    // Asks user to name the file used to save the weights and biases of current network state
    System.out.print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
    System.out.print("Name the File: ");
    Scanner scanner = new Scanner(System.in);                       // Reads command line input
    String input = scanner.nextLine();
    File file = new File(input);                                    // Creates file

    try (FileWriter network_state_file = new FileWriter(file)){     // try and catch to write to file
      // Writing Weights1
      for (int i = 0; i < hidden_layer_size; i++){                  // Builds file structure that holds all weight and bias values
        StringBuilder line = new StringBuilder();                       // Detailed discription of structure in loadPreTrainedNetwork fn
        for (int j = 0; j < input_size; j++){ 
          line.append(weights1.getWeights()[i][j]);                 // Append data to each line bit by bit
          if (j != input_size - 1)
            line.append(',');
        }
        line.append("\n");                                      // \n to force new line in file
        network_state_file.write(line.toString());
      }

      // Writing Weights2
      for (int i = 0; i < output_size; i++){
        StringBuilder line = new StringBuilder();                   // Using stringbuilder library to add data to lines of file
        for (int j = 0; j < hidden_layer_size; j++){
          line.append(weights2.getWeights()[i][j]);
          if (j != hidden_layer_size - 1)
            line.append(',');
        }
        line.append("\n");
        network_state_file.write(line.toString());
      }

      // Writing Biases1
      StringBuilder line = new StringBuilder();
      for (int i = 0; i < hidden_layer_size; i++){
        line.append(biases1.getBiases()[i]);
        if (i != hidden_layer_size - 1)
          line.append(',');
      }
      line.append("\n");
      network_state_file.write(line.toString());

      // Writing Biases2
      line = new StringBuilder();
      for (int i = 0; i < output_size; i++){
        line.append(biases2.getBiases()[i]);
        if (i != output_size - 1)
          line.append(',');
      }
      line.append("\n");
      network_state_file.write(line.toString());
    
      network_state_file.close();                                       // Closes and saves file

      System.out.println("Network state saved under: " + input);        // Prints file name that weights and biases are saved under
      System.out.println("\n\n\n");
    } catch (Exception e) {
      System.out.println(e.getMessage());
    }
  }

  // For computing sigmiod function
  public static double sigmoid(double z){
    return 1 / ( 1 + Math.pow(2.71828182845, -z));    // Converts values to smooth values between 0 and 1
  }

  // For finding the index of the max value of an array
  public static int getMaxValueIndex(double[] act){
    int max = 0;
    for (int i = 0; i < act.length; i++){
      if (act[i] > act[max]) max = i;     // Compares values until it finds largest value.
    }
    return max;
  }

  // For shuffling data
  public static Integer[] shuffleData(Integer[] training_data_index){
    for (int i = 0; i < training_data_index.length; i++)                            // Creates array[0,1,2,...,60000]
      training_data_index[i] = i;
    List<Integer> training_data_index_list = Arrays.asList(training_data_index);    // Converts Array into list
    Collections.shuffle(training_data_index_list);                                  // Shuffles list
    return training_data_index_list.toArray(training_data_index);                   // Converts back into array and returns
  }

  // For creating mini-batch array
  public static int[][] makeMiniBatches(int[][] mini_batches, Integer[] training_data_index){
    int counter = 0;                                                                // Counts through training_data_index array
    for (int i = 0; i < (training_data_index.length / mini_batch_size); i++){       // Fills 6000 mini-batches with 10 data samples each (random)
      for (int j = 0; j < mini_batch_size; j++){
        mini_batches[i][j] = training_data_index[counter];
        counter++;
      }
    }
    return mini_batches;  // Return 6000 x 10 array
  }

  // For reading data (training and testing)
  public static double[][] readData(String filename, double[][] data){
    try{                                                                // Need try and catch for Scanner library
      Scanner myFileReader = new Scanner(new File(filename));           // Loads file selected
      // Parse through data
      int j = 0;
      while (myFileReader.hasNextLine()){                               // This while loop traverses line by line until end of data
        String line = myFileReader.nextLine();                          // Saves current line as var
        String[] temp_str = line.split(",");                     // Splits line into string array using ","
        for (int i = 0; i < temp_str.length; i++){                      // j corresponds with the line awhile i with data point
          data[j][i] = Double.parseDouble(temp_str[i]);
        }
        j++;
      }
    } catch (FileNotFoundException e){                                  // I honestly still dont get why this is needed
      System.out.println(e.getMessage());                               // But it's required so I added it
      data[0][0] = -1;
    }
    return data;
  }

  // For printing accuracy data to console
  public static void print_data(int[] a, int[] g){
    float sum_g = g[0] + g[1] + g[2] + g[3] + g[4] + g[5] + g[6] + g[7] + g[8] + g[9];        // Summation of total correct guesses per digit
    float sum_a = a[0] + a[1] + a[2] + a[3] + a[4] + a[5] + a[6] + a[7] + a[8] + a[9];        // Summation of total times each digit apeared
    float acc = (sum_g / sum_a) * 100;                                                        // Percent accuracy of network's guesses

    // Prints accuracy values for every digit
    System.out.printf("\n\t0 = %d/%d\t1 = %d/%d\t2 = %d/%d", g[0], a[0], g[1], a[1], g[2], a[2]);
    System.out.printf("\t3 = %d/%d\t4 = %d/%d\t5 = %d/%d\n", g[3], a[3], g[4], a[4], g[5], a[5]);
    System.out.printf("\t6 = %d/%d\t7 = %d/%d\t8 = %d/%d", g[6], a[6], g[7], a[7], g[8], a[8]);
    System.out.printf("\t9 = %d/%d\tAccuracy = %d/%d = %f", g[9], a[9], (int) sum_g, (int) sum_a, acc);
    System.out.print("%\n");
    System.out.println();
  }

}
