package digit_recognizer;
import java.util.Random;
import java.util.Scanner;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
/* 	Hand Written Digit Recognizer
	By: Dylan Campbell
	CWID: 10227735
	
	ASSIGNMENT 2
	
	This program emulates a 3 layer neural network that takes input from a csv for the MNIST
	handwritten digit dataset and uses it to learn and be able to accurately guess handwritten
	digits.
*/
public class three_layer_network {
	/*Initialize arrays and matrices*/
	/*----------------------------------------------------------*/
	
	//neural network 3 layer model
	private static double[] input_layer = new double[785];//for all the inputs( 784 pixels)
	private static double[] hidden_layer = new double[100]; //neurons for hidden layer, out of the arse amount
	private static double[] output_layer = new double[10]; // output layer, 10, 1 for every digit from 0 to 9.
	
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
	private static double[] avalue0 = new double[784]; // a values for input layer
	private static double[] avalue1 = new double[100]; // a values for hidden layer
	private static double[] avalue2 = new double[10]; // a values for output layer
	
	//declare training and testing matrices
	private static double[][] initial_set = new double[785][60000]; //initial full reading from csv
	private static double[][] training_set = new double[785][50000]; //784 pixels per 50,000 images
	private static double[][] testing_set = new double[785][10000]; //784 pixels per 10,000 images
	private static double[][] minibatch = new double[785][10]; //784 pixels for 10 random images
	
	//declare arrays necessary for backpropagation
	private static double[] error2 = new double[10]; //error for output layer
	private static double[] bg2 = new double[10]; //bias gradients for output layer
	private static double[][] wg2 = new double[10][100]; //weight gradients for output layer
	private static double[] error1 = new double[100]; 
	private static double[] bg1 = new double[100];
	private static double[][] wg1 = new double[100][784];
	
	//declare containers so hold the sum of the gradients to update the weights and biases after a minibatch
	private static double[][] sumofwg1 = new double[100][784]; //sum of weight gradients for hidden layer
	private static double[][] sumofwg2 = new double[10][100];  //for output layer
	private static double[] sumofbg1 = new double[100]; //sum of bias gradients for hidden layer
	private static double[] sumofbg2 = new double[10]; //for output layer
	
	//declare variables
	private static double lr = 3; //learning rate for well.. rate of learning
	private static int epochs = 30;
	private static int minibatches = 5000;
	private static int hits = 0; //amount guessed correctly
	private static double total = 1; //total attempts
	private static double epoch_total = 1;
	private static int epoch_hits = 0;
	private static boolean trained = false;
	private static int[] acc_per_digit = new int[10];
	private static int[] digit_attempts = new int[10];
	
	
	
	/* FUNCTIONS */
	/*----------------------------------------------------------*/
	public static double sigmoid(double z) {
		//take in the zvalue and calculate the activation (a value)
		double a = 1/(1 + Math.exp(-z));
		return a;
	}
	
	public static void SGD() {
		Random rand = new Random();
		
		for(int e = 0; e < epochs; e++) { //amount of epochs to run
			shuffle(training_set);
			
			for(int i = 0; i < 10; i++) { //resets accuracy values
				acc_per_digit[i] = 0;
				digit_attempts[i] = 0;
			}
			//Collections.shuffle(Arrays.asList(initial_set[0]));
			
		//Stochastic Gradient Descent Algorithm
		//Prolly add this whole section in a for loop for the epochs
		for(int m = 0; m <= minibatches; m++) {
			epoch_hits = 0;
			epoch_total = 1;
			
			//refresh all sumof gradient containers
			refresh();

			//randomize order of items in training set
			
			
			//divide training set into equal sized mini-batches(10 items in each)
			for(int i = 0; i < 10; i++) {
				for(int j = 0; j < training_set.length; j++) {
					minibatch[j][i] = (training_set[j][i]);
				}
			}
		
			//Use backpropagation to compute the weight gradients and bias gradients over the training inputs in the first[next] minibatch
			for(int i = 0; i < minibatch[0].length; i++) {
				for(int j = 0; j < minibatch.length; j++) {
					input_layer[j] = minibatch[j][i]; //place inputs from the given minibatch into the input layer
					//System.out.println(input_layer[0]);
				}
				total += 1;//for total runs made
				backprop(); //run the inputs of the current minibatch into the backpropogation function
				
				accuracy();//check accuracy
				update();//after completing minibatch, update weights and biases
				
			}
			//status_print();
				
		}
		status_print();//once after every epoch
		}
		
	}
	
