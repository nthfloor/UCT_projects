/*
 * Nathan Floor
 * FLRNAT001
 * 
 * Sobel Edge Detection class
 * 
 */

public class EdgeDetector implements ProgressMonitor{
	private int[][] filter_x = {{-1,0,1}, {-2,0,2}, {-1,0,1}};
	private int[][] filter_y = {{1,2,1}, {0,0,0}, {-1,-2,-1}};
	
	private volatile int progressCounter = 0;
	private int width = 0;
	private int height = 0;
	
	private int[] input;
	private int[] edges;
	private int filterSize = 3;
	
	public EdgeDetector(int[] inputData, int w, int h){
		width = w;
		height = h;

		input = new int[w*h];
		edges = new int[w*h];
		input = inputData;
	}
	
	public int[] detectEdges(){
		int max = 0;
		float ratio = 0;
		int[] gradientMagnitude = new int[width*height];
		int[] x_sum = new int[width*height];
		int[] y_sum = new int[width*height];

		//loop through 2D grid of image pixel data
		for(int x=1;x<width-1;x++){
			for(int y=1;y<height-1;y++){
				x_sum[x+(width*y)] = 0;
				y_sum[x+(width*y)] = 0;

				for(int n=0;n<filterSize;n++){
					for(int m=0;m<filterSize;m++){
						int x2 = (x - 1 + n);
						int y2 = (y - 1 + m);
						
						//apply Sobel filter to each pixel
						x_sum[x+(width*y)] += (input[x2+(width*y2)] & 0xff) * filter_x[n][m];
						y_sum[x+(width*y)] += (input[x2+(width*y2)] & 0xff) * filter_y[n][m];
					}
				}				
				progressCounter++;
			}
		}
		
		//convert into circle space
		for(int x=0;x<width;x++){
			for(int y=0;y<height;y++){
				gradientMagnitude[x+(width*y)] = Math.abs(x_sum[x+(width*y)])+Math.abs(y_sum[x+(width*y)]);
				if(gradientMagnitude[x+(width*y)] > max)
					max = gradientMagnitude[x+(width*y)];	
				progressCounter++;
			}
		}		
		
		for(int x=0;x<width;x++){
			for(int y=0;y<height;y++){
				ratio = (float)max/(float)255;
				int pixel_value = (int)(gradientMagnitude[x+(width*y)]/ratio);
				
				//convert pixels into greyscale
				edges[x+(width*y)] = 0xff000000 | (pixel_value << 16 | pixel_value << 8 | pixel_value);
				progressCounter++;
			}
		}
		
		return edges;
	}

	//for progressbar monitor
	public int getProgressCounter() {
		return progressCounter;
	}

	@Override
	public int getMax() {
		return width*height*3;
	}
}
