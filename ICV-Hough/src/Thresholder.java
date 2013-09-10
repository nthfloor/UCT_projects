// Hysteresis Thresholding class
// used to strip the image down to background and edge data only.
// the idea is to find a more connected result. Also reduces odd white pixels floating around.

public class Thresholder implements ProgressMonitor {

		static int[] input;
		static int[] output;
		private volatile int progressCounter;
		int width;
		int height;
		static int lower;
		static int upper;

		public Thresholder(int[] inputData, int w, int h) {
			progressCounter=0;
			
			width=w;
			height=h;
			input = new int[width*height];
			output = new int[width*height];
			input=inputData;
			lower=25;
			upper=50;
		}

		//perform thresholding procedure
		public int[] process() {
			progressCounter=0;
			for(int x=0;x<width;x++) {
				for(int y=0;y<height;y++) {
					int value = (input[y*width+x]) & 0xff; 
					if (value >= upper) {
						input[y*width+x] = 0xffffffff;
						hystConnect(x, y);
					}
					progressCounter++;
				}
			}
		
			for(int x=0;x<width;x++) {
				for(int y=0;y<height;y++) {
					if (input[y*width+x] == 0xffffffff)
						output[y*width+x] = 0xffffffff;
					else
						output[y*width+x] = 0xff000000;
					
					progressCounter++;
				}
			}
			return output;
		}
		private void hystConnect(int x, int y) {
			int value = 0;
			for (int x1=x-1;x1<=x+1;x1++) {
				for (int y1=y-1;y1<=y+1;y1++) {
					if ((x1 < width) & (y1 < height) & (x1 >= 0) & (y1 >= 0) & (x1 != x) & (y1 != y)) {
						value = (input[y1*width+x1])  & 0xff;
						if (value != 255) {
							if (value >= lower) {
								input[y1*width+x1] = 0xffffffff;
								hystConnect(x1, y1);
							} 
							else {
								input[y1*width+x1] = 0xff000000;
							}
						}
					}
				}
			}
		}	

		@Override
		public int getProgressCounter() {
			return progressCounter;
		}

		@Override
		public int getMax() {
			return width*height*2;
		}

	}