	public static void shuffle(double[][] array) {

        for (int row = 0; row < array[0].length; row++) {
            int rand = (int) (Math.random() * array[0].length);

            // swap row
            for (int col = 0; col < array.length; col++) {
                double temp = array[col][row];
                array[col][row] = array[col][rand];
                array[col][rand] = temp;
            }
        }
        

    }
	
	private static void runthrough(double[][] a) { //run the data through the model fully once
		refresh(); //clean out gradient bins
		
		for(int i = 0; i < 10; i++) {
			acc_per_digit[i] = 0;
			digit_attempts[i] = 0;
		}
		
		for(int i = 0; i < a[0].length; i++) {
			for(int j = 0; j < a.length; j++) {
				input_layer[j] = (a[j][i]); //place inputs from the given data into the input layer
			}
			
			backprop(); //run the inputs into the backpropogation function
			
			accuracy();//check accuracy
			status_print();
		}
		//status_print();
			
	}
	private static void status_print() {
		// prints specified post epoch stats
		double correct = 0;
		double attempts = 0;
		
		for(int i = 0 ; i < 10; i++) {
			correct += acc_per_digit[i];
			attempts += digit_attempts[i];
			System.out.print(i + " = " + acc_per_digit[i] + "/" + digit_attempts[i] + "  ");
			if(i == 5) {
			System.out.print("\n");
			}
		}
		
		System.out.print("Accuracy = " + correct + "/" + attempts + " = " + (double)((correct/attempts)*100)+ "\n\n");
	}
		
	private static void accuracy() {
		//Check the accuracy of the model, post minibatch
		
		//compare a value's to expected output
		double value = 0;
		int max = 0;
		for(int i = 0; i < avalue2.length; i++) {
			//System.out.println("avalue2: "+ i+ ": "+ avalue2[i]);
			if((avalue2[i]) > value) {
				max = i;
				value = avalue2[i];
			}
		}
		System.out.println("eo:" + input_layer[0] + " | guessed:" + max);
		if(max == (int)(input_layer[0])) {
			hits += 1; //increase when the system guesses correctly
			epoch_hits += 1;
			acc_per_digit[max] += 1;
			digit_attempts[max] += 1;
		}
		else {
			digit_attempts[((int)input_layer[0])] += 1;
		}
		
		
		
		//ouble accuracy =(hits/total)*100;
		//double epochacc =(epoch_hits/epoch_total)*100;
		//System.out.println("EO: " + (input_layer[0]*255)+ " Guessed: " + max);
		//System.out.println("hits: "+ hits + "/" + total + " = " + accuracy);
		//System.out.println("epoch_hits: "+ epoch_hits + "/" + epoch_total + " = " + epochacc);
	}

	private static void refresh() {
		// Refreshes all sumof gradient containers by initializing them all to 0
		for(int i = 0; i < sumofbg1.length; i++) {
			sumofbg1[i] = 0;
		}
		for(int i = 0; i < sumofbg2.length; i++) {
			sumofbg2[i] = 0;
		}
		for(int i = 0; i < sumofwg1.length; i++) {
			for(int j = 0; j < sumofwg1[0].length; j++) {
				sumofwg1[i][j] = 0;
			}
		}
		for(int i = 0; i < sumofwg2.length; i++) {
			for(int j = 0; j < sumofwg2[0].length; j++) {
				sumofwg2[i][j] = 0;
			}
		}
		
		
	}

	private static void update() {
		// update weights and biases
		
		for(int i = 0; i < bias1.length; i++) { //update biases for hidden layer
			bias1[i] = bias1[i] - (lr/10) * sumofbg1[i];
		}
		
		for(int i = 0; i < weights1.length; i++) { //update weights for hidden layer
			for(int j = 0; j < weights1[0].length; j++) {
				weights1[i][j] = weights1[i][j] - (lr/10) * sumofwg1[i][j];
			}
		}
		
		for(int i = 0; i < bias2.length; i++) { //update biases for output layer
			bias2[i] = bias2[i] - (lr/10) * sumofbg2[i];
		}
		
		for(int i = 0; i < weights2.length; i++) { //update weights for output layer
			for(int j = 0; j < weights2[0].length; j++) {
				weights2[i][j] = weights2[i][j] - (lr/10) * sumofwg2[i][j];
			}
		}
	}

