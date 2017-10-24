package excel_replica;

public class Excel_replica {
	
	private static double[][] w1 = new double[3][4]; //weights from input to hidden layer
	private static double[][] w2 = new double[2][3]; //weights from hidden to output
	
	private static double[] a1 = new double[4]; //activation layer 1
	private static double[] a2 = new double[3]; //activation layer 2
	
	private static double[] b1 = new double[3]; //biases for layer 1
	private static double[] b2 = new double[3]; //biases for layer 2
	
	private static double[] z1 = new double[3]; //z value for layer 1
	private static double[] z2 = new double[2]; //z value for layer 2
	
	private static double[] error1 = new double[3]; //error values for layer 1
	private static double[] error2 = new double[2]; //error values for layer 2
	
	private static double[] gb1 = new double[3]; //bias gradients for layer 1
	private static double[] gb2 = new double[2]; //bias gradients for layer 2
	private static double[] sumofgb1 = new double[3]; //sum of bias gradients for layer 1
	private static double[] sumofgb2 = new double[2]; //sum of bias gradients for layer 2
	
	private static double[][] wg1 = new double[3][4]; //weight gradients for layer 1
	private static double[][] wg2 = new double[2][3]; //weight gradients for layer 2
	private static double[][] sumofwg1 = new double[3][4]; //sum of weight gradients for layer 1
	private static double[][] sumofwg2 = new double[2][3]; //sum of weight gradients for layer 2
 	
	private static double[] input = new double[4]; //input layer
	private static double[] eo = new double[2]; //expected output for input layer
	
	private static double lr = 10; //learning rate
	private static int epochs = 6; //epochs
	
	
	
	public static void main(String[] args) {
		init(); //initialize weights and biases
		
		for(int e = 1; e <= epochs; e++) { //run amount of epochs
			System.out.println("\nEpoch #" + e + ":\n--------");
			//will be running SGD twice, one for each minibatch
			System.out.println("\nMiniBatch #1:\n--------");
			SGD(1); //Stochastic gradient descent
			update();
			System.out.println("\nMiniBatch #2:\n--------");
			SGD(2);
			update();
		}
	}
	
	

	public static void init() {
		//initialize weights, hardcoded like the spreadsheet
		//init weights layer 1
		w1[0][0] = -0.21;
		w1[0][1] = 0.72;
		w1[0][2] = -0.25;
		w1[0][3] = 1;
		w1[1][0] = -0.94;
		w1[1][1] = -0.41;
		w1[1][2] = -0.47;
		w1[1][3] = 0.63;
		w1[2][0] = 0.15;
		w1[2][1] = 0.55;
		w1[2][2] = -0.49;
		w1[2][3] = -0.75;
		//init weights layer 2
		w2[0][0] = 0.76;
		w2[0][1] = 0.48;
		w2[0][2] = -0.73;
		w2[1][0] = 0.34;
		w2[1][1] = 0.89;
		w2[1][2] = -0.23;
		
		//initalize bias
		//init bias layer 1
		b1[0] = 0.1;
		b1[1] = -0.36;
		b1[2] = -0.31;
		//init bias layer 2
		b2[0] = 0.16;
		b2[1] = -0.46;
		
		
	}
	public static void SGD(int mini) {
		if(mini == 1) { //for minibatch set 1
			//init input and expected out
			input[0] = 0;
			input[1] = 1;
			input[2] = 0;
			input[3] = 1;
				
			eo[0] = 0;
			eo[1] = 1;
			feedforward();
			backprop();
		
			//init input and expected out for 2nd run of minibatch1
			input[0] = 1;
			input[1] = 0;
			input[2] = 1;
			input[3] = 0;
						
			eo[0] = 1;
			eo[1] = 0;
			feedforward();
			backprop();
		}
		
		else if(mini == 2) {//for minibatch set 2
			//init input and expected out
			input[0] = 0;
			input[1] = 0;
			input[2] = 1;
			input[3] = 1;
					
			eo[0] = 0;
			eo[1] = 1;
			feedforward();
			backprop();
			
			//init input and expected out for 2nd run of minibatch1
			input[0] = 1;
			input[1] = 1;
			input[2] = 0;
			input[3] = 0;
							
			eo[0] = 1;
			eo[1] = 0;
			feedforward();
			backprop();
		}
	}
	
