package digit_recognizer;
import java.util.Random;
import java.util.Scanner;
import java.util.Arrays;

public class three_layer_network {
	//Initialize arrays and matrices
	
	//neural network 3 layer model
	private static int[] input_layer = new int[784]; //for all the inputs( 784 pixels)
	private static int[] hidden_layer = new int[100]; //neurons for hidden layer, out of the arse amount
	private static int[] output_layer = new int[10]; // output layer, 10, 1 for every digit from 0 to 9.
	
	//sizes vector, just in case
	private static int[] sizes = {784,100,10}; //input,hidden,output sizes
	
	//declare the weight matrices
	private static double[][] weights1 = new double[100][784]; //weights from input layer to hidden layer
	private static double[][] weights2 = new double[10][100]; // weights from hidden layer to output layer
	
	//declare bias arrays
	private static double[] bias1 = new double[100]; //biases for the hidden layer
	private static double[] bias2 = new double[10]; //biases for the output layer
	
	//declare the z value arrays (total inputs for each node)
	private static double[] zvalue1 = new double[100]; //z values for hidden layer
	private static double[] zvalue2 = new double[10]; //z values for output layer
	
	//declare activation arrays
	private static double[] avalue0 = new double[786]; // a values for input layer
	private static double[] avalue1 = new double[100]; // a values for hidden layer
	private static double[] avalue2 = new double[10]; // a values for output layer
	
	
	
	public static double sigmoid(double z) {
		//take in the zvalue and calculate the activation (a value)
		double a = 1/(1 + Math.exp(-z));
		return a;
	}
	
	public static void menu() {
		// create scanner to take input from cmd
	    Scanner scanner = new Scanner(System.in);
	    
	    //Print introduction
	    System.out.println("3 layer neural network by Dylan Campbell");
	    System.out.println("Press [1] to create a new network");
	    int input = scanner.nextInt();
	    if(input == 1) {
	    	new_network();
	    	return;
	    }
	    else {
	    	System.out.println("FAIL");
	    }
	}
	
	private static void new_network() {
		//create a new neural network, we'll give random values to weights and biases
		System.out.println("hello");
		Random rand = new Random();
		//set random weight for the weight matrices
		
		for(int i = 0; i < weights1.length; i++) { //setting random for weights from input to hidden layer
			for(int j = 0; j < weights1[0].length; j++) {
				weights1[i][j] = rand.nextDouble() * 2 - 1;
				System.out.println("weight1: "+ i  + ", "+ j + ": " + weights1[i][j]);
			}
		}
		
		for(int i = 0; i < weights2.length; i++) { //setting random for weights from hidden to output layer
			for(int j = 0; j < weights2[0].length; j++) {
				weights2[i][j] = rand.nextDouble() * 2 - 1;
				System.out.println("weight2: "+ i + ", "+  j + ": " + weights2[i][j]);
			}
		}
		
		for(int i = 0; i < bias1.length; i++) { //bias for hidden layer
			bias1[i] = rand.nextDouble() * 2 - 1;
		}
		
		for(int i = 0; i < bias2.length; i++) { //bias for output layer
			bias2[i] = rand.nextDouble() * 2 - 1;
		}
		
		//temp fill inputs full of random ints from 0 to 255
		//TODO: will fill with input values from file
		for(int i = 0; i < input_layer.length; i++) {
			input_layer[i] = rand.nextInt(255);
		}
	}
		
	public static double[] feedforward() { //use the current weights and biases and feed them through the network
		double sum = 0;
		for(int j = 0; j < zvalue1.length; j++){ // using zvalue1's length to iterate through every jth row of the weight matrices, since they are equivalent in length
			for(int i = 0; i < weights1[0].length; i++) { // for every ith item in the jth row of the weights1 matrices
				sum = weights1[j][i] * input_layer[i]; // summate all the the i'th items in weights1 times the i'th input in the input layer
			}
			zvalue1[j] = sum - bias1[j]; //take that sum and subtract the bias for the current j index for the zvalue
			avalue1[j] = sigmoid(zvalue1[j]); //run the zvalue through the sigmoid function to get the jth activation value
			//I took Discrete Math 1 and 2 and still can't explain math well.. hah..
			
			System.out.println("zvalue1("+j+")=" +zvalue1[j]);
			System.out.println("avalue1("+j+")=" +avalue1[j]);
		
		}
		//same as before but for weights from the hidden layer to the output layer
		for(int j = 0; j < zvalue2.length; j++){ 
			for(int i = 0; i < weights2[0].length; i++) { 
				sum = weights2[j][i] * hidden_layer[i]; 
			}
			zvalue2[j] = sum - bias2[j]; 
			avalue2[j] = sigmoid(zvalue2[j]); 
			
			System.out.println("zvalue2("+j+")=" +zvalue2[j]);
			System.out.println("avalue2("+j+")=" +avalue2[j]);
		
		}
		
		return avalue2; //the final activation vector to be compared to the expected results
	}
	
	public void SGD() {
		//TODO: Stochastic Gradient Descent Algorithm
	}
		
	

	public static void main(String[] args) {
		//new_network();
		menu();
		feedforward();
		
		System.out.println("WE back at main");
	}

	

}
