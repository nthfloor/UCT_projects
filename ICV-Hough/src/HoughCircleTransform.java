/*
 * Nathan Floor
 * FLRNAT001
 * 
 * Hough transform, with accumulator and local maxima detector. 
 */

public class HoughCircleTransform implements ProgressMonitor {
		private int[] originalData;
		private int[] outputData;
		private volatile int progressCounter;
		
		private int width;
		private int height;
		private int[] accumData;
		private int size=30; // number of circles to detect
		private int[] local_maxima;

		public HoughCircleTransform(int[] input, int w, int h, int numCircles) {
			size = numCircles;			
			width=w;
			height=h;
			init();
			originalData = new int[width*height];
			originalData=input;
		}
		//resets all data structures for next run
		private void init(){
			progressCounter=0;
			outputData = new int[width*height];
			
			for(int x=0;x<width;x++) {
				for(int y=0;y<height;y++) {
					outputData[x + (width*y)] = 0xff000000;
				}
			}			
			accumData = new int[width * height];
			for(int x=0;x<width;x++) {
				for(int y=0;y<height;y++) {
					accumData[x*width+y] =0;
				}
			}
		}
		
		//scan image a number  of times looking for circles with different radius
		public int[] detectCircles(int r){
			init();			
			accumulate(r);
			System.out.println("Hough Transform complete.");
			return outputData;
		}

		// hough transform for lines (polar), returns the accumulator array
		private void accumulate(int radius) {						
			int a = 0;
			int b = 0;
			double angle = 0;			
				
			//pass over image data and accumulate votes for centers
			for(int x=0;x<width;x++) {			
				for(int y=0;y<height;y++) {
					progressCounter++;
					//check for edges
					if ((originalData[y*width+x] & 0xff)== 255) {

						for (int theta=0; theta<360; theta++) {
							angle = (theta * 3.14159265) / 180;
							a = (int)Math.round(x - radius * Math.cos(angle));
							b = (int)Math.round(y - radius * Math.sin(angle));
							if(a < width && a > 0 && b < height && b > 0) {
								accumData[a + (b * width)] += 1;
							}
						}
					}
				}
			}
			
			// Find max
			int max=0;
			for(int x=0;x<width;x++) {
				for(int y=0;y<height;y++) {
					if (accumData[x + (y * width)] > max) {
						max = accumData[x + (y * width)];
					}
				}
			}
		
			// Normalize all the values
			int pixel_value;
			for(int x=0;x<width;x++) {
				for(int y=0;y<height;y++) {
					progressCounter++;					
					pixel_value = (int)(((double)accumData[x + (y * width)]/(double)max)*255.0);
					
					//also convert to greyscale for pixel array
					accumData[x + (y * width)] = 0xff000000 | (pixel_value << 16 | pixel_value << 8 | pixel_value);
				}
			}
			localMaxima(radius);
		}
		
		//find local mixima to estimate circle centers
		private int[] localMaxima(int radius) {
			local_maxima = new int[size*3];
			int[] output = new int[width*height];
		
			//loop through image data to identify maxima
			for(int x=0;x<width;x++) {
				for(int y=0;y<height;y++) {
					int value = (accumData[x + (y * width)] & 0xff);
					// if not lowest than add it and sort to correct position
					if (value > local_maxima[(size-1)*3]) {
						// array will act as a queue(start at the back and move forward)
						local_maxima[(size-1)*3] = value;
						local_maxima[(size-1)*3+1] = x;
						local_maxima[(size-1)*3+2] = y;
					
						// shift up until in right place
						int i = (size-2)*3;
						while ((i >= 0) && (local_maxima[i+3] > local_maxima[i])) {
							for(int j=0; j<3; j++) {
								int temp = local_maxima[i+j];
								local_maxima[i+j] = local_maxima[i+3+j];
								local_maxima[i+3+j] = temp;
							}
							i = i - 3;
							if (i < 0) 
								break;
						}
					}
					progressCounter++;
				}
			}
		
			//draw circles based off the maxima found using a fixed radius
			for(int i=size-1; i>=0; i--){	
				drawCircle(local_maxima[i*3], local_maxima[i*3+1], local_maxima[i*3+2], radius);
			}
			return output;
		}
	
		private void setPixel(int value, int xPos, int yPos) {
			outputData[(yPos * width)+xPos] = 0xff000000 | (value << 16 | value << 8 | value);
		}
		
		// draw circle at x y for centers found
		private void drawCircle(int pix, int xCenter, int yCenter, int radius) {
			pix = 250;
			
			int x, y, r2;
			r2 = radius * radius;
			
			setPixel(pix, xCenter, yCenter - radius);
			setPixel(pix, xCenter, yCenter + radius);			
			setPixel(pix, xCenter - radius, yCenter);
			setPixel(pix, xCenter + radius, yCenter);
			
			y = radius;
			x = 1;
			y = (int) (Math.sqrt(r2 - 1) + 0.5);
			while (x < y) {
				    setPixel(pix, xCenter + x, yCenter + y);
				    setPixel(pix, xCenter + x, yCenter - y);				    
				    setPixel(pix, xCenter - y, yCenter + x);
				    setPixel(pix, xCenter - y, yCenter - x);
				    setPixel(pix, xCenter - x, yCenter + y);
				    setPixel(pix, xCenter - x, yCenter - y);
				    setPixel(pix, xCenter + y, yCenter + x);
				    setPixel(pix, xCenter + y, yCenter - x);
				    x += 1;
				    y = (int) (Math.sqrt(r2 - x*x) + 0.5);
			}
			if (x == y) {
				setPixel(pix, xCenter - x, yCenter + y);
				setPixel(pix, xCenter - x, yCenter - y);
				setPixel(pix, xCenter + x, yCenter + y);
				setPixel(pix, xCenter + x, yCenter - y);
			}
		}

		public int[] getAcc() {
			return accumData;
		}

		@Override
		public int getProgressCounter() {
			return (int)progressCounter;
		}

		@Override
		public int getMax() {
			return 3*width*height;
		}
	}