	public static void feedforward() {
		//calculate z value and a value1
		for(int i = 0; i < 3; i++) {
			double sum = 0;
			for(int j = 0; j < 4; j++) {
				sum += w1[i][j] * input[j];
			}
			z1[i] = sum + b1[i];
			System.out.println("z1["+i+"]:"+z1[i]);
			a1[i] = 1 /(1 + Math.pow(2.71828,-z1[i]));
			System.out.println("a1["+i+"]:"+a1[i]);
		}
		
		for(int i = 0; i < 2; i++) {
			double sum = 0;
			for(int j = 0; j < 3; j++) {
				sum += w2[i][j] * a1[j];
			}
			z2[i] = sum + b2[i];
			System.out.println("z2["+i+"]:"+z2[i]);
			a2[i] = 1/(1 + Math.exp(-z2[i]));
			System.out.println("a2["+i+"]:"+a2[i]);
				
			}
		}
	
	public static void backprop() {
		double sum = 0;
		//error layer 2
		for(int i = 0; i < 2; i++) {
			error2[i] = (a2[i] - eo[i]) * a2[i] * (1-a2[i]);
			System.out.println("error2["+i+"]:"+error2[i]);
		}
		
		//bias gradient layer 2
		for(int i = 0; i < 2; i++) {
			gb2[i] = error2[i];
			sumofgb2[i] += gb2[i]; //add to sumofgb2
			System.out.println("gb2["+i+"]:"+gb2[i]);
		}
		
		//weight gradient layer 2
		for(int i = 0; i < 2; i++) {
			for(int j = 0; j < 3; j++) {
				wg2[i][j] = a1[j] * gb2[i];
				sumofwg2[i][j] += wg2[i][j]; //add to sumofwg2
				System.out.println("wg2["+i+"]"+"["+j+"]:"+wg2[i][j]);
			}
		}
		
		//error layer 1
		for(int i = 0; i < 3; i++) {
			sum = 0;
			for(int k = 0; k < 2;k++) { //summate weights and errors
				sum += w2[k][i] * error2[k];
			}
			error1[i] = sum * a1[i] * (1 - a1[i]);
			
			//gradient bias layer 1
			gb1[i] = error1[i];
			sumofgb1[i] += gb1[i]; //add to sumofgb1
			System.out.println("gb1["+i+"]:"+gb1[i]);
		}
		
		//weight gradients layer 1
		for(int i = 0; i < 3; i++) {
			for(int j = 0; j < 4; j++) {
				wg1[i][j] = input[j] * gb1[i];
				sumofwg1[i][j] += wg1[i][j];
				System.out.println("wg1["+i+"]"+"["+j+"]:"+wg1[i][j]);
			}
		}
		
	}
	
	private static void update() {//update weights and biases
		
		for(int i = 0; i < 3; i++) { //update bias layer 1
			b1[i] = b1[i] - (lr/2) * sumofgb1[i];
			sumofgb1[i] = 0; //clean out sumofgb1
			System.out.println("b1["+i+"]"+b1[i]);
		}
		
		for(int i = 0; i < 3; i++) { //update weights layer 1
			for(int j = 0; j < 4; j++) {
				w1[i][j] = w1[i][j] - (lr/2) * sumofwg1[i][j];
				sumofwg1[i][j] = 0;//clean out sumofwg1
				System.out.println("w1["+i+"]"+"["+j+"]:"+w1[i][j]);
			}
		}
		
		for(int i = 0; i < 2; i++) { //update bias layer 2
			b2[i] = b2[i] - (lr/2) * sumofgb2[i];
			sumofgb2[i] = 0; //clean out sumofgb2
			System.out.println("b2["+i+"]"+b2[i]);
		}
		
		for(int i = 0; i < 2; i++) { //update weights layer 2
			for(int j = 0; j < 3; j++) {
				w2[i][j] = w2[i][j] - (lr/2) * sumofwg2[i][j];
				sumofwg2[i][j] = 0; //clean out sumofwg2
				System.out.println("w2["+i+"]"+"["+j+"]:"+w2[i][j]);
			}
		}
		
		
	}
		
	
}
	