	public static void backprop() {
		double sum = 0;
		//use current weights and biases, compute activations of all neurons at all layers of the network.
		feedforward();
		epoch_total += 1;
		//Compute the gradient of the error at the final level of the network and then move "backwards" through the network computing the error
		//at each level, one level at a time. backwards pass.
		
		double[] eo = new double[10];//set the expected output to an array
		eo = expected_o(input_layer[0]);
		
		for(int i=0; i < error2.length; i++) { // computer error vector and gradients for layer2(output layer)
			error2[i] = (avalue2[i] - eo[i]) * (avalue2[i] * (1.0 - avalue2[i]));
			
			
			bg2[i] = error2[i]; //bias gradient (equivalent to error)
			
			for(int j=0; j < wg2[0].length; j++) { //weight gradients
				wg2[i][j] = avalue1[j] * bg2[i];
				
				sumofwg2[i][j] += wg2[i][j];//add wg2 to the sum container for post batch updates
			}
			
			
			sumofbg2[i] += bg2[i]; //add bg2 to sum container for post batch updates
			
		}
		
		for(int i = 0; i < error1.length; i++) { //compute errors, bias and weight gradients for layer1(hidden layer)\
			sum = 0;
			for(int k = 0; k < weights2.length;k++) { //summate weights and errors
				sum += weights2[k][i] * error2[k];
			}
			
			error1[i] = sum * (avalue1[i]* (1- avalue1[i])); // compute errors for hidden layer
			
			bg1[i] = error1[i]; //bias gradient
			
			for(int j = 0; j < wg1[0].length; j++) { //weight gradients of hidden layer
				wg1[i][j] = input_layer[j+1] * bg1[i];
				
				sumofwg1[i][j] += wg1[i][j];
			}
			
			sumofbg1[i] += bg1[i];
		}
		
		
	}
	
	private static double[] expected_o(double d) {
		//translates the single digit output to an array of 0s and a 1
		double[] eo = new double[10];//set the expected output to an array
		
		switch((int)d) {
		case 0: eo[0] = 1; eo[1] = 0; eo[2] = 0; eo[3] = 0; eo[4] = 0; eo[5] = 0;
				eo[6] = 0; eo[7] = 0; eo[8] = 0; eo[9] = 0;
				break;
		case 1: eo[0] = 0; eo[1] = 1; eo[2] = 0; eo[3] = 0; eo[4] = 0; eo[5] = 0;
				eo[6] = 0; eo[7] = 0; eo[8] = 0; eo[9] = 0;
				break;
		case 2: eo[0] = 0; eo[1] = 0; eo[2] = 1; eo[3] = 0; eo[4] = 0; eo[5] = 0;
				eo[6] = 0; eo[7] = 0; eo[8] = 0; eo[9] = 0;
				break;
		case 3: eo[0] = 0; eo[1] = 0; eo[2] = 0; eo[3] = 1; eo[4] = 0; eo[5] = 0;
				eo[6] = 0; eo[7] = 0; eo[8] = 0; eo[9] = 0;
				break;
		case 4: eo[0] = 0; eo[1] = 0; eo[2] = 0; eo[3] = 0; eo[4] = 1; eo[5] = 0;
				eo[6] = 0; eo[7] = 0; eo[8] = 0; eo[9] = 0;
				break;
		case 5: eo[0] = 0; eo[1] = 0; eo[2] = 0; eo[3] = 0; eo[4] = 0; eo[5] = 1;
				eo[6] = 0; eo[7] = 0; eo[8] = 0; eo[9] = 0;
				break;
		case 6: eo[0] = 0; eo[1] = 0; eo[2] = 0; eo[3] = 0; eo[4] = 0; eo[5] = 0;
				eo[6] = 1; eo[7] = 0; eo[8] = 0; eo[9] = 0;
				break;
		case 7: eo[0] = 0; eo[1] = 0; eo[2] = 0; eo[3] = 0; eo[4] = 0; eo[5] = 0;
				eo[6] = 0; eo[7] = 1; eo[8] = 0; eo[9] = 0;
				break;
		case 8: eo[0] = 1; eo[1] = 0; eo[2] = 0; eo[3] = 0; eo[4] = 0; eo[5] = 0;
				eo[6] = 0; eo[7] = 0; eo[8] = 1; eo[9] = 0;
				break;
		case 9: eo[0] = 0; eo[1] = 0; eo[2] = 0; eo[3] = 0; eo[4] = 0; eo[5] = 0;
				eo[6] = 0; eo[7] = 0; eo[8] = 0; eo[9] = 1;
				break;
			
			
		}
		return eo;
	}

	public static void feedforward() { //use the current weights and biases and feed them through the network
		double sum = 0;
		for(int j = 0; j < zvalue1.length; j++){ // using zvalue1's length to iterate through every jth row of the weight matrices, since they are equivalent in length
			for(int i = 0; i < weights1[0].length; i++) { // for every ith item in the jth row of the weights1 matrices
				sum += weights1[j][i] * input_layer[i+1]; // summate all the the i'th items in weights1 times the i'th input in the input layer
			}
			zvalue1[j] = sum + bias1[j]; //take that sum and subtract the bias for the current j index for the zvalue
			avalue1[j] = sigmoid(zvalue1[j]); //run the zvalue through the sigmoid function to get the jth activation value
			//I took Discrete Math 1 and 2 and still can't explain math well.. hah..
			
			//System.out.println("zvalue1("+j+")=" +zvalue1[j]);
			//System.out.println("avalue1("+j+")=" +avalue1[j]);
		
		}
		sum = 0;
		//same as before but for weights from the hidden layer to the output layer
		for(int j = 0; j < zvalue2.length; j++){ 
			for(int i = 0; i < weights2[0].length; i++) { 
				sum += weights2[j][i] * avalue1[i]; 
			}
			zvalue2[j] = sum + bias2[j]; 
			avalue2[j] = sigmoid(zvalue2[j]); 
			
			//System.out.println("zvalue2("+j+")=" +zvalue2[j]);
			//System.out.println("avalue2("+j+")=" +avalue2[j]);
		
		}
		
		
		//return avalue2; //the final activation vector to be compared to the expected results
	}
	
	public static void menu() throws IOException {
		// create scanner to take input from cmd
	    Scanner scanner = new Scanner(System.in);
	    
	    //Print introduction
	    System.out.println("3 layer neural network by Dylan Campbell");
	    System.out.println("[1] Create a new network");
	    System.out.println("[2] Load a pretrained network");
	    if(trained) {
	    	System.out.println("[3] Display network accuracy on TRAINING data");
	    	System.out.println("[4] Display network accuracy on TESTING data");
	    	System.out.println("[5] current network state to file");
	    	System.out.println("[0] Exit");
	    }
	    int input = scanner.nextInt();
	    if(input == 1) {
	    	System.out.println("Training... Please Wait...");
	    	String file = "/Users/Red Death/Downloads/mnist_train.csv";
	    	//String file = System.getProperty("user.dir") + "/mnist_train.csv";
	    	data_from_csv(file);
	    	new_network();
	    	SGD();
	    	trained = true;
	    	return;
	    }
	    else if(input == 2) {
	    	String file = "/Users/Red Death/Downloads/mnist_train.csv";
	    	data_from_csv(file);
	    	load("saved_state.csv");
	    	trained = true;
	    }
	    else if(input == 3) {
	    	runthrough(training_set);
	    }
	    else if(input == 4) {
	    	runthrough(testing_set);
	    }
	    else if(input == 5) {
	    	save();
	    }
	    else if(input == 0) {
	    	System.exit(0);
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
		
		for(int i = 0; i < weights1.length; i++) { //setting random for weights from input to hidden layer between -1 and 1
			for(int j = 0; j < weights1[0].length; j++) {
				weights1[i][j] = rand.nextDouble() * 2.0 - 1.0;
				//System.out.println("weight1: "+ i  + ", "+ j + ": " + weights1[i][j]);
			}
		}
		
		for(int i = 0; i < weights2.length; i++) { //setting random for weights from hidden to output layer between -1 and 1
			for(int j = 0; j < weights2[0].length; j++) {
				weights2[i][j] = rand.nextDouble() * 2.0 - 1.0;
				//System.out.println("weight2: "+ i + ", "+  j + ": " + weights2[i][j]);
			}
		}
		
		for(int i = 0; i < bias1.length; i++) { //bias for hidden layer between -1 and 1
			bias1[i] = rand.nextDouble() * 2.0 - 1.0;
		}
		
		for(int i = 0; i < bias2.length; i++) { //bias for output layer between -1 and 1
			bias2[i] = rand.nextDouble() * 2.0 - 1.0;
		}
		

		//TODO: will fill with input values from test cases
		int x = rand.nextInt(training_set[0].length);
		for(int i = 0; i < input_layer.length; i++) {
			input_layer[i] = training_set[i][x];// input random test case
		}
	}
		
	public static void data_from_csv(String file) {
	//FUNCTION CREATED BY mkyong @ mkyong.com, with a twist from me to get training data set.
        String csvFile = file;
        BufferedReader br = null;
        String line = "";
        String[] inputs = new String[60000];
        int k = 0; //Will be used to iterate through the initial full input array
        try {

            br = new BufferedReader(new FileReader(csvFile));
            while ((line = br.readLine()) != null) { //will write on the inputs array until it reaches 784 and will overwrite with the next 784, etc.

                inputs = line.split(","); //split the csv using the commas, this will 
                
               
                for(int i = 0; i < inputs.length; i++) { //before the 784 slots get overwritten, capture them in the [0-784][k] spots of the testing_set matrices
                	
                	initial_set[i][k] = Integer.parseInt(inputs[i]);
                	
                   	//initial_set[i][k] /= 255; //normalize data, avoiding the first bit that gives us an expected output
                	
                	
                	//System.out.println(i+ "," + k + ": " + initial_set[i][k] + " = " + inputs[i]);
                	
                	                	
                	}
                
                k++;//after the 784 are captured, we increment k to grab the next 784.
        		}
            for(int i = 0; i < initial_set[0].length; i++) {
            	for(int j = 0; j < initial_set.length; j++) {
            		if(i <= 49999) {
            			training_set[j][i] = initial_set[j][i];
            		}
            		else {
            			testing_set[j][i-50000] = initial_set[j][i];
            		}
            		
            	}
            }
            

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
	}
	
	public static void save() throws IOException {
		File file = new File("saved_state.csv");
		BufferedWriter out = new BufferedWriter(new FileWriter(file));
		for(int i = 0; i < weights1.length; i++) {
			for(int j = 0; j < weights1[0].length; j++) {
			try {
		         // APPEND MODE SET HERE
		         out.write(Double.toString(weights1[i][j]));
		         out.write(",");
		         out.flush();
		      	} catch (IOException ioe) {
		      		ioe.printStackTrace();
		      	} finally {
		      		;
		      	} // end try/catch/finally
			}
		}
		for(int i = 0; i < weights2.length; i++) {
			for(int j = 0; j < weights2[0].length; j++) {
			try {
		         out.write(Double.toString(weights2[i][j]));
		         out.write(",");
		         out.flush();
		      	} catch (IOException ioe) {
		      		ioe.printStackTrace();
		      	} finally {                       
		      		;
		      	} // end try/catch/finally
			}
		}
		for(int i = 0; i < bias1.length; i++) {
			try {
		         out.write(Double.toString(bias1[i]));
		         out.write(",");
		         out.flush();
		      	} catch (IOException ioe) {
		      		ioe.printStackTrace();
		      	} finally {                       
		      		;
		      	} // end try/catch/finally
		}
		for(int i = 0; i < bias2.length; i++) {
			try {
		         out.write(Double.toString(bias2[i]));
		         out.write(",");
		         out.flush();
		      	} catch (IOException ioe) {
		      		ioe.printStackTrace();
		      	} finally {                       
		      		;
		      	} // end try/catch/finally
		}
		out.close();
		
	}
	
	public static void load(String file) { //load weights and biases from a saved file
		String stateFile = file;
        BufferedReader br = null;
        String line = "";
        String[] inputs = new String[79510];
        int inputindex = 0;
        
        try {

            br = new BufferedReader(new FileReader(stateFile));
            while ((line = br.readLine()) != null) { 

                inputs = line.split(","); //split the file using the commas
                
                
            }

            for(int j = 0; j < weights1.length; j++) {
            	for(int k = 0; k < weights1[0].length; k++) {
            		weights1[j][k] = Double.parseDouble(inputs[inputindex]);
            		inputindex += 1;
            		System.out.println(weights1[j][k]);
            	}
            }
            for(int j = 0; j < weights2.length; j++) {
            	for(int k = 0; k < weights2[0].length; k++) {
            		weights2[j][k] = Double.parseDouble(inputs[inputindex]);
            		inputindex += 1;
            	}
            }
            for(int j = 0; j < bias1.length; j++) {
            	bias1[j] = Double.parseDouble(inputs[inputindex]);
            	inputindex += 1;
            }
            for(int j = 0; j < bias2.length; j++) {
            	bias2[j] = Double.parseDouble(inputs[inputindex]);
            	inputindex += 1;
            }
                
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
		
	}
            
	public static void main(String[] args) throws IOException {
		while(true) {
		menu();
		}
	}

	

}